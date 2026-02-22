import os
import re

directory = "/home/jdpark/opensource-job-portal"
exclude_dirs = {'.git', 'node_modules', 'venv', 'env', '__pycache__', 'staticfiles'}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return  # Skip binary files

    original_content = content
    
    # Case sensitive replacements first
    content = content.replace("Inaworks.id", "Inaworks.id")
    content = content.replace("InaWorks.id", "InaWorks.id")
    content = content.replace("INAWORKS.ID", "INAWORKS.ID")
    content = content.replace("inaworks.id", "inaworks.id")
    
    # Additional generic inaworks variations without .com
    content = content.replace("Inaworks", "Inaworks")
    content = content.replace("InaWorks", "InaWorks")
    content = content.replace("inaworks", "inaworks")
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

for root, dirs, files in os.walk(directory):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith(('.py', '.html', '.js', '.css', '.json', '.md', '.txt', '.svelte', '.ts')):
            replace_in_file(os.path.join(root, file))

print("Replacement complete.")
