import os
import sys
import yaml


def validate_md_files(directory):
    """
    Validates that all .md/.mdx files in the given directory
    have a non-empty 'question' field in their frontmatter.
    """
    invalid_files = []

    # Traverse all files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read file content
                    lines = f.readlines()

                # Extract frontmatter
                if len(lines) < 2 or lines[0].strip() != '---':
                    print(f"[WARNING] No valid frontmatter in {file_path}")
                    continue

                # Find the closing `---` for frontmatter
                end_index = None
                for i in range(1, len(lines)):
                    if lines[i].strip() == '---':
                        end_index = i
                        break

                if end_index is None:
                    print(f"[WARNING] Frontmatter not closed in {file_path}")
                    continue

                # Parse YAML frontmatter
                frontmatter = '\n'.join(lines[1:end_index])
                try:
                    metadata = yaml.safe_load(frontmatter)
                except yaml.YAMLError as e:
                    print(f"[ERROR] YAML parsing error in {file_path}: {e}")
                    invalid_files.append(file_path)
                    continue

                # Validate the `question` field
                if not metadata or 'question' not in metadata or not metadata['question'].strip():
                    print(f"[ERROR] 'question' field is missing or empty in {file_path}")
                    invalid_files.append(file_path)

    return invalid_files


if __name__ == "__main__":
    faq_directory = "faq"

    if not os.path.exists(faq_directory):
        print(f"[ERROR] Directory '{faq_directory}' does not exist.")
        sys.exit(1)

    print(f"Validating markdown files in '{faq_directory}'...")
    invalid_files = validate_md_files(faq_directory)

    if invalid_files:
        print("\nValidation failed for the following files:")
        for file in invalid_files:
            print(f" - {file}")
        sys.exit(1)
    else:
        print("\nAll files passed validation!")
        sys.exit(0)
