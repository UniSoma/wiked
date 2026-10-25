"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const api = require("./docsify-example.cjs");

test("opt-in and associations are explicit, stable, and unambiguous", () => {
  assert.equal(api.diagramID("wiked-diagram=process"), "process");
  assert.equal(api.diagramID("process.svg"), null);
  assert.equal(api.diagramID("wiked-diagram=Process"), null);
  assert.equal(api.diagramID("wiked-diagram=process&wiked-diagram=other"), null);
  assert.deepEqual(api.association("process.svg#wiked-node=team.receive&section=step_receive"),
    { node: "team.receive", section: "step_receive" });
  for (const value of ["#wiked-node=receive", "#wiked-node=receive&section=step&section=other",
    "#wiked-node=receive&section=step&extra=x", "#wiked-node=Bad&section=step"]) {
    assert.equal(api.association(value), null);
  }
});

test("authored paths match independently of the hash router", () => {
  assert.equal(api.assetKey("../assets/process.svg#wiked-diagram=process"),
    api.assetKey("../assets/process.svg#wiked-node=receive&section=step_receive"));
  assert.notEqual(api.assetKey("one.svg"), api.assetKey("two.svg"));
  assert.equal(api.sourceURL("/wiki/team/process.svg#flow", "https://example.test/viewer/index.html"),
    "https://example.test/wiki/team/process.svg");
  for (const value of ["https://other.test/process.svg", "data:image/svg+xml,test", "/secret.html",
    "https://user:pass@example.test/process.svg"]) {
    assert.throws(() => api.sourceURL(value, "https://example.test/"));
  }
});

test("CSS resource checks reject external and obfuscated resources", () => {
  assert.equal(api.safeCSS(".node {fill: url(#gradient)}"), true);
  assert.equal(api.safeCSS('@font-face{src:url("data:application/font-woff;base64,YWJj")}'), true);
  for (const value of ["url(https://other.test/x)", "@import 'evil.css'", "url(//other.test/x)",
    "u\\72l(https://other.test)", "url(/* comment */evil)", "expression(alert(1))"]) {
    assert.equal(api.safeCSS(value), false);
  }
});

// A deliberately small DOM model exercises adapter control flow, not browser
// rendering or XML parsing. Real Docsify/browser coverage is a separate opt-in.
class Element {
  constructor(tag, attrs = {}, children = []) {
    this.localName = tag;
    this.namespaceURI = "http://www.w3.org/2000/svg";
    this.attrs = { ...attrs };
    this.children = [];
    this.style = {};
    this.listeners = {};
    this.textContent = "";
    this.append(...children);
  }
  get attributes() {
    return Object.entries(this.attrs).map(([name, value]) => ({ name, value, localName: name.split(":").pop() }));
  }
  get id() { return this.attrs.id; }
  get src() { return this.attrs.src; }
  get alt() { return this.attrs.alt; }
  getAttribute(name) { return this.attrs[name] ?? null; }
  setAttribute(name, value) { this.attrs[name] = value; }
  hasAttribute(name) { return name in this.attrs; }
  removeAttribute(name) { delete this.attrs[name]; }
  append(...children) {
    for (const child of children) { child.parent = this; this.children.push(child); }
  }
  after(sibling) {
    sibling.parent = this.parent;
    this.parent.children.splice(this.parent.children.indexOf(this) + 1, 0, sibling);
  }
  remove() { this.parent.children = this.parent.children.filter(child => child !== this); }
  attachShadow() { this.shadowRoot = new Element("shadow"); return this.shadowRoot; }
  contains(element) { return this === element || this.children.some(child => child.contains(element)); }
  closest(tag) { return this.localName === tag ? this : this.parent?.closest(tag) || null; }
  querySelectorAll(selector) {
    const match = node => selector === "*" ||
      (selector === "g[class]" && node.localName === "g" && node.hasAttribute("class")) ||
      (selector === "[id]" && node.hasAttribute("id")) ||
      (selector === "[data-wiked-diagram]" && node.hasAttribute("data-wiked-diagram")) ||
      (selector === "[data-wiked-diagram-open]" && node.hasAttribute("data-wiked-diagram-open")) ||
      (selector === "img[data-origin]" && node.localName === "img" && node.hasAttribute("data-origin")) ||
      (selector === "a[href]" && node.localName === "a" && node.hasAttribute("href"));
    return this.children.flatMap(child => [...(match(child) ? [child] : []), ...child.querySelectorAll(selector)]);
  }
  addEventListener(type, handler, options = {}) {
    (this.listeners[type] ||= []).push({ handler, signal: options.signal });
  }
  fire(type, overrides = {}) {
    const event = { type, button: 0, preventDefault() { this.prevented = true; }, stopPropagation() {}, ...overrides };
    for (const listener of this.listeners[type] || []) {
      if (!listener.signal?.aborted) listener.handler(event);
    }
    return event;
  }
  scrollIntoView() { this.scrolled = (this.scrolled || 0) + 1; }
  focus() { this.focused = true; }
}

