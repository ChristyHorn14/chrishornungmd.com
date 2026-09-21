"""Build the static Crabs page and homepage summary from a validated public bundle."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import os
import tempfile
from string import Template

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
        wording = item['whats_new'] + item.get('editorial_notes', [])
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


def number(value):
    if type(value) is not int or value < 0:
        raise ValueError('Expected a nonnegative integer count')
    return value


def validate_bundle(releases, stats, tags):
    published = public_releases(releases)
    latest = published[0]
    if releases['latest_release_date'] != latest['date']:
        raise ValueError('Latest release is a candidate; review and mark published before website import')
    for data in (stats, tags):
        if data.get('schema') != 1 or data.get('release_date') != latest['date']:
            raise ValueError('Unsupported or mismatched stats/tag release')
    if stats['total_notes'] != latest['notes'] or stats['total_cards'] != latest['cards']:
        raise ValueError('Stats and release totals disagree')
    if tags['count_unit'] != 'notes_and_cards':
        raise ValueError('Unknown tag count units')
    for key in ('total_notes','total_cards','total_tags','total_tag_nodes','total_media','total_note_types','untagged_notes'):
        number(stats[key])
    record=next(r for r in releases['releases'] if r['date']==latest['date'])
    if stats['total_media'] != record['total_media']:
        raise ValueError('Media totals disagree')
    if stats['untagged_notes']>stats['total_notes']:
        raise ValueError('Invalid untagged note count')
    if stats['deck_name'] is not None and not isinstance(stats['deck_name'],str):
        raise ValueError('Invalid deck name')
    if not isinstance(stats['deck_names'],list) or any(not isinstance(n,str) for n in stats['deck_names']):
        raise ValueError('Invalid deck names')
    seen=set(); explicit=0
    def nodes(items, parent=None):
        nonlocal explicit
        paths=[node['path'] for node in items]
        if paths!=sorted(set(paths)):
            raise ValueError('Tag siblings must be sorted and unique')
        for node in items:
            path=node['path']
            if not isinstance(path,str) or path in seen:
                raise ValueError('Invalid/duplicate tag path')
            seen.add(path)
            if node['name']!=path.split('::')[-1] or node['depth']!=len(path.split('::'))-1:
                raise ValueError('Tag path/depth mismatch')
            if (parent is None and '::' in path) or (parent is not None and path.rsplit('::',1)[0]!=parent['path']):
                raise ValueError('Invalid hierarchy relationship')
            if type(node['explicit']) is not bool:
                raise ValueError('Invalid explicit flag')
            explicit+=node['explicit']
            if node['explicit'] != (node['direct_notes']>0):
                raise ValueError('Explicit tag has inconsistent direct count')
            for unit in ('notes','cards'):
                direct=number(node['direct_'+unit]); aggregate=number(node['aggregate_'+unit])
                if direct>aggregate or aggregate>stats['total_'+unit]:
                    raise ValueError('Invalid tag counts')
                if parent is not None and aggregate>parent['aggregate_'+unit]:
                    raise ValueError('Child count exceeds parent')
            nodes(node['children'],node)
    nodes(tags['roots'])
    if len(seen)!=tags['total_nodes'] or len(seen)!=stats['total_tag_nodes'] or explicit!=tags['total_tags'] or explicit!=stats['total_tags']:
        raise ValueError('Tag totals disagree')
    for record in releases['releases']:
        changes=record.get('tag_changes')
        if changes is None:
            continue
        if changes.get('schema')!=1 or changes.get('count_unit')!='notes':
            raise ValueError('Unsupported tag-change schema')
        for key in ('tags_added','tags_removed','branches_added','branches_removed'):
            values=changes[key]
            if not isinstance(values,list) or any(not isinstance(v,str) for v in values) or values!=sorted(set(values)):
                raise ValueError('Invalid tag change paths')
        for row in changes['by_branch']:
            for key in ('depth','before_notes','after_notes','added_notes','removed_notes','modified_notes'):
                number(row[key])
            if type(row['net_notes']) is not int or row['net_notes']!=row['after_notes']-row['before_notes']:
                raise ValueError('Invalid branch delta')
    return published


def inline(text):
    # Explicitly small safe Markdown vocabulary; no raw HTML or executable links.
    pattern=r'(`[^`]+`|\[[^\]]+\]\(https://[^\s)]+\))'
    parts=[]
    for token in re.split(pattern,text):
        if token.startswith('`') and token.endswith('`'):
            parts.append('<code>'+escape(token[1:-1])+'</code>')
        elif re.fullmatch(r'\[[^\]]+\]\(https://[^\s)]+\)',token):
            label,url=token[1:-1].split('](',1)
            parts.append('<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>')
        else:
            parts.append(escape(token))
    return ''.join(parts)


def markdown(text):
    output=[];paragraph=[];in_list=False
    def flush():
        if paragraph:
            output.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
    for line in text.splitlines()+['']:
        if not line.startswith('- ') and in_list:
            output.append('</ul>');in_list=False
        if line.startswith('# '):
            flush()  # Page supplies the section title.
        elif line.startswith('## '):
            flush();output.append('<h3>'+inline(line[3:])+'</h3>')
        elif line.startswith('- '):
            flush()
            if not in_list:output.append('<ul>');in_list=True
            output.append('<li>'+inline(line[2:])+'</li>')
        elif not line.strip():flush()
        else:paragraph.append(line.strip())
    return '\n'.join(output)


def bullets(lines):
    return '<ul>'+''.join('<li>'+escape(line)+'</li>' for line in lines)+'</ul>' if lines else ''


def render(releases):
    latest=releases[0]
    return '\n'.join([START, '        <div class="crabs-release" aria-label="Deck release information">',
        f'          <p class="release-date">Current release · <time datetime="{latest["date"]}">{latest["label"]}</time></p>',
        f'          <p class="release-counts">{latest["cards"]:,} cards · {latest["notes"]:,} notes</p>',
        '          <a class="text-link" href="crabs/">Explore the Crabs guide &amp; releases <span aria-hidden="true">→</span></a>',
        '        </div>', END])


def render_tree(nodes):
    result=[]
    for node in nodes:
        label=escape(node['name'] or '(empty component)')
        count=f'<span class="tag-count">{node["aggregate_notes"]:,} notes · {node["aggregate_cards"]:,} cards</span>'
        exact=f'{node["direct_notes"]:,} notes · {node["direct_cards"]:,} cards tagged exactly here'
        if node['children']:
            content=f'<details><summary>{label}{count}</summary><p class="tag-direct">{exact}</p><ul>{render_tree(node["children"])}</ul></details>'
        else:
            content=f'<div class="tag-leaf">{label}{count}</div>'
        result.append(f'<li data-path="{escape(node["path"],quote=True)}">{content}</li>')
    return '\n'.join(result)


def build(source, root=ROOT):
    data_dir=source.parent
    raw=json.loads(source.read_text(encoding='utf-8'))
    stats=json.loads((data_dir/'deck-stats.json').read_text(encoding='utf-8'))
    tags=json.loads((data_dir/'tags.json').read_text(encoding='utf-8'))
    releases=validate_bundle(raw,stats,tags)
    latest=releases[0]
    homepage=(root/'index.html').read_text(encoding='utf-8')
    if homepage.count(START)!=1 or homepage.count(END)!=1 or homepage.index(START)>homepage.index(END):
        raise ValueError('Expected one ordered homepage release marker pair')
    # Keep the existing download mechanism as the sole link configuration.
    download=re.search(r'href="(https://docs\.google\.com/forms/[^"]+)"',homepage)
    if not download:raise ValueError('Existing Google Form download link not found')
    from html import unescape
    download=unescape(download.group(1))
    current=next(r for r in raw['releases'] if r['date']==latest['date'])
    whats_new=bullets(latest['wording'])
    changes=current.get('tag_changes')
    if changes:
        for title,key in [('New tags','tags_added'),('Removed tags','tags_removed'),('New hierarchy branches','branches_added')]:
            whats_new+=f'<details class="release-history"><summary>{title} ({len(changes[key])})</summary><div class="tag-list">'+bullets(changes[key])+'</div></details>'
    history=''
    for record in releases:
        history+=f'<details class="release-history"><summary><time datetime="{record["date"]}">{record["label"]}</time> · {record["cards"]:,} cards</summary>'
        history+=f'<p>{record["notes"]:,} notes · {record["cards"]:,} cards</p>'
        history+=bullets(record['wording']) or '<p>Published baseline; change statistics were not recorded.</p>'
        history+='</details>'
    docs={name:(data_dir/name).read_text(encoding='utf-8') for name in ('how-to-use.md','updating.md')}
    template=Template((root/'templates/crabs.html').read_text(encoding='utf-8'))
    page=template.substitute(untagged=f"{stats['untagged_notes']:,}",deck_name=escape(stats['deck_name'] or ' / '.join(stats['deck_names'])),
        release_date=f'<time datetime="{latest["date"]}">{latest["label"]}</time>',download=escape(download,quote=True),
        stats=''.join(f'<div><dt>{label}</dt><dd>{stats[key]:,}</dd></div>' for key,label in
                      [('total_cards','Cards'),('total_notes','Notes'),('total_tags','Content tags'),('total_media','Media files')]),
        usage=markdown(docs['how-to-use.md']),updating=markdown(docs['updating.md']),
        tree=render_tree(tags['roots']),whats_new=whats_new,history=history)
    before,rest=homepage.split(START);_,after=rest.split(END)
    outputs={root/'index.html':before+render(releases)+after,root/'crabs/index.html':page}
    # Only public artifacts; never source packages, snapshots, raw notes or audits.
    for name,data in [('releases.json',raw),('deck-stats.json',stats),('tags.json',tags)]:
        outputs[root/'crabs/data'/name]=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    for name,text in docs.items():outputs[root/'crabs/data'/name]=text
    return outputs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path,help='Generated website/releases.json; sibling stats, tags and docs required')
    parser.add_argument('--check',action='store_true',help='Validate and check generated files without writing')
    args=parser.parse_args()
    outputs=build(args.source)
    # Preflight every path before changing any file; individual replacements atomic.
    for path in outputs:
        if path.is_symlink() or ROOT.resolve() not in path.resolve().parents:
            raise ValueError('Unsafe website output path')
    stale=[str(p.relative_to(ROOT)) for p,text in outputs.items() if not p.exists() or p.read_text(encoding='utf-8')!=text]
    if args.check:
        if stale:raise SystemExit('Crabs build is out of date: '+', '.join(stale))
        print('Crabs page, homepage and public data match the source bundle')
        return
    staged=[]
    try:
        for path,text in outputs.items():
            path.parent.mkdir(parents=True,exist_ok=True)
            fd,temp=tempfile.mkstemp(prefix='.crabs-',dir=path.parent)
            staged.append((temp,path))
            with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as stream:stream.write(text)
        for temp,path in staged:os.replace(temp,path)
    finally:
        for temp,_ in staged:Path(temp).unlink(missing_ok=True)
    print('Built Crabs documentation, homepage summary and public data. No deployment performed.')


if __name__=='__main__':main()
