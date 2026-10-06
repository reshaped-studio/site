(function () {
  'use strict';
  document.querySelectorAll('[data-object-guides]').forEach(function (group) {
    var tablist = group.querySelector('.object-tabs');
    var tabs = Array.from(tablist.querySelectorAll('button'));
    var panels = Array.from(group.querySelectorAll('.object-guide'));
    function select(index, focus) {
      tabs.forEach(function (tab, i) {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) tabs[index].focus();
    }
    tablist.setAttribute('role', 'tablist');
    tabs.forEach(function (tab, index) {
      tab.setAttribute('role', 'tab');
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].setAttribute('aria-labelledby', tab.id);
      panels[index].tabIndex = 0;
      tab.addEventListener('click', function () { select(index, false); });
      tab.addEventListener('keydown', function (event) {
        var next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { event.preventDefault(); select(next, true); }
      });
    });
    select(0, false);
    tablist.hidden = false;
  });
  var dialog = document.querySelector('.wireframe-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  var trigger = null;
  document.querySelectorAll('[data-enlarge]').forEach(function (button) {
    button.hidden = false;
    button.addEventListener('click', function () {
      trigger = button;
      dialog.querySelector('h2').textContent = button.dataset.title;
      dialog.querySelector('img').src = button.dataset.image;
      dialog.querySelector('img').alt = button.dataset.alt;
      dialog.querySelector('#wireframe-dialog-description').textContent = button.dataset.description;
      dialog.showModal();
    });
  });
  dialog.querySelector('[data-close-dialog]').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('close', function () { if (trigger) trigger.focus(); });
})();