function svgNode(id) {
  return new Element("g", { class: Buffer.from(id).toString("base64") }, [new Element("rect", { x: "12", width: "160" })]);
}

function xmlDocument(svg) {
  return { documentElement: svg, querySelector: () => null };
}

function documentModel(svg) {
  return {
    defaultView: { DOMParser: class { parseFromString() { return xmlDocument(svg); } } },
    importNode: value => value,
    createElement: tag => new Element(tag),
    baseURI: "https://example.test/viewer/index.html",
  };
}

test("SVG rejection checks active content, event handlers, namespaces and resources", () => {
  const svg = new Element("svg", {}, [svgNode("receive")]);
  assert.equal(api.prepareSVG("<svg/>", documentModel(svg)), svg);
  for (const child of [new Element("script"), new Element("foreignObject"),
    new Element("g", { onclick: "evil()" }), new Element("image", { href: "https://other.test/x.png" }),
    new Element("g", { "xml:base": "https://other.test" }), new Element("animate")]) {
    assert.throws(() => api.prepareSVG("<svg/>", documentModel(new Element("svg", {}, [child]))));
  }
  const foreign = new Element("div");
  foreign.namespaceURI = "http://www.w3.org/1999/xhtml";
  assert.throws(() => api.prepareSVG("<svg/>", documentModel(new Element("svg", {}, [foreign]))));
  assert.throws(() => api.prepareSVG("<!DOCTYPE svg><svg/>", documentModel(svg)));
  assert.throws(() => api.prepareSVG("x".repeat(4 * 1024 * 1024 + 1), documentModel(svg)));
});

test("node lookup uses stable source keys, tolerates padding, and rejects ambiguity", () => {
  const node = svgNode("receive");
  const svg = new Element("svg", {}, [node]);
  assert.equal(api.findNode(svg, "receive", btoa), node);
  node.setAttribute("class", btoa("receive").replace(/=+$/, ""));
  assert.equal(api.findNode(svg, "receive", btoa), node);
  assert.throws(() => api.findNode(svg, "missing", btoa));
  svg.append(svgNode("receive"));
  assert.throws(() => api.findNode(svg, "receive", btoa));
});

function entry(name = "process", node = "receive", section = "step_receive") {
  const image = new Element("img", {
    "data-origin": `${name}.svg`, title: `wiked-diagram=${name}`,
    src: `https://example.test/wiki/team/${name}.svg`, alt: "Process flow",
  });
  const target = new Element("a", { id: section });
  const link = new Element("a", { href: `${name}.svg#wiked-node=${node}&section=${section}` });
  return { image, target, link, children: [image, target, link] };
}

async function withPlugin(content, fetcher, run) {
  const previousWindow = global.window;
  const previousFetch = global.fetch;
  const warn = console.warn;
  const warnings = [];
  const document = documentModel(new Element("svg", {}, [svgNode("receive"), svgNode("receive_again")]));
  document.querySelector = () => content;
  global.window = { document, btoa };
  global.fetch = fetcher;
  console.warn = message => warnings.push(message);
  const hooks = {};
  api.plugin({ beforeEach: callback => { hooks.before = callback; }, doneEach: callback => { hooks.done = callback; } }, {});
  try { await run(hooks, document, warnings); }
  finally { global.window = previousWindow; global.fetch = previousFetch; console.warn = warn; }
}

const response = async () => ({ ok: true, text: async () => "<svg/>" });

