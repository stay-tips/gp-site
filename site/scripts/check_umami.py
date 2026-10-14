#!/usr/bin/env python3
"""Check the published tracker and the server configuration needed by heatmaps."""

import json
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen


class AnalyticsScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "script" and attributes.get("data-website-id"):
            self.scripts.append(attributes)


def check(page_url):
    with urlopen(page_url, timeout=20) as response:
        page = AnalyticsScripts()
        page.feed(response.read().decode())

    tracker = [s for s in page.scripts if urlsplit(s.get("src", "")).path == "/script.js"]
    recorder = [s for s in page.scripts if urlsplit(s.get("src", "")).path == "/recorder.js"]
    assert len(tracker) == 1, "Expected exactly one Umami pageview tracker"
    assert len(recorder) == 1, "Missing or duplicate Umami recorder.js: heatmaps cannot collect data"
    tracker, recorder = tracker[0], recorder[0]
    assert tracker["data-website-id"] == recorder["data-website-id"], "Website IDs differ"
    assert page.scripts.index(tracker) < page.scripts.index(recorder), "Tracker must precede recorder"
    assert "defer" in tracker and "defer" in recorder, "Both scripts must use defer"
    assert tracker.get("data-do-not-track") == "true", "Do Not Track must remain enabled"

    script_url = urljoin(page_url, recorder["src"])
    with urlopen(script_url, timeout=20) as response:
        assert "javascript" in response.headers.get("Content-Type", ""), "Recorder is not JavaScript"

    config_url = urljoin(script_url, f"/api/websites/{recorder['data-website-id']}/recorder")
    with urlopen(config_url, timeout=20) as response:
        config = json.load(response)
    assert config.get("enabled") is True, "Recorder disabled on Umami server"
    assert config.get("heatmapEnabled") is True, "Heatmaps disabled on Umami server"
    assert config.get("heatmapSampleRate", 0) > 0, "Heatmap sample rate is zero"
    print(f"PASS: tracker, recorder and heatmap configuration — {page_url}")


if __name__ == "__main__":
    for url in sys.argv[1:] or ["https://greenproperty.it/"]:
        check(url)
