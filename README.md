# Chris Hornung, MD

A lightweight professional portfolio for surgical education, clinical research, and interactive medical learning.

## Hosting

GitHub Pages publishes `main` from `/ (root)`. No frontend dependencies, backend, analytics, cookies, or third-party fonts. Crabs uses a Python standard-library static build. Every commit to main automatically redeploys. `.nojekyll` ensures files are served directly.

Temporary URL: https://christyhorn14.github.io/chrishornungmd.com/

## Local preview

Run `python3 -m http.server 8000` in this directory and open http://localhost:8000.

## Updating content

- `index.html`: semantic page content, project cards, research items, navigation and SEO metadata.
- `styles.css`: shared colors, typography, responsive layout and reduced-motion behavior.
- `icon.svg` and `social-card.png`: site icon and social sharing artwork.
- `404.html`, `robots.txt`, `sitemap.xml`: error page and crawler support.

To add a tool, duplicate a `.project` article in `.projects`, change its title, description and verified HTTPS link, then give its illustration a suitable class. For an unreleased tool use a status label without a link. The grid wraps to one column on narrow screens. Add research items as articles in `.research-list`. Stable section IDs (`tools`, `research`, `about`) can later become separate page routes without changing the site's content model.

## Sources and editorial decisions

Read-only references reviewed on September 19, 2026:

- https://github.com/ChristyHorn14/oral-cavity-staging-ninja — README, package manifest, and live application. Next.js / React / TypeScript; clinical T, N and stage-group drills. Live: https://oral-cavity-staging-ninja.vercel.app/
- https://github.com/ChristyHorn14/mohs-recon-dojo — README and live application. Next.js / TypeScript; current nasal module covers aesthetic subunits, structural needs and preferred reconstruction. Live: https://mohs-recon-dojo.vercel.app/

No TI-RADS repository was found in the account's 14-repository listing. Its description and In Development status follow the owner's brief. The bio, affiliation, and five research areas come directly from that brief. No publications, results, collaborators or statistics have been inferred. The card illustrations are original decorative CSS graphics, not diagnostic images. Rounded elements and case-based learning language subtly connect the site to the existing Dojo tools. No source app files or settings were changed.

## Domain configuration (historical setup reference)

The checkout now contains an active `CNAME` for `chrishornungmd.com`, and page canonicals use that domain. The following is the original setup reference, not an instruction to repeat completed DNS changes. No DNS settings are modified by the Crabs build.

When ready, follow this order:

1. Optionally verify ownership using GitHub account Settings → Pages; use the exact TXT value GitHub supplies.
2. In **this repository** Settings → Pages, save `chrishornungmd.com` as Custom domain. GitHub creates the active CNAME file when publishing from a branch. Alternatively rename `CNAME.example` to `CNAME` and confirm the setting.
3. In Cloudflare, configure these records, initially **DNS only** (gray cloud), TTL Auto:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | ChristyHorn14.github.io |

Replace conflicting web A/AAAA/CNAME records for @ or www only after checking their purpose; preserve mail and unrelated records. The www target contains no repository path. Optional IPv6 AAAA values for @ are `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, and `2606:50c0:8003::153`.

4. Once GitHub validates DNS and provisions a certificate, enable **Enforce HTTPS**. DNS and certificate provisioning may take up to 24 hours.
5. Replace `https://christyhorn14.github.io/chrishornungmd.com/` with `https://chrishornungmd.com/` in index.html (canonical, og:url, og:image), sitemap.xml, robots.txt and 404.html. Relative CSS/icon links already work on both hosts.
6. Verify apex HTTPS, www redirect, social image, navigation, and both existing app links.

Official reference: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

Future staging, mohs and tirads subdomains remain unconfigured. Add each domain to its own hosting project and use that provider's verified DNS instructions at that time; no application migration is necessary.

## Validation

Local desktop visual review, 390px and 320px viewport overflow checks, keyboard-visible skip-link focus, internal anchor checks, and both live app destinations were checked before deployment. The homepage is static; the Crabs child page progressively enhances its tag explorer with JavaScript. Content remains available without scripts or external services.

## Crabs documentation and release builds

The homepage stays the portfolio. Substantial projects can use a directory with an `index.html`; Crabs is the first, at `/crabs/`. Relative assets/navigation also work under the temporary GitHub project path. Shared typography/colors remain in `styles.css`, with page-specific rules in `crabs/crabs.css`.

Source of truth: `.apkg` → CrabsChangeLog → generated public JSON/Markdown → this static site. No counts, hierarchy or release history are maintained in the template. No Anki package, raw educational notes, audit or media archive is copied here.

From the CrabsChangeLog repository, use the documented `release_workflow.py ... --website /path/to/chrishornungmd.com` command. Candidate releases are reviewed there; the website stays on its last published bundle. After review/distribution, mark published using that command's `--publication-status published` option.

To import separately:

```sh
python3 scripts/update_crabs_release.py /path/to/CrabsChangeLog/website/releases.json
python3 scripts/update_crabs_release.py /path/to/CrabsChangeLog/website/releases.json --check
python3 -m unittest discover -s tests -v
```

The source must have sibling `deck-stats.json`, `tags.json`, `how-to-use.md`, and `updating.md`. The importer validates matching release dates, totals and hierarchy, and rejects candidate bundles. Older history without tag changes means unavailable, not zero.

For an offline rebuild from the last imported bundle:

```sh
python3 scripts/update_crabs_release.py crabs/data/releases.json
```

Generated: `crabs/index.html`, `crabs/data/*`, and the marked release block in homepage `index.html`. Human-maintained: `templates/crabs.html`, `crabs/crabs.css`, `crabs/explorer.js`, and the importer/tests. Usage/update prose belongs in CrabsChangeLog's `docs/` directory. Supported Markdown: headings, paragraphs, single-level bullets, inline code and HTTPS links. Text is escaped; raw HTML is not executed.

The native collapsed `details` tree and all documentation work without JavaScript. `explorer.js` adds literal path search, result announcements and collapse-all. The full tree is rendered from JSON at build time; no network request is needed at runtime. Search clears back to the user's previous expanded state. Counts are branch totals, not filtered search totals.

Preview with `python3 -m http.server 8000`, then open `/` and `/crabs/`. Review mobile layout, keyboard expansion/search, and both Git diffs. This is a Python static build, with no npm dependency or app framework. Importing never commits or deploys. Pushing the publishing branch will still trigger the existing GitHub Pages deployment.

The existing Google Form URL is preserved and read from the homepage during build. It currently uses a Google Forms `/edit` URL; verify respondent access before deciding whether to replace it with a public responder URL. No download-access behavior was changed.