function originalLinks(content) {
  return content.querySelectorAll("[data-wiked-diagram]")
    .flatMap(host => host.shadowRoot.querySelectorAll("[data-wiked-diagram-open]"));
}

test("original link uses the validated resolved SVG URL and preserves native actions", async () => {
  const first = entry();
  first.image.setAttribute("src", "https://example.test/wiki/nested/assets/process.svg?v=2#ignored");
  const content = new Element("main", {}, first.children);
  await withPlugin(content, response, async hooks => {
    await hooks.done();
    const [link] = originalLinks(content);
    assert.equal(originalLinks(content).length, 1);
    assert.equal(link.localName, "a");
    assert.equal(link.getAttribute("href"), "https://example.test/wiki/nested/assets/process.svg?v=2");
    assert.equal(link.getAttribute("data-wiked-diagram-open"), "process");
    assert.equal(link.textContent, "Open original diagram");
    assert.equal(link.hasAttribute("target"), false);
    for (const modifiers of [{}, { ctrlKey: true }, { metaKey: true }, { button: 1 }]) {
      assert.notEqual(link.fire("click", modifiers).prevented, true);
    }
    assert.notEqual(link.fire("keydown", { key: "Enter" }).prevented, true);
  });
});

test("enhancement supports both directions, keyboard and repeated occurrences without redraw", async () => {
  const first = entry();
  const second = new Element("a", { href: "process.svg#wiked-node=receive_again&section=step_receive" });
  const content = new Element("main", {}, [...first.children, second]);
  await withPlugin(content, response, async (hooks, document, warnings) => {
    await hooks.done();
    assert.equal(first.image.hidden, true);
    const host = content.querySelectorAll("[data-wiked-diagram]")[0];
    const svg = host.shadowRoot.children[1];
    const node = api.findNode(svg, "receive", btoa);
    const again = api.findNode(svg, "receive_again", btoa);
    node.fire("click");
    assert.equal(first.target.scrolled, 1);
    node.fire("keydown", { key: "Enter" });
    assert.equal(first.target.scrolled, 2);
    node.fire("keydown", { key: "Escape" });
    assert.equal(first.target.scrolled, 2);
    first.link.fire("click");
    second.fire("click");
    assert.equal(node.scrolled, 1);
    assert.equal(again.scrolled, 1);
    assert.equal(node.children[0].getAttribute("width"), "160");
    assert.equal(node.children[0].getAttribute("x"), "12");
    assert.deepEqual(warnings, []);
  });
});

test("different diagrams may reuse the same source node key", async () => {
  const first = entry("one");
  const second = entry("two", "receive", "step_other");
  const content = new Element("main", {}, [...first.children, ...second.children]);
  await withPlugin(content, response, async (hooks, document) => {
    // Simulate a separately parsed SVG per request, as the real DOMParser does.
    document.defaultView.DOMParser = class {
      parseFromString() { return xmlDocument(new Element("svg", {}, [svgNode("receive")])); }
    };
    await hooks.done();
    const hosts = content.querySelectorAll("[data-wiked-diagram]");
    assert.equal(hosts.length, 2);
    assert.deepEqual(originalLinks(content).map(link => link.getAttribute("href")),
      [first.image.src, second.image.src]);
    first.link.fire("click");
    second.link.fire("click");
    assert.equal(hosts[0].shadowRoot.children[1].children[0].scrolled, 1);
    assert.equal(hosts[1].shadowRoot.children[1].children[0].scrolled, 1);
  });
});

test("reopening rebuilds once and aborts old link handlers", async () => {
  const first = entry();
  const content = new Element("main", {}, first.children);
  await withPlugin(content, response, async (hooks, document) => {
    document.defaultView.DOMParser = class {
      parseFromString() { return xmlDocument(new Element("svg", {}, [svgNode("receive")])); }
    };
    await hooks.done();
    hooks.before("new entry");
    await hooks.done();
    const hosts = content.querySelectorAll("[data-wiked-diagram]");
    assert.equal(hosts.length, 1);
    assert.equal(originalLinks(content).length, 1);
    first.link.fire("click");
    assert.equal(hosts[0].shadowRoot.children[1].children[0].scrolled, 1);
  });
});

