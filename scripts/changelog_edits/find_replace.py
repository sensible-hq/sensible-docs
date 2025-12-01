#!/usr/bin/env python3
"""
Mass find-replace operation on ReadMe changelogs
Reads tab-delimited find/replace pairs from a config file
"""

import os
import sys
import requests
from typing import List, Dict, Tuple
from collections import defaultdict

# Configuration
README_API_KEY = os.environ.get('README_API_KEY')
BASE_URL = "https://api.readme.com/v2"

class ChangelogUpdater:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def fetch_all_changelogs(self) -> List[Dict]:
        """Fetch all changelogs with pagination"""
        print("Fetching all changelogs from API v2...")
        all_changelogs = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{BASE_URL}/changelogs?per_page={per_page}&page={page}"
            response = requests.get(url, headers=self.headers)
            
            if not response.ok:
                print(f"Error: {response.status_code} - {response.text}")
                sys.exit(1)
            
            data = response.json()
            changelogs = data.get('data', [])
            
            if not changelogs:
                break
            
            all_changelogs.extend(changelogs)
            print(f"  Page {page}: Retrieved {len(changelogs)} changelogs")
            print(f"  Total so far: {len(all_changelogs)}/{data.get('total', '?')}")
            
            if len(changelogs) < per_page or not data.get('paging', {}).get('next'):
                break
            
            page += 1
        
        print(f"\nTotal changelogs fetched: {len(all_changelogs)}\n")
        return all_changelogs
    
    def load_replacements(self, config_file: str) -> List[Tuple[str, str]]:
        """Load find/replace pairs from tab-delimited file"""
        replacements = []
        
        with open(config_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n')
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('\t')
                if len(parts) != 2:
                    print(f"Warning: Line {line_num} doesn't have exactly 2 tab-separated values, skipping")
                    continue
                
                find_str, replace_str = parts
                replacements.append((find_str, replace_str))
        
        print(f"Loaded {len(replacements)} find/replace pairs from {config_file}\n")
        return replacements
    
    def preview_changes(self, changelogs: List[Dict], replacements: List[Tuple[str, str]]) -> Dict:
        """Preview all changes without making them"""
        print("=" * 80)
        print("PREVIEW OF CHANGES")
        print("=" * 80)
        
        changes = defaultdict(list)
        total_replacements = 0
        
        for changelog in changelogs:
            slug = changelog['slug']
            content = changelog.get('content', {}).get('body', '')
            
            if not content:
                continue
            
            changelog_changes = []
            modified_content = content
            
            for find_str, replace_str in replacements:
                count = modified_content.count(find_str)
                
                if count > 0:
                    modified_content = modified_content.replace(find_str, replace_str)
                    changelog_changes.append({
                        'find': find_str,
                        'replace': replace_str,
                        'count': count
                    })
                    total_replacements += count
            
            if changelog_changes:
                changes[slug] = {
                    'original': content,
                    'modified': modified_content,
                    'changes': changelog_changes,
                    'changelog': changelog
                }
        
        print(f"\nChangelogs affected: {len(changes)}/{len(changelogs)}")
        print(f"Total replacements: {total_replacements}\n")
        
        for slug, data in changes.items():
            print(f"\n📝 Changelog: {slug}")
            for change in data['changes']:
                print(f"  └─ Replace {change['count']}x: '{change['find']}' → '{change['replace']}'")
            
            first_change = data['changes'][0]
            find_str = first_change['find']
            idx = data['original'].find(find_str)
            if idx != -1:
                start = max(0, idx - 50)
                end = min(len(data['original']), idx + len(find_str) + 50)
                context = data['original'][start:end]
                print(f"\n  Context preview:")
                print(f"  ...{context}...")
        
        print("\n" + "=" * 80)
        print(f"Summary: {len(changes)} changelogs will be updated")
        print("=" * 80 + "\n")
        
        return changes
    
    def apply_changes(self, changes: Dict, auto_confirm: bool = False) -> Dict:
        """Apply changes to changelogs via API with individual confirmation"""
        print("\n" + "=" * 80)
        print("APPLYING CHANGES")
        print("=" * 80 + "\n")
        
        updated = []
        skipped = []
        failed = []
        
        for i, (slug, data) in enumerate(changes.items(), 1):
            print(f"\n[{i}/{len(changes)}] Changelog: {slug}")
            print(f"Title: {data['changelog'].get('title', 'N/A')}")
            
            for change in data['changes']:
                print(f"  └─ Replace {change['count']}x: '{change['find']}' → '{change['replace']}'")
            
            if not auto_confirm:
                while True:
                    response = input("\nUpdate this changelog? (y/n/q to quit): ").strip().lower()
                    if response in ['y', 'n', 'q']:
                        break
                    print("Please enter 'y', 'n', or 'q'")
                
                if response == 'q':
                    print("\nQuitting. Remaining changelogs will not be updated.")
                    skipped.extend(list(changes.keys())[i-1:])
                    break
                
                if response == 'n':
                    print(f"  ⊘ Skipped")
                    skipped.append(slug)
                    continue
            
            changelog = data['changelog']
            modified_content = data['modified']
            
            update_url = f"{BASE_URL}/changelogs/{slug}"
            payload = {
                'content': {
                    'body': modified_content,
                    'type': changelog.get('content', {}).get('type', 'markdown')
                }
            }
            
            print(f"  Updating...")
            response = requests.patch(update_url, headers=self.headers, json=payload)
            
            if response.ok:
                print(f"  ✓ Success")
                updated.append({
                    'slug': slug,
                    'title': changelog.get('title', 'N/A'),
                    'changes': data['changes']
                })
            else:
                print(f"  ✗ Error: {response.status_code} - {response.text}")
                failed.append({
                    'slug': slug,
                    'title': changelog.get('title', 'N/A'),
                    'error': f"{response.status_code} - {response.text}"
                })
        
        return {
            'updated': updated,
            'skipped': skipped,
            'failed': failed
        }
    
    def print_summary(self, results: Dict) -> None:
        """Print final summary of changes"""
        print("\n\n" + "=" * 80)
        print("FINAL SUMMARY")
        print("=" * 80)
        
        updated = results['updated']
        skipped = results['skipped']
        failed = results['failed']
        
        print(f"\n✓ Successfully updated: {len(updated)}")
        print(f"⊘ Skipped: {len(skipped)}")
        print(f"✗ Failed: {len(failed)}")
        
        if updated:
            print("\n" + "-" * 80)
            print("SUCCESSFULLY UPDATED CHANGELOGS:")
            print("-" * 80)
            for item in updated:
                print(f"\n📝 {item['slug']}")
                print(f"   Title: {item['title']}")
                total_changes = sum(c['count'] for c in item['changes'])
                print(f"   Changes: {total_changes} replacements across {len(item['changes'])} patterns")
                for change in item['changes']:
                    print(f"     • {change['count']}x: '{change['find']}' → '{change['replace']}'")
        
        if skipped:
            print("\n" + "-" * 80)
            print("SKIPPED CHANGELOGS:")
            print("-" * 80)
            for slug in skipped:
                print(f"  • {slug}")
        
        if failed:
            print("\n" + "-" * 80)
            print("FAILED UPDATES:")
            print("-" * 80)
            for item in failed:
                print(f"\n✗ {item['slug']}")
                print(f"   Title: {item['title']}")
                print(f"   Error: {item['error']}")
        
        print("\n" + "=" * 80)
        print("END OF SUMMARY")
        print("=" * 80 + "\n")
    
    def run(self, config_file: str, auto_confirm: bool = False) -> None:
        """Main execution flow"""
        replacements = self.load_replacements(config_file)
        
        if not replacements:
            print("No replacements found in config file. Exiting.")
            sys.exit(0)
        
        print("Find/Replace pairs to apply:")
        for i, (find_str, replace_str) in enumerate(replacements, 1):
            print(f"  {i}. '{find_str}' → '{replace_str}'")
        print()
        
        changelogs = self.fetch_all_changelogs()
        
        changes = self.preview_changes(changelogs, replacements)
        
        if not changes:
            print("No changes to make. Exiting.")
            sys.exit(0)
        
        if not auto_confirm:
            response = input("\nProceed with updates? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("Cancelled. No changes made.")
                sys.exit(0)
        
        results = self.apply_changes(changes, auto_confirm)
        
        self.print_summary(results)


def main():
    if not README_API_KEY:
        print("Error: README_API_KEY environment variable not set")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage: python changelog_replacer.py <config_file> [--auto-confirm]")
        print("\nConfig file format (tab-delimited):")
        print("  find_string1\treplace_string1")
        print("  find_string2\treplace_string2")
        print("\nLines starting with # are treated as comments")
        print("\nWithout --auto-confirm, you'll be asked to confirm each changelog update individually")
        sys.exit(1)
    
    config_file = sys.argv[1]
    auto_confirm = '--auto-confirm' in sys.argv
    
    if not os.path.exists(config_file):
        print(f"Error: Config file '{config_file}' not found")
        sys.exit(1)
    
    updater = ChangelogUpdater(README_API_KEY)
    updater.run(config_file, auto_confirm)


if __name__ == "__main__":
    main()