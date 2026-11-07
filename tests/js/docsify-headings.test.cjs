"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const api = require("./docsify-headings.cjs");

test("slugs fold accents and keep only ASCII letters, digits, and single hyphens", () => {
  assert.equal(api.slug("Governança de decisão do portfólio"), "governanca-de-decisao-do-portfolio");
  assert.equal(api.slug("Pendências"), "pendencias");
  assert.equal(api.slug("  -Run make_check (now)!- "), "run-makecheck-now");
  assert.equal(api.slug("1. Intro"), "1-intro");
  assert.equal(api.slug("Two\nlines"), "two-lines");
  assert.equal(api.slug("«»"), "section");
});

test("plans number repeated slugs and never reuse an existing id", () => {
  assert.deepEqual(api.anchorPlan(["Pendências", "Pendências", "Pendencias"], []),
    ["pendencias", "pendencias-1", "pendencias-2"]);
  assert.deepEqual(api.anchorPlan(["Pendências", "Operations"], ["pendências", "operations"]),
    ["pendencias", null]);
  assert.deepEqual(api.anchorPlan(["Ação", "Ação"], ["acao-1"]), ["acao", null]);
});
