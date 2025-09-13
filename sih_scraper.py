# sih_scraper.py
# Requires: requests, beautifulsoup4, pandas
# Install: pip install requests beautifulsoup4 pandas

import re
import json
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://sih.gov.in/sih2025PS"
OUT_DIR = Path("sih_ps_output")
OUT_DIR.mkdir(exist_ok=True)

def fetch_page(url):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text

def split_sections(text):
    """
    Heuristic: Split on repeated 'Problem Statement ID' headings that occur
    before each statement details block on the page.
    """
    # Normalize whitespace
    txt = re.sub(r"\r\n|\r", "\n", text)
    # Find occurrences of "Problem Statement ID" and split keeping separators
    parts = re.split(r"(?=(?:Problem Statement ID))", txt)
    # First part may be header; ignore empty/intro chunk
    parts = [p.strip() for p in parts if p.strip()]
    return parts

def extract_fields(block):
    # Prepare a result dict with defaults
    r = {
        "ps_id": None,
        "title": None,
        "description": None,
        "background": None,
        "expected_solution": None,
        "organization": None,
        "department": None,
        "category": None,
        "theme": None,
        "youtube_link": None,
        "dataset_link": None,
        "contact_info": None,
        "raw_text": block.strip()
    }

    # Try extracting numeric ID: e.g., "Problem Statement ID\n\n25001"
    m = re.search(r"Problem Statement ID\s*[:\-\s]*\n*\s*([0-9]{4,6})", block)
    if m:
        r["ps_id"] = m.group(1).strip()

    # Title: typically "Problem Statement Title\n\n<Title>"
    m = re.search(r"Problem Statement Title\s*[:\-\s]*\n*\s*(.+?)(?:\n{2,}|Description|Background|Organization|Category)", block, flags=re.S)
    if m:
        r["title"] = m.group(1).strip()

    # Description: look for "Description" followed by text until "Background" or "Expected Solution" or "Organization"
    m = re.search(r"Description\s*\n+(.*?)(?=\n(?:Background|Expected Solution|Expected Outcomes|Organization|Department|Category))", block, flags=re.S)
    if m:
        r["description"] = ' '.join(line.strip() for line in m.group(1).splitlines() if line.strip())

    # Background
    m = re.search(r"Background\s*\n+(.*?)(?=\n(?:Expected Solution|Expected Outcomes|Organization|Description|Category))", block, flags=re.S)
    if m:
        r["background"] = ' '.join(line.strip() for line in m.group(1).splitlines() if line.strip())

    # Expected Solution / Expected Outcomes
    m = re.search(r"(?:Expected Solution|Expected Outcomes|Expected Outcomes\s*and\s*Deliverables)\s*\n+(.*?)(?=\n(?:Organization|Department|Category|Youtube Link|Dataset Link|Contact))", block, flags=re.S)
    if m:
        r["expected_solution"] = ' '.join(line.strip() for line in m.group(1).splitlines() if line.strip())

    # Organization / Department / Category / Theme
    m = re.search(r"Organization\s*(?:[:\-\s]*)\n*(.*?)\n{1,3}", block)
    if m:
        r["organization"] = m.group(1).strip()
    m = re.search(r"Department\s*(?:[:\-\s]*)\n*(.*?)\n{1,3}", block)
    if m:
        r["department"] = m.group(1).strip()
    m = re.search(r"Category\s*(?:[:\-\s]*)\n*(.*?)\n{1,3}", block)
    if m:
        r["category"] = m.group(1).strip()
    m = re.search(r"Theme\s*(?:[:\-\s]*)\n*(.*?)\n{1,3}", block)
    if m:
        r["theme"] = m.group(1).strip()

    # Links: youtube, dataset, contact
    m = re.search(r"YouTube Link\s*\[?.*?\]?\s*(https?://\S+)", block, flags=re.I)
    if m:
        r["youtube_link"] = m.group(1).strip()
    m = re.search(r"Dataset Link\s*\[?.*?\]?\s*(https?://\S+)", block, flags=re.I)
    if m:
        r["dataset_link"] = m.group(1).strip()
    m = re.search(r"Contact info\s*\[?.*?\]?\s*(https?://\S+|\S+@\S+|\+?\d[\d\s-]{7,})", block, flags=re.I)
    if m:
        r["contact_info"] = m.group(1).strip()

    return r

def write_outputs(records):
    # JSON
    with open(OUT_DIR / "sih_ps_all.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # CSV using pandas for robust quoting
    df = pd.DataFrame(records)
    df.to_csv(OUT_DIR / "sih_ps_all.csv", index=False)

    # Individual markdown files
    for rec in records:
        pid = rec.get("ps_id") or "unknown"
        safe_title = re.sub(r"[^\w\s-]", "", (rec.get("title") or "")).strip().replace(" ", "_")[:80]
        fname = OUT_DIR / f"{pid}_{safe_title}.md"
        with open(fname, "w", encoding="utf-8") as md:
            md.write(f"# {rec.get('title') or 'No title'}\n\n")
            md.write(f"**Problem Statement ID:** {pid}\n\n")
            if rec.get("organization"):
                md.write(f"**Organization:** {rec.get('organization')}\n\n")
            if rec.get("department"):
                md.write(f"**Department:** {rec.get('department')}\n\n")
            if rec.get("category"):
                md.write(f"**Category:** {rec.get('category')}\n\n")
            if rec.get("theme"):
                md.write(f"**Theme:** {rec.get('theme')}\n\n")
            md.write("## Description\n\n")
            md.write((rec.get("description") or "N/A") + "\n\n")
            if rec.get("background"):
                md.write("## Background\n\n")
                md.write(rec.get("background") + "\n\n")
            if rec.get("expected_solution"):
                md.write("## Expected Solution / Outcomes\n\n")
                md.write(rec.get("expected_solution") + "\n\n")
            if rec.get("youtube_link"):
                md.write(f"**YouTube Link:** {rec.get('youtube_link')}\n\n")
            if rec.get("dataset_link"):
                md.write(f"**Dataset Link:** {rec.get('dataset_link')}\n\n")
            if rec.get("contact_info"):
                md.write(f"**Contact:** {rec.get('contact_info')}\n\n")

def main():
    print("Fetching page:", URL)
    html = fetch_page(URL)
    soup = BeautifulSoup(html, "html.parser")

    # Get visible text for robust processing
    visible_text = soup.get_text("\n", strip=True)
    sections = split_sections(visible_text)
    print(f"Found approx {len(sections)} sections (including header chunks).")

    records = []
    for sec in sections:
        if "Problem Statement ID" not in sec:
            continue
        rec = extract_fields(sec)
        # Only keep if has an ID or title
        if rec["ps_id"] or rec["title"]:
            records.append(rec)

    print(f"Extracted {len(records)} problem statement(s). Writing outputs...")
    write_outputs(records)
    print("Done. Files in:", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
