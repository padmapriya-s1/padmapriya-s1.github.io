# coding: utf-8
"""
Publications markdown generator for academicpages (modified)

Takes a TSV of publications with metadata and converts them for use with
academicpages.github.io. This script is based on the original notebook but
modified to:
  - Support a `category` field in the TSV (e.g. conference, manuscripts, preprints)
  - Put `collection: publications` in the YAML and set `category` from TSV
  - Replace the "Recommended citation" text with the abstract (excerpt)
  - Render DOI as a blue clickable link below the title (in the page body)
  - Show author names below the title (uses `authors` column if present, else
    extracts authors from the `citation` field)

Expected TSV columns (at minimum):
  pub_date, url_slug, title, venue, citation
Optional/commonly-used columns:
  excerpt, paper_url, site_url, category, authors, published

Usage:
  place `publications.tsv` in the same folder and run this script. It will
  write .md files to ../_publications/ (same default as the original script).

Note: the Jekyll layout may need small tweaks to render fields exactly how you
want; this script focuses on the generated markdown.
"""

import os
import pandas as pd

# ---- Helper: HTML escape for YAML/body content ----
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce HTML entities for some problematic characters.
    If input isn't a str, it will be converted.
    """
    if pd.isna(text):
        return ""
    text = str(text)
    return "".join(html_escape_table.get(c, c) for c in text)

# ---- Read TSV ----
publications = pd.read_csv("publications.tsv", sep="\t", header=0, dtype=str)

# Ensure columns exist (avoid KeyError later)
required = ["pub_date", "url_slug", "title", "venue", "citation"]
for col in required:
    if col not in publications.columns:
        raise SystemExit(f"Required column '{col}' missing from publications.tsv")

# Fill NaN with empty strings to simplify checks
publications = publications.fillna("")

# ---- Create markdown files ----
out_dir = os.path.join("..", "_publications")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

for row, item in publications.iterrows():
    # Basic file names
    md_filename = f"{item.pub_date}-{item.url_slug}.md"
    html_filename = f"{item.pub_date}-{item.url_slug}"

    # Start YAML front matter
    md_lines = []
    md_lines.append("---")
    # Title (keep as-is but escape quotes)
    md_lines.append(f'title: "{html_escape(item.title)}"')

    # Collection and category
    # If the TSV has a `category` column and it's non-empty, use it; else default to 'manuscripts'
    category_value = item.get("category", "").strip()
    if category_value:
        md_lines.append("collection: publications")
        md_lines.append(f"category: {html_escape(category_value)}")
    else:
        md_lines.append("collection: publications")
        md_lines.append("category: manuscripts")

    # Permalink
    md_lines.append(f"permalink: /publication/{html_filename}")

    # excerpt (used by theme lists) - store raw excerpt in YAML (escaped)
    if len(item.get("excerpt", "").strip()) > 0:
        md_lines.append(f"excerpt: '{html_escape(item.excerpt)}'")

    # date and venue
    md_lines.append(f"date: {item.pub_date}")
    md_lines.append(f"venue: '{html_escape(item.venue)}'")

    # paperurl (usually DOI or arXiv URL)
    if len(item.get("paper_url", "").strip()) > 0:
        md_lines.append(f"paperurl: '{item.paper_url}'")

    # keep citation in YAML for reference (escaped)
    if len(item.get("citation", "").strip()) > 0:
        md_lines.append(f"citation: '{html_escape(item.citation)}'")

    # optional published flag
    if "published" in item and str(item.published).strip().lower() in ["true", "false"]:
        md_lines.append(f"published: {str(item.published).strip().lower()}")

    md_lines.append("---\n")

    # ---- Body content ----
    # We'll show DOI (paper_url) as a blue clickable link, authors below title, then abstract.
    body_lines = []

    # DOI - show as blue link if paper_url present
    if len(item.get("paper_url", "").strip()) > 0:
        # Use a common Google-like link color for blue; the actual site CSS may override this.
        doi = item.paper_url.strip()
        body_lines.append(f"**DOI:** <a href='{doi}' style='color:#1a0dab;'>{doi}</a>\n")

    # Authors - prefer an explicit 'authors' column; otherwise extract from citation before first '(' character
    authors_text = ""
    if len(item.get("authors", "").strip()) > 0:
        authors_text = item.authors.strip()
    else:
        # crude extraction: take everything before the first '(' which commonly starts the year
        cit = item.get("citation", "").strip()
        if cit:
            authors_text = cit.split("(")[0].strip()

    if authors_text:
        # keep authors unescaped for readability but run html_escape to be safe in YAML/body
        body_lines.append(f"**Authors:** {html_escape(authors_text)}\n")

    # Abstract (excerpt) - place under a heading
    if len(item.get("excerpt", "").strip()) > 0:
        body_lines.append("### Abstract\n\n" + html_escape(item.excerpt).strip() + "\n")

    # Optional: keep a download link at top if paper_url exists
    if len(item.get("paper_url", "").strip()) > 0:
        doi = item.paper_url.strip()
        body_lines.insert(0, f"<a href='{doi}'>Download paper here</a>\n")

    # Combine YAML + body
    md = "\n".join(md_lines) + "\n" + "\n".join(body_lines)

    # Write file
    safe_md_filename = os.path.basename(md_filename)
    out_path = os.path.join(out_dir, safe_md_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

print(f"Wrote {len(publications)} publication(s) to {out_dir}")
