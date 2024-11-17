import os
import sys
import yaml
import re

def validate_faq(file_path):
    """
    Validate the structure and content of a FAQ markdown file.

    Args:
        file_path (str): Path to the Markdown file to validate.

    Returns:
        None
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"Error: {file_path} does not have valid frontmatter.")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    try:
        frontmatter_data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML frontmatter in {file_path}: {e}")
        return False

    if 'question' not in frontmatter_data or not isinstance(frontmatter_data['question'], str):
        print(f"Error: Missing or invalid 'question' field in {file_path}.")
        return False

    if not body.strip():
        print(f"Error: Missing 'answer' (body) in {file_path}.")
        return False

    if 'category' in frontmatter_data and not isinstance(frontmatter_data['category'], str):
        print(f"Error: 'category' field must be a string in {file_path}.")
        return False

    print(f"Validated: {file_path} is valid.")
    return True

def validate_all_faqs(directory):
    """
    Validate all FAQ markdown files in a directory.

    Args:
        directory (str): Path to the directory containing Markdown files.

    Returns:
        None
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                validate_faq(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_faq.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    validate_all_faqs(directory)
