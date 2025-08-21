"""
Utility script to fix misencoded arrow characters in HTML files.

The training materials include navigation links that use left and right arrow
symbols to indicate previous/next links. In some environments, these
Unicode characters were misinterpreted, resulting in sequences like
``â†`` and ``â†’`` appearing in the HTML. This script scans all HTML files
within the project and replaces those misencoded sequences with the
correct Unicode arrows.

To run this script from the repository root:

    python Construction-Supplementary-material-main/Construction-Supplementary-material-main/replace_misencoded_arrows.py

This will modify affected files in place.
"""

import os
from typing import Dict

# Mapping of misencoded sequences to correct Unicode characters.
# These sequences result when UTF-8 bytes for arrow characters are
# mistakenly interpreted as ISO-8859-1 (Latin-1). We restore them to
# proper arrows.
REPLACEMENTS: Dict[str, str] = {
    "â†": "←",  # Left arrow (U+2190)
    "â†’": "→",  # Right arrow (U+2192)
}


def replace_in_file(path: str) -> bool:
    """Replace misencoded arrows in a single file.

    Args:
        path: Path to the HTML file.

    Returns:
        True if the file was modified, False otherwise.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            original = file.read()
    except UnicodeDecodeError:
        # Skip binary files or files with encoding issues.
        return False

    modified = original
    for bad, good in REPLACEMENTS.items():
        modified = modified.replace(bad, good)

    if modified != original:
        with open(path, "w", encoding="utf-8") as file:
            file.write(modified)
        return True
    return False


def main() -> None:
    base_dir = os.path.dirname(__file__)
    updated = 0
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.lower().endswith(".html"):
                path = os.path.join(root, filename)
                if replace_in_file(path):
                    updated += 1
    print(f"Replaced misencoded arrows in {updated} file(s).")


if __name__ == "__main__":
    main()