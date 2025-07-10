#!/usr/bin/env python3
"""Quick script to fix markdown formatting issues in the Personal MCP Server Sprint Plan
"""


def fix_markdown_formatting(file_path):
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    fixed_lines = []

    for i, line in enumerate(lines):
        # Add the current line
        fixed_lines.append(line)

        # Check if current line is a heading starting with ####
        if line.startswith("#### "):
            # Check if next line exists and is a list item
            if i + 1 < len(lines) and lines[i + 1].startswith("- ["):
                # Add a blank line between heading and list
                fixed_lines.append("")

        # Check if current line starts a deliverables list
        if line.endswith("**:") and i + 1 < len(lines) and lines[i + 1].startswith("- ["):
            # Add blank line before list
            fixed_lines.append("")

    # Write back the fixed content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(fixed_lines))

    print(f"Fixed markdown formatting in {file_path}")


if __name__ == "__main__":
    file_path = r"c:\Users\James\Documents\Github\GHrepos\Core-Framework\docs\Personal Ideas\Stage1-ConceptualDevelopment\ConceptualProjects\ModelContextProtocol\Personal-MCP-Server-Sprint-Plan.md"
    fix_markdown_formatting(file_path)
