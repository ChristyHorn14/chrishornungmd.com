# Chris Hornung, MD

A lightweight professional portfolio for surgical education, clinical research, and interactive medical learning.

## Hosting

GitHub Pages publishes `main` from `/ (root)`. No dependencies, build step, backend, analytics, cookies, or third-party fonts. Every commit to main automatically redeploys. `.nojekyll` ensures files are served directly.

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

## Connect chrishornungmd.com later

`CNAME.example` contains the intended domain but deliberately is not an active `CNAME`: activating it now would redirect the working temporary URL before DNS is ready. No Cloudflare changes have been made.

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

Local desktop visual review, 390px and 320px viewport overflow checks, keyboard-visible skip-link focus, internal anchor checks, and both live app destinations were checked before deployment. This is a static page with no client JavaScript. Content remains available without scripts or external services.

## Crabs release updates

The Crabs section is generated into `index.html` between the `GENERATED CRABS RELEASES` markers. It stays available without JavaScript, including the native expandable What’s New / release history. The importer uses only published releases and an explicit allowlist of dates, totals, and reviewed `whats_new` text; audit and compatibility fields are excluded. No raw source JSON is hosted or duplicated. The general import note follows the generated public `website/whats-new.md`; review it if that public guidance changes.

For each release:

1. Run the CrabsChangeLog release tool against the old and new packages.
2. Review the generated public wording and test the update in Anki.
3. Mark the reviewed release published in CrabsChangeLog.
4. From this website repository, import the generated public data:

   ```sh
   python3 scripts/update_crabs_release.py /path/to/CrabsChangeLog/website/releases.json
   python3 scripts/update_crabs_release.py /path/to/CrabsChangeLog/website/releases.json --check
   ```

5. Preview with `python3 -m http.server 8000`, check desktop/mobile and expand the history, then review the diff. No build or TypeScript step is required. Commit and deploy only after approval.

Do not hand-edit the generated block. The latest published release is selected by date; older published entries automatically appear in history. Draft releases are ignored. Review public wording before importing it: the importer escapes HTML but preserves the source text. The existing Access the deck Google Form URL must remain unchanged; its submission confirmation supplies the download link.
