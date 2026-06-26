#!/usr/bin/env python3
import os
import re
import sys
import yaml

def check_link(base_dir, link_path):
    # Strip anchors
    if '#' in link_path:
        link_path = link_path.split('#')[0]
    if not link_path:
        return True # Just an anchor link within the page
    # Decode URL-encoded paths
    from urllib.parse import unquote
    link_path = unquote(link_path)
    # Check if absolute path or external link
    if link_path.startswith(('http://', 'https://', 'mailto:', 'file:///')):
        return True
    
    # Path relative to base_dir
    target_path = os.path.normpath(os.path.join(base_dir, link_path))
    if not os.path.exists(target_path):
        return False
    return True

def validate_file(file_path, repo_root):
    rel_path = os.path.relpath(file_path, repo_root)
    filename = os.path.basename(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Determine if it's a reserved file
    is_reserved = filename in ('index.md', 'log.md')
    is_root_index = rel_path == 'index.md'
    
    has_frontmatter = content.startswith('---')
    
    if is_reserved:
        if has_frontmatter:
            if is_root_index:
                # Root index can declare okf_version, verify it
                parts = content.split('---', 2)
                if len(parts) < 3:
                    print(f"ERROR: Malformed YAML frontmatter in root index {rel_path}")
                    return False
                try:
                    data = yaml.safe_load(parts[1])
                except Exception as e:
                    print(f"ERROR: Failed to parse YAML frontmatter in root index {rel_path}: {e}")
                    return False
                if not data or 'okf_version' not in data:
                    print(f"ERROR: Root index {rel_path} has frontmatter but lacks 'okf_version'")
                    return False
                if data.get('type') != "Knowledge Bundle Index":
                    print(f"ERROR: Root index {rel_path} frontmatter type must be 'Knowledge Bundle Index'")
                    return False
            else:
                print(f"ERROR: Reserved file {rel_path} must not contain concept frontmatter")
                return False
        # Check relative links in index.md
        if filename == 'index.md':
            base_dir = os.path.dirname(file_path)
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for text, link in links:
                if not check_link(base_dir, link):
                    print(f"ERROR: Link '{link}' in {rel_path} does not point to an existing file")
                    return False
        return True

    # Concept document
    if not has_frontmatter:
        print(f"ERROR: Concept document {rel_path} is missing YAML frontmatter")
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"ERROR: Malformed YAML frontmatter in {rel_path}")
        return False

    frontmatter_str = parts[1]
    body_str = parts[2].strip()

    # Check YAML parsing
    try:
        metadata = yaml.safe_load(frontmatter_str)
    except Exception as e:
        print(f"ERROR: Failed to parse YAML frontmatter in {rel_path}: {e}")
        return False

    if not metadata:
        print(f"ERROR: Frontmatter is empty in {rel_path}")
        return False

    # Check required fields
    required_fields = ['type', 'id', 'title', 'description', 'status', 'version', 'tags', 'timestamp']
    for field in required_fields:
        if field not in metadata or metadata[field] is None:
            print(f"ERROR: Missing required field '{field}' in {rel_path} frontmatter")
            return False
        if str(metadata[field]).strip() == "":
            print(f"ERROR: Empty field '{field}' in {rel_path} frontmatter")
            return False

    # Verify body is not empty
    if not body_str:
        print(f"ERROR: Concept document {rel_path} has an empty body")
        return False

    # Check relative links in concept documents too
    base_dir = os.path.dirname(file_path)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', body_str)
    for text, link in links:
        if not check_link(base_dir, link):
            print(f"WARNING: Link '{link}' in concept {rel_path} does not point to an existing file")

    return True

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Exclude hidden directories like .git, .agents, .tmp
    exclude_dirs = {'.git', '.agents', '.tmp'}
    
    markdown_files = []
    for root, dirs, files in os.walk(repo_root):
        # Prune hidden directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))

    success = True
    print(f"Validating {len(markdown_files)} markdown files...")
    for file_path in markdown_files:
        if not validate_file(file_path, repo_root):
            success = False

    if not success:
        print("Validation failed!")
        sys.exit(1)
    else:
        print("All checks passed successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()
