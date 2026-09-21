/* Progressive enhancement: the generated native details tree also works without JS. */
'use strict';
const tree = document.querySelector('#tag-tree');
const input = document.querySelector('#tag-search');
const items = Array.from(tree.querySelectorAll('li[data-path]'));
const details = Array.from(tree.querySelectorAll('details'));
const status = document.querySelector('#search-status');
let savedOpen = null;
document.querySelector('#search-controls').hidden = false;
function filterTags() {
  const query = input.value.trim().toLocaleLowerCase();
  if (!query) {
    items.forEach(item => { item.hidden = false; });
    if (savedOpen) details.forEach(item => { item.open = savedOpen.has(item); });
    savedOpen = null;
    status.textContent = '';
    return;
  }
  if (!savedOpen) savedOpen = new Set(details.filter(item => item.open));
  let matches = 0;
  // Full paths make matching a parent include its descendants. Reverse order lets
  // a child reveal its ancestors without interpreting punctuation as a selector.
  items.slice().reverse().forEach(item => {
    const ownMatch = item.dataset.path.toLocaleLowerCase().includes(query);
    if (ownMatch) matches += 1;
    const nested = item.querySelector(':scope > details > ul');
    const childMatch = nested && Array.from(nested.children).some(child => !child.hidden);
    item.hidden = !(ownMatch || childMatch);
    const control = item.querySelector(':scope > details');
    if (control) control.open = !!childMatch;
  });
  status.textContent = matches ? `${matches} matching tag paths. Counts still describe the full branches.` : 'No matching tags.';
}
input.addEventListener('input', filterTags);
document.querySelector('#collapse-tags').addEventListener('click', () => {
  input.value = '';
  filterTags();
  details.forEach(item => { item.open = false; });
  status.textContent = 'All branches collapsed.';
});
