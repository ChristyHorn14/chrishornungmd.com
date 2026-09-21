# Publishing the blog

The blog is static HTML for the existing GitHub Pages custom domain. Markdown is the article source of truth. Generated HTML is committed with the sources; GitHub Pages does not run Python. No browser framework or CMS is involved.

## Setup and build

Python 3.9+ is required. From the repository root, install the small Markdown dependency once (prefer your own virtual environment):

```sh
python3 -m venv /tmp/chrishornung-blog-venv
source /tmp/chrishornung-blog-venv/bin/activate
python3 -m pip install -r blog/requirements.txt
python3 blog/build_blog.py
```

Activate that environment in later terminal sessions before building. If `/tmp` is cleared, repeat setup. Python-Markdown 3.7 is the only direct dependency; Python 3.9 also installs the two pinned compatibility dependencies in requirements.txt. Front matter parsing uses the standard library.

## Add an article

1. Create `blog/posts/my-next-post.md` with this front matter, then write Markdown below it:

```markdown
---
title: "My next article"
date: "2026-09-21"
slug: "my-next-post"
description: "A short summary for the index and search/social previews."
---

## First section

Article text, **emphasis**, [links](https://example.com/), lists, and code.
```

All metadata values must be double-quoted strings; escape embedded double quotes as `\"`. This intentionally small YAML-compatible format supports one field per line, not full YAML. Required: `title`, `date` (YYYY-MM-DD), `slug`, `description`. Optional: `original_url` (HTTPS), `original_note` (requires original_url), `social_image` (local root-relative path), `social_image_alt`. Slugs must be unique lowercase words/numbers separated by hyphens. `assets`, `posts`, `templates`, `tests`, and `index` are reserved. Dates determine display order; future-dated posts are still published when built. There is no draft flag: keep drafts outside `posts/`.

2. Place images in `blog/assets/my-next-post/`. Use `![Descriptive alt text](/blog/assets/my-next-post/image.webp)`. For a caption, a content-only HTML `<figure>` with `<img>` and `<figcaption>` is supported (see staging-dojo.md). Keep original images when practical. Markdown supports headings, lists, links, blockquotes, fenced code, tables, and attribute lists. Raw HTML is allowed for trusted author content; do not paste unreviewed scripts or site boilerplate.
3. Run `python3 blog/build_blog.py`. This validates metadata, local links/anchors/assets, canonicals and analytics before writing. Identical output is not rewritten. It generates the index automatically, newest-first (slug breaks date ties).
4. Preview and inspect, then commit/push yourself when satisfied. Include generated HTML and images along with source changes.

## Files and URLs

- `posts/*.md`: content and article-specific metadata.
- `templates/page.html`: shared HTML shell, metadata, navigation, footer and analytics slot.
- `templates/article.html` and `templates/index.html`: layouts.
- `build_blog.py`: deterministic generator and built-in validation.
- `blog.css`: scoped blog styling, loaded only on blog pages; shared `/styles.css` supplies the existing site design.
- `index.html`: generated `/blog/` listing.
- `<slug>/index.html`: generated `/blog/<slug>/` article.
- `assets/<slug>/`: local article images.
- `tests/test_build_blog.py`: lightweight regression tests.

Do not edit generated HTML. Changing a published slug changes its public URL; prefer keeping it stable. Removing/renaming a source leaves an old generated page, and the build fails with its path so you can deliberately remove or redirect it. The generator never deletes files automatically. Root-relative assets target the custom domain and root-served local preview, not the temporary GitHub project-subdirectory URL.

## Shared analytics and metadata

Every build reads the marked Cloudflare Web Analytics snippet from the root homepage and inserts it unchanged into `templates/page.html`'s analytics slot. The build fails if the homepage snippet is absent or generated pages do not contain exactly the expected beacon. Posts never contain analytics or tokens. The token remains the site's existing public client-side token.

Titles, descriptions, Open Graph, Twitter cards and canonical URLs are generated for the index and every article. Canonicals always use `https://chrishornungmd.com/blog/` or `https://chrishornungmd.com/blog/<slug>/`, including in local preview. Articles also include Article JSON-LD with author and original publication date. Social images default to `/social-card.png`; an optional `social_image` replaces it. Provide `social_image_alt` with a custom image. Original publication links appear as a restrained note. The Medium article is not edited; its own canonical is outside this build's control.

## Preview and checks

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/`, `/blog/`, and `/blog/staging-dojo/`. Stop with Ctrl-C. Check desktop/mobile layout and navigation. The existing analytics script is present in local previews as requested.

```sh
python3 blog/build_blog.py --check
python3 -m unittest discover -s blog/tests -v
```

`--check` validates without writing and fails if generated HTML is out of date. External links are preserved but are not network-checked on every build. The root sitemap is not managed by this generator; the index and homepage links provide discovery.

## Staging Dojo migration provenance

Migrated from the specified Medium URL on September 21, 2026. Its displayed publication date is December 14, 2025. The complete currently published article was copied, preserving paragraphs, 12 body headings (including the opening H3), six ordered-list items, bold emphasis, four links, and one image/caption. No code blocks were present. Medium's navigation, subscription prompts, tags and recommendations are not article content and were omitted.

The screenshot is Medium's 1400px WebP rendition, copied byte-for-byte without additional recompression from:
`https://miro.medium.com/v2/resize:fit:1400/format:webp/1*xCpq_4ToL8JCZBu3SgauQg.png`

The original image had empty alt text; descriptive alt text was added. This reproduces the content available at migration time, not a verified archival December 2025 revision. Historical claims were not updated.
