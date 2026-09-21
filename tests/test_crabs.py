import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from html.parser import HTMLParser
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import update_crabs_release as build

ROOT=Path(__file__).resolve().parents[1]


class CrabsTests(unittest.TestCase):
    def setUp(self):
        self.releases={'schema':1,'latest_release_date':'2027-01-01','latest_published_release_date':'2027-01-01',
            'releases':[{'date':'2027-01-01','publication_status':'published','total_cards':2,'total_notes':1,
                'total_media':0,'whats_new':['Measured change.'],'editorial_notes':['Author note.']}]}
        self.stats={'schema':1,'release_date':'2027-01-01','total_cards':2,'total_notes':1,'total_media':0,
            'total_tags':1,'total_tag_nodes':2,'total_note_types':1,'untagged_notes':0,'deck_name':'Crabs','deck_names':['Crabs']}
        leaf={'path':'Crabs::A','name':'A','depth':1,'explicit':True,'direct_notes':1,'aggregate_notes':1,
              'direct_cards':2,'aggregate_cards':2,'children':[]}
        root=dict(leaf,path='Crabs',name='Crabs',depth=0,explicit=False,direct_notes=0,direct_cards=0,children=[leaf])
        self.tags={'schema':1,'release_date':'2027-01-01','count_unit':'notes_and_cards','total_tags':1,'total_nodes':2,'roots':[root]}

    def validate(self):return build.validate_bundle(self.releases,self.stats,self.tags)

    def test_valid_bundle_includes_editorial(self):
        self.assertEqual(self.validate()[0]['wording'],['Measured change.','Author note.'])

    def test_candidate_rejected(self):
        self.releases['latest_release_date']='2027-02-01'
        with self.assertRaises(ValueError):self.validate()

    def test_mixed_release_rejected(self):
        self.tags['release_date']='2026-01-01'
        with self.assertRaises(ValueError):self.validate()

    def test_count_mismatch_rejected(self):
        self.stats['total_cards']=3
        with self.assertRaises(ValueError):self.validate()

    def test_corrupt_hierarchy_rejected(self):
        self.tags['roots'][0]['children'][0]['path']='Other::A'
        with self.assertRaises(ValueError):self.validate()

    def test_boolean_count_rejected(self):
        self.stats['total_tags']=True
        with self.assertRaises(ValueError):self.validate()

    def test_html_escaped_and_tree_collapsed(self):
        node=self.tags['roots'][0];node['name']='<script>alert(1)</script>'
        html=build.render_tree([node])
        self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html)
        self.assertNotIn(' open',html);self.assertIn('<summary>',html)

    def test_markdown_safe_supported_features(self):
        html=build.markdown('# Title\n\n## Heading\n\nText `tag` and <script>.\n\n- [Manual](https://example.org)\n- item\n')
        self.assertIn('<h3>Heading</h3>',html);self.assertIn('<code>tag</code>',html)
        self.assertIn('&lt;script&gt;',html);self.assertNotIn('<h1>',html)
        self.assertIn('<a href="https://example.org">Manual</a>',html)

    def test_homepage_is_concise_and_linked(self):
        html=build.render(self.validate())
        self.assertIn('href="crabs/"',html);self.assertNotIn('<details',html)

    def test_build_and_committed_public_data_are_consistent(self):
        # This also provides an offline build from the last imported public bundle.
        outputs=build.build(ROOT/'crabs/data/releases.json')
        for path,text in outputs.items():
            self.assertEqual(path.read_text(),text,str(path))

    def test_generated_html_local_links_and_unique_ids(self):
        class Links(HTMLParser):
            def __init__(self):super().__init__();self.ids=[];self.urls=[]
            def handle_starttag(self,tag,attrs):
                a=dict(attrs)
                if 'id' in a:self.ids.append(a['id'])
                for key in ('href','src'):
                    if key in a:self.urls.append(a[key])
        for filename in ['index.html','crabs/index.html']:
            page=ROOT/filename;p=Links();p.feed(page.read_text())
            self.assertEqual(len(p.ids),len(set(p.ids)))
            for url in p.urls:
                if url.startswith(('https:','mailto:')):continue
                if url.startswith('#'):
                    if url!='#':self.assertIn(url[1:],p.ids)
                else:
                    self.assertTrue((page.parent/url.split('#')[0]).exists(),url)