test("stale SVG loads cannot enhance an entry after navigation", async () => {
  const first = entry();
  const content = new Element("main", {}, first.children);
  let release;
  const pending = new Promise(resolve => { release = resolve; });
  await withPlugin(content, () => pending, async hooks => {
    const completion = hooks.done();
    hooks.before("other entry");
    release(await response());
    await completion;
    assert.equal(content.querySelectorAll("[data-wiked-diagram]").length, 0);
    assert.equal(originalLinks(content).length, 0);
    assert.notEqual(first.image.hidden, true);
  });
});

test("failed requests preserve static images and expose a diagnostic", async () => {
  const first = entry();
  const content = new Element("main", {}, first.children);
  await withPlugin(content, async () => ({ ok: false, status: 404 }), async (hooks, document, warnings) => {
    await hooks.done();
    assert.notEqual(first.image.hidden, true);
    assert.match(first.image.getAttribute("data-wiked-error"), /404/);
    assert.equal(content.querySelectorAll("[data-wiked-diagram]").length, 0);
    assert.equal(originalLinks(content).length, 0);
    assert.equal(warnings.length, 1);
  });
});

test("unmarked static images never gain original links", async () => {
  const first = entry();
  first.image.removeAttribute("title");
  const content = new Element("main", {}, first.children);
  await withPlugin(content, async () => { throw new Error("Unexpected fetch"); }, async hooks => {
    await hooks.done();
    assert.equal(originalLinks(content).length, 0);
    assert.notEqual(first.image.hidden, true);
    assert.equal(first.image.hasAttribute("data-wiked-error"), false);
  });
});

test("an older successful response cannot duplicate a newer generation's original link", async () => {
  const first = entry();
  const content = new Element("main", {}, first.children);
  let release;
  const pending = new Promise(resolve => { release = resolve; });
  let calls = 0;
  await withPlugin(content, () => ++calls === 1 ? pending : response(), async hooks => {
    const old = hooks.done();
    await hooks.done();
    const [link] = originalLinks(content);
    release(await response());
    await old;
    assert.deepEqual(originalLinks(content), [link]);
    assert.equal(first.image.hidden, true);
  });
});

test("originally hidden images keep the original link hidden across rebuilds and failure", async () => {
  const first = entry();
  first.image.hidden = true;
  const content = new Element("main", {}, first.children);
  let fail = false;
  await withPlugin(content, async () => fail ? { ok: false, status: 404 } : response(), async hooks => {
    for (let repeat = 0; repeat < 2; repeat++) {
      await hooks.done();
      const [host] = content.querySelectorAll("[data-wiked-diagram]");
      assert.equal(host.hidden, true);
      assert.equal(host.style.display, "none");
      assert.equal(originalLinks(content).length, 1);
    }
    fail = true;
    await hooks.done();
    assert.equal(first.image.hidden, true);
    assert.equal(originalLinks(content).length, 0);
  });
});

test("failed rebuild removes the old original link and restores the static fallback", async () => {
  const first = entry();
  const content = new Element("main", {}, first.children);
  let fail = false;
  await withPlugin(content, async () => {
    if (fail) throw new Error("Network failure");
    return response();
  }, async hooks => {
    await hooks.done();
    assert.equal(originalLinks(content).length, 1);
    fail = true;
    await hooks.done();
    assert.equal(originalLinks(content).length, 0);
    assert.equal(first.image.hidden, false);
    assert.equal(first.image.hasAttribute("data-wiked-original-hidden"), false);
  });
});

test("rejected URLs, SVG content and associations never publish original links", async () => {
  for (const failure of ["url", "svg", "association"]) {
    const first = entry();
    if (failure === "url") first.image.setAttribute("src", "https://other.test/process.svg");
    if (failure === "association") first.link.removeAttribute("href");
    const content = new Element("main", {}, first.children);
    await withPlugin(content, response, async (hooks, document, warnings) => {
      if (failure === "svg") document.defaultView.DOMParser = class {
        parseFromString() { return xmlDocument(new Element("svg", {}, [new Element("script")])); }
      };
      await hooks.done();
      assert.notEqual(first.image.hidden, true);
      assert.equal(originalLinks(content).length, 0);
      assert.equal(warnings.length, 1);
    });
  }
});
