import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'build_blog.py'
spec = importlib.util.spec_from_file_location('build_blog', MODULE)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def post(**changes):
    meta = dict(title='A title', date='2026-01-02', slug='new-post', description='A description')
    meta.update(changes)
    return '---\n' + '\n'.join(k + ': ' + json.dumps(v) for k, v in meta.items()) + '\n---\n\nA paragraph.'


class BlogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(build.ROOT / 'blog', self.root / 'blog', ignore=shutil.ignore_patterns('__pycache__'))
        for name in ('index.html', 'styles.css', 'icon.svg', 'social-card.png'):
            shutil.copyfile(build.ROOT / name, self.root / name)

    def test_metadata(self):
        meta, body = build.parse_post(post(title='A "quoted" title: & more'))
        self.assertEqual(meta['title'], 'A "quoted" title: & more')
        self.assertEqual(body, 'A paragraph.')

    def test_rejects_malformed_metadata(self):
        for text in (post(slug='../escape'), post(slug='assets'), post(slug='UPPER'), post(date='2025-02-30'),
                     post(date='20250102'), post(title=''), post(original_url='javascript:alert(1)'),
                     post(original_note='No source'), post().replace('title:', 'unknown:'),
                     post().replace('---\n\n', 'title: "Duplicate"\n---\n\n'), 'No front matter',
                     post().replace('"A title"', 'unquoted')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                build.parse_post(text)

    def test_new_post_gets_shell_analytics_metadata_and_listing(self):
        (self.root / 'blog/posts/new.md').write_text(post(), encoding='utf-8')
        outputs = build.render_site(self.root)
        article = outputs['blog/new-post/index.html']
        self.assertIn('href="https://chrishornungmd.com/blog/new-post/"', article)
        self.assertIn(build.analytics(self.root), article)
        self.assertIn('"datePublished": "2026-01-02"', article)
        self.assertIn('https://chrishornungmd.com/social-card.png', article)
        index = outputs['blog/index.html']
        self.assertLess(index.index('href="/blog/new-post/"'), index.index('href="/blog/staging-dojo/"'))
        self.assertIn(build.analytics(self.root), index)

    def test_duplicate_slugs(self):
        original = self.root / 'blog/posts/staging-dojo.md'
        shutil.copyfile(original, original.with_name('duplicate.md'))
        with self.assertRaisesRegex(ValueError, 'duplicate slug'):
            build.render_site(self.root)

    def test_missing_asset_fails(self):
        (self.root / 'blog/posts/new.md').write_text(post() + '\n\n![Missing](/blog/assets/missing.png)', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'missing local target'):
            build.render_site(self.root)

    def test_analytics_regression_fails(self):
        outputs = build.render_site(self.root)
        beacon = build.analytics(self.root)
        outputs['blog/index.html'] = outputs['blog/index.html'].replace(beacon, '')
        with self.assertRaisesRegex(ValueError, 'analytics or canonical'):
            build.validate(self.root, outputs, beacon)

    def test_deterministic_and_current(self):
        first = build.render_site(self.root)
        self.assertEqual(first, build.render_site(self.root))
        for path, html in first.items():
            self.assertEqual((self.root / path).read_text(encoding='utf-8'), html)

    def test_markdown_features(self):
        text = post() + '\n\n## Heading\n\n**Bold** and `code`.\n\n1. One\n2. Two\n\n```python\nx = 1\n```\n'
        (self.root / 'blog/posts/new.md').write_text(text, encoding='utf-8')
        html = build.render_site(self.root)['blog/new-post/index.html']
        for expected in ('<h2>Heading</h2>', '<strong>Bold</strong>', '<code>code</code>', '<ol>', 'class="language-python"'):
            self.assertIn(expected, html)

    def test_missing_homepage_beacon_fails(self):
        (self.root / 'index.html').write_text('<html></html>', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Cloudflare'):
            build.render_site(self.root)


if __name__ == '__main__':
    unittest.main()
