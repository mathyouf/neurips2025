# Email Distribution Guide

## Overview

Your NeurIPS Twin survey visualization is now ready! Here's how to send personalized links to each participant.

## Step 1: Generate the Email-UUID Mapping

Run the export script to create a file with each participant's UUID and personalized URL:

```bash
cd /home/user/neurips2025
python3 scripts/export_uuid_mapping.py
```

This creates `uuid_email_mapping_PRIVATE.csv` with 333 entries containing:
- **Email**: Participant's email address
- **UUID**: Their unique identifier
- **Personalized_URL**: Direct link that auto-fills their UUID

**Example output:**
```
Email,UUID,Personalized_URL
user@example.com,34e1c7f6-cee1-44a5-7c65-67cb444bfedd,https://[YOUR-SITE]/?uuid=34e1c7f6-cee1-44a5-7c65-67cb444bfedd
```

## Step 2: Replace [YOUR-SITE-URL] with Your Actual URL

Before sending, update the Personalized_URL column to use your actual GitHub Pages URL or custom domain.

Example:
```
https://mathyouf.github.io/neurips2025/?uuid=34e1c7f6-cee1-44a5-7c65-67cb444bfedd
```

## Step 3: Send Emails

Use your email tool with mail merge functionality (Gmail, Mailchimp, SendGrid, etc.).

### Email Template:

**Subject:** See Yourself in the NeurIPS Twin Survey Results

**Body:**
```
Hi [Name],

Thank you for participating in the NeurIPS Twin survey! The interactive visualization is now live, and you can explore the results.

🔗 Your Personalized Link: [Personalized_URL]

When you click the link, you'll automatically see:
• Your position on the political compass charts (highlighted in gold)
• Your k-nearest neighbors based on response similarity
• What you and your neighbors answered to key questions
• UMAP clustering showing your position among all respondents

You can adjust the slider to see anywhere from 0-20 of your nearest neighbors.

Explore the results and see where you fit in the NeurIPS community!

Best regards,
[Your Name]
```

## Step 4: How the Link Works

When participants click their personalized link:

1. **Auto-filled UUID**: The `?uuid=xxx` parameter automatically fills the UUID field
2. **Instant Highlighting**: Their dot is immediately highlighted with:
   - Gold borders
   - Full opacity
   - Larger size (4px vs 2px)
3. **KNN Visualization**: Their k-nearest neighbors are also highlighted
4. **Response Display**: Shows what they and their neighbors answered

## Features Participants Will See

### 1. Compass Charts (Figures 1 & 2)
- Their position based on AGI/safety beliefs and prototype/creativity preferences
- Category averages as larger dots
- Hover interactions to explore different groups

### 2. Pie Charts
- Distribution of categorical responses (dinner companions, workplaces, podcasts)
- Professional figure captions

### 3. Responses Section
- Shows their answers to key questions
- Displays up to 5 nearest neighbors' responses
- Side-by-side comparison

### 4. UMAP Clustering (Figure 3)
- Overall similarity visualization
- Dropdown to color by any survey question
- Shows natural clustering patterns

## Privacy & Security

✅ **Safe to Share:**
- Personalized URLs with UUIDs
- Public visualization site

🔒 **Keep Private:**
- `uuid_email_mapping_PRIVATE.csv` (contains emails!)
- `/data/groups_with_uuid.csv` (has email column)
- `/data/neuripstwin7.csv` (original with emails)

All public files (`/docs/`) have emails removed and replaced with UUIDs.

## Testing

Before mass sending, test with a few participants:

1. Pick 2-3 test email addresses
2. Send them their personalized links
3. Verify:
   - UUID auto-fills
   - Highlighting works
   - All charts update
   - Responses section appears
   - UMAP chart shows gold highlighting

## Manual UUID Entry (Alternative)

Participants can also:
1. Visit the site without a UUID parameter
2. Manually enter their UUID in the input field
3. Same highlighting will occur

But personalized links provide a better user experience!

## Technical Details

- **UUID Generation**: MD5 hash of email (deterministic, consistent)
- **KNN Calculation**: Euclidean distance on UMAP X,Y coordinates
- **Highlighting**: Updates all 3 charts simultaneously
- **Privacy**: One-way mapping (UUID → data, not reverse)

## Troubleshooting

**UUID not found:**
- Verify the UUID is correct
- Check that groups data is loaded properly
- Ensure the participant completed the survey

**Charts not highlighting:**
- Check browser console for errors
- Verify all CSV files are accessible
- Test with a known working UUID

**Slow loading:**
- Normal on first visit (loading 3 CSV files)
- Subsequent visits are cached and faster

---

**Questions?** Check the main documentation or open an issue on GitHub.
