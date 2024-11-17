import os
import sys
import yaml
import re


frontmatter_keys = [
    {'name': 'question', 'required': True, 'type': str},
    {'name': 'category', 'required': False, 'type': str},
]

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

    # Split frontmatter and body
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

    for key in frontmatter_keys:
        key_name = key['name']
        required = key['required']
        expected_type = key['type']

        if required and key_name not in frontmatter_data:
            print(f"Error: Missing required field '{key_name}' in {file_path}.")
            return False

        if key_name in frontmatter_data and not isinstance(frontmatter_data[key_name], expected_type):
            print(f"Error: Field '{key_name}' must be of type '{expected_type.__name__}' in {file_path}.")
            return False

    
    if len(body.strip()) == 0:
        print(f"Error: Answer must be not empty in {file_path}.")
        return False
    
    return True

def validate_all_faqs(directory):
    """
    Validate all FAQ markdown files in a directory.

    Args:
        directory (str): Path to the directory containing Markdown files.

    Returns:
        None
    """
    all_valid = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if not validate_faq(file_path):
                    all_valid = False
    
    if not all_valid:
        sys.exit(1)

if __name__ == "__main__":
    directory = 'faqs'
    validate_all_faqs(directory)
