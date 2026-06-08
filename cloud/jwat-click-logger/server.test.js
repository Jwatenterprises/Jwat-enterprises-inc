import assert from 'node:assert/strict';
import { test } from 'node:test';
import { cleanToken, partnerLinks } from './server.js';

test('cleanToken normalizes unsafe input', () => {
  assert.equal(cleanToken('ROK Financial!!'), 'rok-financial--');
  assert.equal(cleanToken('../bad'), '..-bad');
  assert.equal(cleanToken(''), 'unknown');
});

test('partner allowlist includes core JWAT lanes', () => {
  assert.ok(partnerLinks['rok-financial']);
  assert.ok(partnerLinks.gohighlevel);
  assert.ok(partnerLinks.upfirst);
  assert.ok(partnerLinks.nav);
  assert.ok(partnerLinks['tax-services']);
});
