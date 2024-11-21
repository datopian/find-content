import os
import sys
import yaml
import re

frontmatter_keys = [
    {'name': 'path', 'required': True, 'type': str},
    {'name': 'publish_date', 'required': False, 'type': str},
    {'name': 'authors', 'required': False, 'type': list},
    {'name': 'content', 'required': False, 'type': str},
    {'name': 'themes', 'required': False, 'type': list},
    {'name': 'keywords', 'required': False, 'type': list},
    {'name': 'geographies', 'required': False, 'type': list},
    {'name': 'regions', 'required': False, 'type': list},
    {'name': 'diseases', 'required': True, 'type': list},
    {'name': 'related_datasets', 'required': False, 'type': list},
    {'name': 'featured_image_url', 'required': False, 'type': str},
    {'name': 'type', 'required': False, 'type': str},
]

def validate_insight(file_path):
    """
    Validate the structure and content of an Insight markdown file.

    Args:
        file_path (str): Path to the Markdown file to validate.

    Returns:
        bool: True if valid, False otherwise.
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
    is_valid = True
    
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
            is_valid = False

        if key_name in frontmatter_data and not isinstance(frontmatter_data[key_name], expected_type):
            print(f"Error: Field '{key_name}' must be of type '{expected_type.__name__}' in {file_path}.")
            is_valid = False

    if len(body.strip()) == 0:
        print(f"Error: Content body must not be empty in {file_path}.")
        is_valid = False
    
    return is_valid

def validate_all_insights(directory):
    """
    Validate all Insight markdown files in a directory.

    Args:
        directory (str): Path to the directory containing Markdown files.

    Returns:
        None
    """
    all_valid = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.mdx'):
                file_path = os.path.join(root, file)
                if not validate_insight(file_path):
                    all_valid = False
    
    if not all_valid:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    directory = 'insights'
    validate_all_insights(directory)
