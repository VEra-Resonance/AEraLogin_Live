#!/usr/bin/env python3
"""
Script to reverse news IDs in dashboard.html
Changes ID 1 → 16, ID 2 → 15, ID 3 → 14, etc.
Highest ID = first news entry
"""

import re
import sys

def reverse_news_ids(file_path):
    """Reverse all news IDs in feedData array"""
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all news IDs
    id_pattern = r'id:\s*(\d+),'
    matches = list(re.finditer(id_pattern, content))
    
    if not matches:
        print("❌ No news IDs found!")
        return False
    
    # Calculate max ID (should be 15)
    max_id = max(int(m.group(1)) for m in matches)
    print(f"📊 Found {len(matches)} news entries, max ID: {max_id}")
    
    # Create replacement mapping: 1→16, 2→15, 3→14, etc.
    new_max_id = max_id + 1
    mapping = {}
    for old_id in range(1, max_id + 1):
        new_id = new_max_id - old_id + 1
        mapping[old_id] = new_id
        print(f"  ID {old_id} → {new_id}")
    
    # Replace IDs in reverse order (to avoid conflicts)
    modified_content = content
    for old_id in sorted(mapping.keys(), reverse=True):
        new_id = mapping[old_id]
        # Use word boundaries to match exact IDs
        pattern = rf'\bid:\s*{old_id},'
        replacement = f'id: {new_id},'
        modified_content = re.sub(pattern, replacement, modified_content)
    
    # Backup original file
    backup_path = file_path + '.backup-id-reverse'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup created: {backup_path}")
    
    # Write modified content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    print(f"✅ IDs reversed in: {file_path}")
    
    return True

if __name__ == '__main__':
    file_path = 'dashboard.html'
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    print(f"🔄 Reversing news IDs in {file_path}...")
    success = reverse_news_ids(file_path)
    
    if success:
        print("✅ Done! News IDs have been reversed.")
        print("   Highest ID is now first in the list.")
    else:
        print("❌ Failed to reverse IDs")
        sys.exit(1)
