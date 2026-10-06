const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const script = fs.readFileSync(path.join(__dirname, '../src/js/design-plans.js'), 'utf8');
function element() {
  return { hidden: false, attrs: {}, events: {}, dataset: {}, setAttribute(k, v) { this.attrs[k] = v; }, addEventListener(k, fn) { this.events[k] = fn; }, focus() { this.focused = true; } };
}
function fixture({ modal = true } = {}) {
  const tabs = Array.from({ length: 3 }, (_, i) => Object.assign(element(), { id: `tab-${i + 1}` }));
  const panels = Array.from({ length: 3 }, element);
  const tablist = Object.assign(element(), { hidden: true, querySelectorAll: () => tabs });
  const group = { querySelector: () => tablist, querySelectorAll: () => panels };
  const heading = {}, image = {}, description = {}, close = element();
  const dialog = Object.assign(element(), { querySelector: (s) => ({ h2: heading, img: image, '#wireframe-dialog-description': description, '[data-close-dialog]': close })[s] });
  if (modal) dialog.showModal = () => { dialog.open = true; close.focus(); };
  dialog.close = () => { dialog.open = false; dialog.events.close(); };
  const trigger = Object.assign(element(), { hidden: true, dataset: { image: '/img/example.svg', alt: 'Review the order', title: 'Review', description: 'Check total before submission.' } });
  const document = { querySelectorAll: (s) => s === '[data-object-guides]' ? [group] : [trigger], querySelector: () => dialog };
  vm.runInNewContext(script, { document });
  return { tabs, panels, tablist, dialog, heading, image, description, close, trigger };
}
test('enhancement labels tabs and shows one guide without losing the others', () => {
  const f = fixture();
  assert.equal(f.tablist.hidden, false);
  assert.equal(f.tablist.attrs.role, 'tablist');
  assert.deepEqual(f.panels.map(p => p.hidden), [false, true, true]);
  assert.equal(f.panels[0].attrs['aria-labelledby'], 'tab-1');
  f.tabs[1].events.click();
  assert.deepEqual(f.panels.map(p => p.hidden), [true, false, true]);
  assert.equal(f.tabs[1].tabIndex, 0);
  assert.equal(f.tabs[0].attrs['aria-selected'], 'false');
});
test('arrow keys wrap and Home/End select and focus the matching guide', () => {
  const f = fixture(); let prevented = 0;
  function key(index, name) { f.tabs[index].events.keydown({ key: name, preventDefault() { prevented++; } }); }
  key(0, 'ArrowLeft'); assert.equal(f.panels[2].hidden, false); assert.equal(f.tabs[2].focused, true);
  key(2, 'ArrowRight'); assert.equal(f.panels[0].hidden, false);
  key(0, 'End'); assert.equal(f.panels[2].hidden, false);
  key(2, 'Home'); assert.equal(f.panels[0].hidden, false);
  key(0, 'Tab'); assert.equal(prevented, 4);
});
test('enlargement receives the selected screen and restores focus after close', () => {
  const f = fixture(); assert.equal(f.trigger.hidden, false);
  f.trigger.events.click();
  assert.equal(f.dialog.open, true); assert.equal(f.image.src, '/img/example.svg');
  assert.equal(f.image.alt, 'Review the order'); assert.equal(f.heading.textContent, 'Review');
  assert.equal(f.description.textContent, 'Check total before submission.');
  f.close.events.click(); assert.equal(f.dialog.open, false); assert.equal(f.trigger.focused, true);
});
test('unsupported dialogs retain inline wireframes and do not expose unusable enlargement', () => {
  const f = fixture({ modal: false }); assert.equal(f.trigger.hidden, true); assert.equal(f.tablist.hidden, false);
});
test('each public example contains three substantive guides and five referenced SVG screens', () => {
  const plans = require('../src/_data/designPlans.json'); assert.equal(plans.length, 3);
  for (const plan of plans) {
    assert.equal(plan.insights.length, 3); assert.equal(plan.objects.length, 3);
    assert.equal(plan.flows.length, 2); assert.equal(plan.flows.flatMap(f => f.steps).length, 5);
    for (const guide of plan.objects) for (const field of ['definition','instance','attributes','relationships','actions','states']) assert.ok(guide[field].length, `${plan.slug}: ${field}`);
    for (const step of plan.flows.flatMap(f => f.steps)) assert.ok(fs.existsSync(path.join(__dirname, '../src', step.image)), step.image);
  }
});

test('client deliverables connect requirements to goals and specify edge behavior and review decisions', () => {
  const plans = require('../src/_data/designPlans.json');
  for (const plan of plans) {
    assert.equal(plan.document.status, 'Draft for review');
    assert.ok(plan.document.decision.length);
    const goals = new Set(plan.goals.map(goal => goal.id));
    for (const requirement of plan.requirementDetails) {
      assert.ok(goals.has(requirement.goal));
      assert.ok(requirement.acceptance.length);
    }
    assert.deepEqual(plan.edgeStates.map(state => state.state), ['Empty', 'Loading', 'Error', 'Permission denied']);
    assert.ok(plan.openDecisions.length >= 1);
    assert.ok(plan.openDecisions.every(decision => decision.owner && decision.question));
    assert.ok(plan.outOfScope.length >= 1);
    assert.ok(plan.objects.every(object => object.rules.length >= 2));
  }
});
