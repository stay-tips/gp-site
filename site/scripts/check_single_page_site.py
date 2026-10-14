#!/usr/bin/env python3
"""Check the built site before rsync removes the retired sections in production."""
import json
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


root = Path(sys.argv[1]).resolve()
origin = "https://greenproperty.it/"
required = {"index.html", "grazie/index.html", "privacy-policy/index.html", "terms/index.html", "404.html"}
# This legal draft may exist in the developer's working tree; it is not a legacy section.
allowed = required | {"cancellazione-dati/index.html"}
published = {str(path.relative_to(root)) for path in root.rglob("*.html")}
assert required <= published, f"Missing pages: {required - published}"
assert published <= allowed, f"Unexpected published pages: {published - allowed}"
for retired in ("index.json", "index.xml", "en", "advantages", "blog", "project", "booking", "team", "search", "values", "contact", "tags", "categories"):
    assert not (root / retired).exists(), f"Retired output still present: {retired}"

pages = {name: Page((root / name).read_text()) for name in published}
home = pages["index.html"]
forms = [attrs for tag, attrs in home.tags if tag == "form"]
assert len(forms) == 2 and all(attrs.get("action") == "/api/leads" for attrs in forms)
assert {attrs.get("id") for attrs in forms} == {"gp-form-1", "gp-form-2"}
assert sum(tag == "h1" for tag, _ in home.tags) == 1
canonical = [attrs["href"] for tag, attrs in home.tags if tag == "link" and attrs.get("rel") == "canonical"]
assert canonical == [origin], canonical
assert any(attrs.get("id") == "modulo" for _, attrs in home.tags)
assert not any(attrs.get("hreflang") == "en" for _, attrs in home.tags)
assert "Case study" not in (root / "index.html").read_text()
scripts = [attrs["src"] for tag, attrs in home.tags if tag == "script" and "src" in attrs]
tracker = "https://stats.greenproperty.it/script.js"
recorder = "https://stats.greenproperty.it/recorder.js"
assert scripts.count(tracker) == scripts.count(recorder) == 1
assert scripts.index(tracker) < scripts.index(recorder)
form_script = next(src for src in scripts if "landing-form" in src)
form_source = (root / urlsplit(form_script).path.lstrip("/")).read_text()
assert "/grazie/" in form_source and "/advantages/" not in form_source
definition = json.loads((Path(__file__).resolve().parents[2] / "deploy/umami-funnel.json").read_text())
assert definition["parameters"]["steps"][0] == {"type": "path", "value": "/"}
for step in definition["parameters"]["steps"][1:]:
    assert step["value"] in form_source

for name, page in pages.items():
    page_url = urljoin(origin, name.removesuffix("index.html"))
    base = next((attrs["href"] for tag, attrs in page.tags if tag == "base"), page_url)
    for tag, attrs in page.tags:
        assert not (tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh"), f"Redirect in {name}"
        for attribute in ("href", "src", "action"):
            if not attrs.get(attribute):
                continue
            target = urlsplit(urljoin(base, attrs[attribute]))
            if target.scheme not in ("http", "https") or target.netloc != "greenproperty.it":
                continue
            if target.path == "/api/leads":
                continue
            local = root / unquote(target.path).lstrip("/")
            if local.is_dir():
                local /= "index.html"
            assert local.is_file(), f"Broken {attribute} in {name}: {attrs[attribute]}"
            if target.fragment and local.suffix == ".html":
                destination = pages[str(local.relative_to(root))]
                assert any(a.get("id") == unquote(target.fragment) for _, a in destination.tags), f"Missing anchor: {attrs[attribute]}"

thank_you = pages["grazie/index.html"]
assert any(tag == "meta" and attrs.get("name") == "robots" and "noindex" in attrs.get("content", "") for tag, attrs in thank_you.tags)
sitemap = ET.parse(root / "sitemap.xml")
locations = {node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
expected = {origin, origin + "privacy-policy/", origin + "terms/"}
if "cancellazione-dati/index.html" in published:
    expected.add(origin + "cancellazione-dati/")
assert locations == expected, f"Unexpected sitemap: {locations}"
llms = (root / "llms.txt").read_text()
for retired in ("/advantages/", "/booking/", "/blog/", "/project/", "/search/", "/en/"):
    assert retired not in llms
print(f"PASS: {len(published)} HTML pages, root landing, direct forms, legal links, sitemap, no legacy routes or redirects")
