# Chris Hornung, MD

A lightweight professional portfolio for surgical education, clinical research, and interactive medical learning.

## Hosting

GitHub Pages publishes `main` from `/ (root)`. No dependencies, build step, backend, analytics, cookies, or third-party fonts. Every commit to main automatically redeploys. `.nojekyll` ensures files are served directly.

URL: chrishornungmd.com

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

 or external services.
