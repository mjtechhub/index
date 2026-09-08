#!/usr/bin/env python3
"""
MJ Tech Hub - Safe Tutorial Migration Script
Removes literal '\\n' artifacts and normalizes script inclusions across tutorials.
"""

from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
TUTORIALS_DIR = REPO_ROOT / "tutorials" / "networking"

def migrate_tutorials():
    if not TUTORIALS_DIR.exists():
        print(f"Directory not found: {TUTORIALS_DIR}")
        return False

    html_files = sorted(list(TUTORIALS_DIR.glob("*.html")))
    print(f"Found {len(html_files)} tutorial files to inspect...")

    modified_count = 0
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Replace literal '\n' artifact when between script tags
        # Pattern: <script src="../../js/components.js"></script>\n    <script src="../../js/tutorial.js"></script>
        content = re.sub(
            r'<script src=[\"\']\.\./\.\./js/components\.js[\"\']></script>\\n\s*<script src=[\"\']\.\./\.\./js/tutorial\.js[\"\']></script>',
            '    <script src="../../js/components.js"></script>\n    <script src="../../js/tutorial.js"></script>',
            content
        )

        # General check for any remaining literal '\n' inside script tags
        content = content.replace(r"\n    <script", "\n    <script")
        content = content.replace(r"\n<script", "\n<script")

        # In case literal \n is anywhere in text before </body>
        if r"\n" in content:
            # Check if there is still a literal \n
            content = re.sub(r'\\n\s*', '\n', content)

        if content != original_content:
            with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
            modified_count += 1

    print(f"Migration completed. Modified {modified_count} of {len(html_files)} files.")

    # Verify no literal '\n' remains
    remaining_errors = []
    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            if r"\n" in f.read():
                remaining_errors.append(file_path.name)

    if remaining_errors:
        print(f"FAILED: {len(remaining_errors)} files still have literal '\\n': {remaining_errors}")
        return False
    else:
        print("PASS: All tutorial files have zero literal '\\n' artifacts.")
        return True

if __name__ == "__main__":
    success = migrate_tutorials()
    exit(0 if success else 1)
