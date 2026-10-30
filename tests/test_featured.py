import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import featured_projects as featured


class FeaturedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads((ROOT / 'data/repositories.json').read_text(encoding='utf-8'))
        cls.data = featured.load(cls.snapshot)

    def test_manifest_selects_six_existing_public_source_projects(self):
        self.assertEqual(len(self.data['projects']), 6)
        for bad_field, bad_value in [('private', True), ('fork', True), ('archived', True)]:
            snapshot = copy.deepcopy(self.snapshot)
            repo = next(r for r in snapshot['repositories'] if r['name'] == self.data['projects'][0]['name'])
            repo[bad_field] = bad_value
            with self.assertRaises(ValueError):
                featured.load(snapshot)

    def test_missing_project_is_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot['repositories'] = [r for r in snapshot['repositories'] if r['name'] != self.data['projects'][0]['name']]
        with self.assertRaises(ValueError):
            featured.load(snapshot)

    def test_html_escapes_editorial_content(self):
        data = copy.deepcopy(self.data)
        data['projects'][0]['title']['zh'] = '<script>alert("demo")</script>'
        rendered = featured.website(data)
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertEqual(rendered.count('<article '), 6)

    def test_export_preflights_all_destinations_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile, site = root / 'profile', root / 'site'
            profile.mkdir()
            site.mkdir()
            original = f'Owner biography\n{featured.START}\nOld selection\n{featured.END}\nOwner footer\n'
            for name in ['README.md', 'README.zh.md']:
                (profile / name).write_text(original, encoding='utf-8')
            (site / 'index.html').write_text('No approved markers', encoding='utf-8')
            with self.assertRaises(ValueError):
                featured.export(self.data, profile, site)
            self.assertEqual((profile / 'README.md').read_text(encoding='utf-8'), original)
            (site / 'index.html').write_text(original, encoding='utf-8')
            self.assertEqual(len(featured.export(self.data, profile, site, check=True)), 3)
            self.assertEqual((profile / 'README.md').read_text(encoding='utf-8'), original)
            self.assertEqual(len(featured.export(self.data, profile, site)), 3)
            self.assertEqual(featured.export(self.data, profile, site, check=True), [])
            for path in [profile / 'README.md', profile / 'README.zh.md', site / 'index.html']:
                rendered = path.read_text(encoding='utf-8')
                self.assertTrue(rendered.startswith('Owner biography\n'))
                self.assertTrue(rendered.endswith('Owner footer\n'))

    def test_ambiguous_or_reversed_markers_are_rejected(self):
        for body in ['', featured.END + featured.START, featured.START * 2 + featured.END]:
            with self.assertRaises(ValueError):
                featured.replace_block(body, 'selection')

    def test_priority_and_guide_keep_evidence_separate_from_maintenance(self):
        base = {'name': 'fixture', 'fork': False, 'description': '', 'inspection': {'state': 'content'}}
        self.assertEqual(featured.priority(base, {'fixture'}), '重点 / Focus')
        self.assertEqual(featured.priority(base, set()), '按需 / On demand')
        self.assertEqual(featured.priority({**base, 'fork': True}, set()), '参考 / Reference')
        self.assertEqual(featured.priority({**base, 'inspection': {'state': 'placeholder'}}, set()), '待评估 / Pending')
        guide = featured.guide(self.data, self.snapshot)
        for project in self.data['projects']:
            self.assertEqual(guide.count(f'<a id="{project["anchor"]}"></a>'), 1)
            for command in project['commands']:
                self.assertIn(command, guide)
            for lang in ('en', 'zh'):
                self.assertIn(project['limits'][lang], guide)


if __name__ == '__main__':
    unittest.main()
