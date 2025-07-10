#!/usr/bin/env python3
"""Bulk fix script for common Pylance issues."""

import os
import re


def fix_logging_format(content: str) -> str:
    """Fix f-string logging to use lazy % formatting."""
    # Pattern to match logger.info(f"...{var}...") and similar
    patterns = [
        (r'logger\.(\w+)\(f"([^"]*?)"\)', r'logger.\1("\2")'),
        (r"logger\.(\w+)\(f\'([^\']*?)\'\)", r'logger.\1("\2")'),
    ]

    for pattern, _replacement in patterns:
        # Find all f-string logging calls
        matches = re.finditer(pattern, content)
        for match in reversed(list(matches)):
            log_level = match.group(1)
            message = match.group(2)

            # Extract variables from {var} patterns
            var_pattern = r"\{([^}]+)\}"
            variables = re.findall(var_pattern, message)

            if variables:
                # Replace {var} with %s
                new_message = re.sub(var_pattern, "%s", message)
                # Build the replacement
                var_list = ", ".join(variables)
                new_call = f'logger.{log_level}("{new_message}", {var_list})'

                # Replace in content
                start, end = match.span()
                content = content[:start] + new_call + content[end:]

    return content


def fix_exception_handling(content: str) -> str:
    """Fix exception handling to use 'from e' pattern."""
    patterns = [
        (
            r"except Exception as e:\s*\n(\s+)([^\n]*raise [^\n]*Error[^\n]*)\n",
            r"except Exception as e:\n\1\2 from e\n",
        ),
        (
            r"except FileNotFoundError:\s*\n(\s+)([^\n]*raise [^\n]*Error[^\n]*)\n",
            r"except FileNotFoundError as exc:\n\1\2 from exc\n",
        ),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    return content


def fix_unused_variables(content: str) -> str:
    """Fix unused variables by prefixing with underscore."""
    # This is a simple fix - in practice you'd want more sophisticated analysis
    lines = content.split("\n")
    for _i, line in enumerate(lines):
        # Look for simple assignment patterns that might be unused
        if " = " in line and not line.strip().startswith("#"):
            # This is a simplified approach - real implementation would need AST analysis
            pass
    return content


def fix_import_paths(content: str, file_path: str) -> str:
    """Fix import paths to use proper relative imports."""
    if "test_" in file_path or file_path.endswith("_test.py"):
        # Add sys.path fix for test files
        if "import sys" not in content and "from core." in content:
            import_section = 'import sys\nsys.path.insert(0, os.path.join(os.path.dirname(__file__), "blackbox-task-manager", "src"))\n\n'

            # Find the first import line
            lines = content.split("\n")
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    insert_pos = i
                    break

            if insert_pos > 0:
                lines.insert(insert_pos, import_section)
                content = "\n".join(lines)

    return content


def fix_file_encoding(content: str) -> str:
    """Fix file operations to include encoding."""
    patterns = [
        (r"open\(([^,)]+)\)", r'open(\1, encoding="utf-8")'),
        (r'open\(([^,)]+),\s*"([rwa]+)"\)', r'open(\1, "\2", encoding="utf-8")'),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content


def process_file(file_path: str) -> bool:
    """Process a single file and apply fixes."""
    try:
        with open(file_path, encoding="utf-8") as f:
            original_content = f.read()

        content = original_content

        # Apply fixes
        content = fix_logging_format(content)
        content = fix_exception_handling(content)
        content = fix_import_paths(content, file_path)
        content = fix_file_encoding(content)

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes: {file_path}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main function to process all Python files."""
    # Add specific files that need fixing
    target_files = [
        "test_task_manager_with_logging.py",
        "final_pylance_verification_test.py",
        "pylance_issues_action_plan.py",
        "comprehensive_edge_case_tests.py",
        "blackbox-task-manager/test_task_manager_manual.py",
        "blackbox-task-manager/test_connection_pool.py",
        "blackbox-task-manager/test_full_logging.py",
        "test_database_integration.py",
        "test_comprehensive_logging.py",
        "final_logging_verification.py",
        "test_enhanced_logging.py",
        "test_task_manager_comprehensive.py",
    ]

    print(f"Starting bulk fixes for {len(target_files)} files...")

    fixed_count = 0
    for file_path in target_files:
        print(f"Checking: {file_path}")
        if os.path.exists(file_path):
            print("  File exists, processing...")
            if process_file(file_path):
                fixed_count += 1
        else:
            print(f"  File not found: {file_path}")
    print(f"\nProcessed {len(target_files)} files, fixed {fixed_count} files")


if __name__ == "__main__":
    main()
