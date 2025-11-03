import pandas as pd
import os

# Escape special characters for YAML
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    return "".join(html_escape_table.get(c, c) for c in str(text))

# Read publications.tsv
publications = pd.read_csv("publications.tsv", sep="\t", header=0)

# Generate markdown files
for _, item in publications.iterrows():
    md_filename = f"{item.pub_date}-{item.url_slug}.md"
    html_filename = f"{item.pub_date}-{item.url_slug}"

    md = f"---\ntitle: \"{item.title}\"\n"
    md += "collection: publications"
    md += f"\npermalink: /publication/{html_filename}"

    if pd.notna(item.get('category')):
        md += f"\ncategory: {item.category}"

    if len(str(item.get('author', ''))) > 0:
        md += f"\nauthor: '{html_escape(item.author)}'"

    if len(str(item.excerpt)) > 5:
        md += f"\nexcerpt: '{html_escape(item.excerpt)}'"

    md += f"\ndate: {item.pub_date}"
    md += f"\nvenue: '{html_escape(item.venue)}'"

    if len(str(item.paper_url)) > 5:
        md += f"\npaperurl: '{item.paper_url}'"

    md += f"\n---"

    # Markdown body
    md_body = []

    if len(str(item.paper_url)) > 5:
        md_body.append(f"<a href='{item.paper_url}'>Download paper here</a>")

    if len(str(item.excerpt)) > 5:
        md_body.append(html_escape(item.excerpt))

    # Combine YAML and body
    full_md = md + "\n\n" + "\n\n".join(md_body)

    output_path = os.path.join("../_publications", md_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_md)
