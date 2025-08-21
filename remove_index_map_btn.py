"""
Utility script to remove Index Map buttons from pages other than the home page.

The supplementary materials include a green "Index Map" button linking back to
`evidence-central-index.html` on many module and task pages. The user has
requested that this button only appear on the home page (`index.html`). This
script scans all HTML files in the repository, excluding `index.html`, and
comments out the entire `<div>` block that contains the `index-map-btn`
anchor. Commenting out the block retains the code for future reference
without rendering it in the browser.

To run from the repository root:

    python Construction-Supplementary-material-main/Construction-Supplementary-material-main/remove_index_map_btn.py

After running, repackage the site to see the changes.
"""

import os
import re
from typing import List, Tuple


def remove_index_map_button(content: str) -> Tuple[str, bool]:
    """Wrap the index map button div in HTML comments if present.

    Searches for a `<div>` containing an `<a>` element with class
    `index-map-btn` and comments out that entire block. Uses a non-greedy
    pattern to avoid overmatching.

    Returns the modified content and a boolean indicating whether a change
    was made.
    """
    pattern = re.compile(
        r"<div[^>]*>\s*<a[^>]*class=\"index-map-btn\"[^>]*>.*?</a>\s*</div>",
        re.DOTALL,
    )
    matches = list(pattern.finditer(content))
    if not matches:
        return content, False
    def replacer(match: re.Match) -> str:
        return f"<!-- {match.group(0)} -->"
    new_content = pattern.sub(replacer, content)
    return new_content, True


def process_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, changed = remove_index_map_button(content)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
    return changed


def main() -> None:
    base_dir = os.path.dirname(__file__)
    updated_files: List[str] = []
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if not filename.lower().endswith(".html"):
                continue
            # Skip the home page (index.html) so it retains its button
            if filename == "index.html":
                continue
            path = os.path.join(root, filename)
            if process_file(path):
                updated_files.append(os.path.relpath(path, base_dir))
    print(f"Removed index map buttons from {len(updated_files)} file(s):")
    for uf in updated_files:
        print(f" - {uf}")


if __name__ == "__main__":
    main()