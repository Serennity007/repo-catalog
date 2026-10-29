import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'scripts/build_catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def tree(*paths, truncated=False):
    return {'sha': 'abc123', 'truncated': truncated, 'tree': [{'path': p, 'type': 'blob', 'sha': 'blob123'} for p in paths]}


class EvidenceTests(unittest.TestCase):
    def test_license_only_is_placeholder(self):
        self.assertEqual(catalog.inspect_tree(tree('LICENSE'))['state'], 'placeholder')

    def test_readme_stub_is_placeholder(self):
        self.assertEqual(catalog.inspect_tree(tree('README.md', 'LICENSE'), '# Example\n\nDeveloper resource.')['state'], 'placeholder')

    def test_substantive_readme_is_documentation(self):
        guide = '# Guide\n\n' + '\n'.join(f'Step {i}: '+ 'A complete worked example with input, output and explanation. ' * 3 for i in range(6))
        self.assertEqual(catalog.inspect_tree(tree('README.md', 'LICENSE'), guide)['state'], 'docs')

    def test_metadata_and_banner_do_not_inflate_content(self):
        self.assertEqual(catalog.inspect_tree(tree('LICENSE', '.github/banner.svg', '.gitattributes', 'README.zh-CN.md'))['state'], 'placeholder')

    def test_nested_readme_is_content(self):
        self.assertEqual(catalog.inspect_tree(tree('guides/README.md'))['state'], 'content')

    def test_code_is_content(self):
        self.assertEqual(catalog.inspect_tree(tree('scripts/tool.py'))['state'], 'content')

    def test_truncated_or_missing_tree_is_rejected(self):
        for invalid in (tree('tool.py', truncated=True), {}, {'message': 'rate limited'}):
            with self.assertRaises(ValueError):
                catalog.inspect_tree(invalid)

    def test_auth_failure_is_not_empty_repository(self):
        response = subprocess.CompletedProcess([], 1, b'', b'HTTP 403: Forbidden')
        with patch.object(catalog.subprocess, 'run', return_value=response), patch.object(catalog.time, 'sleep'):
            with self.assertRaises(RuntimeError):
                catalog.api('repos/owner/example')

    def test_later_pagination_failure_is_not_partial_success(self):
        with patch.object(catalog, 'api', side_effect=[[{'name': str(i), 'private': False} for i in range(100)], RuntimeError('page 2 failed')]):
            with self.assertRaises(RuntimeError):
                catalog.all_repos()

    def test_private_repositories_are_filtered(self):
        with patch.object(catalog, 'api', return_value=[{'name': 'public', 'private': False}, {'name': 'secret', 'private': True}]):
            self.assertEqual([r['name'] for r in catalog.all_repos()], ['public'])

    def test_specific_groups_win_over_generic_ai(self):
        for name, expected in [('ai-coding-picks', 'reading'), ('ai-commit', 'cli'), ('xss-audit-desktop', 'security'), ('taotao-futures-research', 'markets'), ('paper-zh-translation', 'research')]:
            self.assertEqual(catalog.group_for({'name': name, 'description': '', 'fork': False}), expected)

    def test_forks_and_mirrors_keep_provenance(self):
        self.assertEqual(catalog.group_for({'name': 'GhostTrack', 'fork': True}), 'forks')
        self.assertEqual(catalog.group_for({'name': 'example', 'fork': False, 'description': 'Unofficial mirror of upstream'}), 'mirrors')

    def test_markdown_cells_cannot_add_rows_or_html(self):
        result = catalog.cell('a|b\n<script>')
        self.assertNotIn('|', result)
        self.assertNotIn('\n', result)
        self.assertNotIn('<script>', result)


class SnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads(catalog.SNAPSHOT.read_text(encoding='utf-8'))

    def test_public_only_unique_and_valid(self):
        catalog.validate(self.snapshot)

    def test_private_snapshot_input_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot['repositories'][0]['private'] = True
        with self.assertRaises(ValueError):
            catalog.render(snapshot)

    def test_offline_render_is_reproducible(self):
        for name, body in catalog.render(self.snapshot).items():
            self.assertEqual((ROOT / name).read_text(encoding='utf-8'), body, name)

    def test_every_repository_listed_once_in_full_index(self):
        body = catalog.render(self.snapshot)['docs/catalog.md']
        for repo in self.snapshot['repositories']:
            self.assertEqual(body.count(f']({repo["url"]})'), 1, repo['name'])

    def test_category_links_have_targets(self):
        outputs = catalog.render(self.snapshot)
        import re
        for anchor in re.findall(r'docs/catalog.md#([a-z]+)', outputs['README.md']):
            self.assertIn(f'<a id="{anchor}"></a>', outputs['docs/catalog.md'])

    def test_recent_dates_use_beijing_time(self):
        snapshot = copy.deepcopy(self.snapshot)
        repo = next(r for r in snapshot['repositories'] if r['name'] == 'xss-audit-desktop')
        repo['pushed_at'] = '2030-01-01T20:00:00Z'
        body = catalog.render(snapshot)['README.zh-CN.md']
        self.assertIn('| [xss-audit-desktop](https://github.com/Serennity007/xss-audit-desktop) | 2030-01-02 |', body)


if __name__ == '__main__':
    unittest.main()
