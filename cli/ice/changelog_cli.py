import argparse
from datetime import date

from engine.toolbox.changelog import collect_changes, build_changelog, render_markdown

def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate changelog from git history.")
    parser.add_argument("--from", dest="from_ref", required=True, help="Base ref (tag/branch/commit)")
    parser.add_argument("--to", dest="to_ref", default="HEAD", help="Target ref (default: HEAD)")
    parser.add_argument("--version", required=True, help="Release version (e.g. 0.4.0)")
    parser.add_argument("--date", default=None, help="Release date (YYYY-MM-DD, default: today)")
    parser.add_argument("--append-file", default="CHANGELOG.md", help="File to append to (default: CHANGELOG.md)")
    args = parser.parse_args(argv)

    d = args.date or str(date.today())

    items = collect_changes(args.from_ref, args.to_ref)
    ch = build_changelog(args.version, d, items)
    md = render_markdown(ch)

    # Append in testa al file
    try:
        with open(args.append_file, "r", encoding="utf-8") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = "# Changelog\n\n"

    with open(args.append_file, "w", encoding="utf-8") as f:
        f.write(existing.rstrip() + "\n\n" + md)

    print(md)