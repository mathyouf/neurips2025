# UUID Distribution Guide

## Privacy Protection

This survey visualization uses UUIDs to protect participant privacy. Email addresses have been removed from all publicly accessible files.

## How UUIDs Work

- Each participant's email is hashed to generate a deterministic UUID
- UUIDs are consistent: same email = same UUID
- The mapping is one-way: UUID → data (not data → email)

## Distributing UUIDs to Participants

You should send each participant their UUID privately via email. Here's a template:

```
Subject: Your NeurIPS Twin Survey Visualization UUID

Hi [Name],

Thank you for participating in the NeurIPS Twin survey! You can now explore the interactive visualization and find yourself on the charts.

Your personal UUID: [UUID]

Visit: https://[your-site]/
Enter your UUID in the "Find Yourself" section to:
- Highlight your position on the compass charts
- See your k-nearest neighbors based on cluster similarity
- Adjust the slider to see 0-20 of your closest neighbors

Your email address is not stored in any publicly accessible files.

Best regards,
[Your Name]
```

## Generating the UUID Mapping

The private mapping file `/data/groups_with_uuid.csv` contains UUIDs and emails.

To extract UUIDs for distribution:

```bash
python3 << 'EOF'
import csv

with open('data/groups_with_uuid.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Email']},{row['UUID']}")
EOF
```

**Important**: Never commit or deploy files containing email addresses to public repositories.

## Public Files (Safe)

- `/docs/neuripstwin7.csv` - Survey data with UUIDs (no emails)
- `/docs/groups_with_uuid.csv` - Cluster data with UUIDs (no emails)

## Private Files (Keep Secure)

- `/data/groups_with_uuid.csv` - Contains email-to-UUID mapping
- `/data/neuripstwin7.csv` - Original survey data with emails

These should never be in the `/docs/` directory or deployed to GitHub Pages.
