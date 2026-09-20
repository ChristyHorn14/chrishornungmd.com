"""Render published public Crabs release data into the static homepage."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '        <!-- BEGIN GENERATED CRABS RELEASES -->'
END = '        <!-- END GENERATED CRABS RELEASES -->'


def public_releases(source):
    if source.get('schema') != 1:
        raise ValueError('Unsupported release schema')
    releases = []
    for item in source['releases']:
        if item.get('publication_status') != 'published':
            continue
        stamp = date.fromisoformat(item['date'])
        counts = [item['total_cards'], item['total_notes']]
        if any(type(count) is not int or count < 0 for count in counts):
            raise ValueError('Invalid release counts')
        wording = item['whats_new']
        if not isinstance(wording, list) or any(not isinstance(line, str) for line in wording):
            raise ValueError('Invalid public release wording')
        # Explicit allowlist: never copy audit, compatibility, or identity fields.
        releases.append(dict(date=stamp.isoformat(), label=f'{stamp:%B} {stamp.day}, {stamp.year}',
                             cards=counts[0], notes=counts[1], wording=wording))
    releases.sort(key=lambda item: item['date'], reverse=True)
    if not releases or len({item['date'] for item in releases}) != len(releases):
        raise ValueError('Published release dates must be present and unique')
    if releases[0]['date'] != source['latest_published_release_date']:
        raise ValueError('Latest published release does not match release history')
    return releases


def render(releases):
    def stamp(item):
        return f'<time datetime="{item["date"]}">{item["label"]}</time>'

    def counts(item):
        return f'{item["cards"]:,} cards · {item["notes"]:,} notes'

    def changes(item):
        return '\n'.join('              <li>' + escape(line) + '</li>' for line in item['wording'])

    latest = releases[0]
    lines = [START, '        <div class="crabs-release" aria-label="Deck release information">',
             f'          <p class="release-date">Current release · {stamp(latest)}</p>',
             f'          <p class="release-counts">{counts(latest)}</p>',
             '          <details class="release-details">',
             '            <summary>What’s New &amp; release history</summary>',
             '            <div class="release-body">',
             '              <h3>What’s New</h3>']
    if latest['wording']:
        lines += ['              <ul>', changes(latest), '              </ul>']
    if len(releases) > 1:
        lines += ['              <h3>Previous releases</h3>']
        for item in releases[1:]:
            lines += ['              <article class="release-history-entry">',
                      f'                <h4>{stamp(item)}</h4>',
                      f'                <p>{counts(item)}</p>']
            if item['wording']:
                lines += ['                <ul>', changes(item), '                </ul>']
            lines += ['              </article>']
    lines += ['              <p class="release-note">Card updates may include text, tags, media, or deck placement changes. Items removed from this package may remain in an existing Anki collection after import.</p>',
              '            </div>', '          </details>', '        </div>', END]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Generated website/releases.json from CrabsChangeLog')
    parser.add_argument('--check', action='store_true', help='Check that the homepage matches without writing')
    args = parser.parse_args()
    generated = render(public_releases(json.loads(args.source.read_text())))
    target = ROOT / 'index.html'
    current = target.read_text()
    if current.count(START) != 1 or current.count(END) != 1:
        raise ValueError('Expected exactly one release marker pair')
    before, rest = current.split(START)
    _, after = rest.split(END)
    updated = before + generated + after
    if args.check:
        if updated != current:
            raise SystemExit('Crabs release content is out of date')
        print('Crabs release content matches published source')
    else:
        target.write_text(updated)
        print('Updated Crabs release content')


if __name__ == '__main__':
    main()
