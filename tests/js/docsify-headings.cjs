"use strict";
const { readFileSync } = require("node:fs");
const { join } = require("node:path");

// Exercise the single resolver embedded in the distributed HTML example.
const html = readFileSync(join(__dirname, "../../distr/agents/skills/wiked/viewers/index.html"), "utf8");
const scripts = [...html.matchAll(/<script id="wiked-docsify-headings">([\s\S]*?)<\/script>/g)];
if (scripts.length !== 1) throw new Error("Expected exactly one inline heading resolver");
const resolver = { exports: {} };
new Function("module", scripts[0][1])(resolver);
module.exports = resolver.exports;
