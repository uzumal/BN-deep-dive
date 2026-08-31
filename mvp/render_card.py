#!/usr/bin/env python3
"""out/event.json + card.html → out/card.png (1200x630)"""
import json, glob
from pathlib import Path
from playwright.sync_api import sync_playwright

event = json.loads(Path("out/event.json").read_text(encoding="utf-8"))
html = Path("card.html").read_text(encoding="utf-8")
for k, v in event.items():
    html = html.replace("{{%s}}" % k, str(v))
Path("out/card_filled.html").write_text(html, encoding="utf-8")

candidates = glob.glob("/opt/pw-browsers/**/chrome", recursive=True) + \
             glob.glob("/opt/pw-browsers/**/headless_shell", recursive=True) + \
             ["/opt/pw-browsers/chromium"]
exe = next((c for c in candidates if Path(c).is_file()), None)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630})
    page.goto("file://" + str(Path("out/card_filled.html").resolve()))
    page.wait_for_timeout(400)
    page.screenshot(path="out/card.png")
    browser.close()
print("out/card.png written")
