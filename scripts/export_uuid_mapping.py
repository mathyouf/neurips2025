#!/usr/bin/env python3
"""
Export email-to-UUID mapping for distribution to participants.
This file should be kept PRIVATE and never committed to public repos.
"""
import csv
import os

def export_uuid_mapping():
    """Export email-to-UUID mapping from private groups file"""
    # Get the script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    input_file = os.path.join(project_root, 'data', 'groups_with_uuid.csv')
    output_file = os.path.join(project_root, 'data', 'uuid_email_mapping_PRIVATE.csv')

    mapping = []

    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        seen_emails = set()

        for row in reader:
            email = row['Email']
            uuid = row['UUID']

            # Only add each email once (some may have duplicates)
            if email not in seen_emails:
                mapping.append({
                    'Email': email,
                    'UUID': uuid,
                    'Personalized_URL': f'https://[YOUR-SITE-URL]/?uuid={uuid}'
                })
                seen_emails.add(email)

    # Sort by email for easier lookup
    mapping.sort(key=lambda x: x['Email'])

    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Email', 'UUID', 'Personalized_URL'])
        writer.writeheader()
        writer.writerows(mapping)

    print(f"✓ Exported {len(mapping)} unique email-to-UUID mappings")
    print(f"✓ File: {output_file}")
    print("\n⚠️  WARNING: Keep this file PRIVATE! Never commit to public repos.")
    print("\nYou can now:")
    print("1. Use this file to send personalized URLs via email")
    print("2. Import into your email tool for mail merge")
    print("3. Each URL auto-fills the UUID field")

if __name__ == '__main__':
    export_uuid_mapping()
