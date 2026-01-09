#!/usr/bin/env python3
"""
Political Compass-style visualization for NeurIPS Twin survey data
X-axis: AGI timeline beliefs (average)
Y-axis: AI safety concerns (inverted - lower = more safety concern)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Load the data
df = pd.read_csv('data/neuripstwin7.csv')

# Filter out empty rows
df = df[df['Timestamp'].notna() & (df['Timestamp'].str.strip() != '')]

# Column names
agi_col = 'I believe AGI is likely within the next 10 years.'
safety_col = 'We should slow down AI progress until safety is better understood.'
dinner_col = 'Who would you most want to have dinner with?'
workplace_col = 'I would most want to work at:'
podcast_col = 'What is your favorite ML related podcast?'

# Function to calculate average scores for each unique value in a categorical column
def get_category_positions(df, category_col, agi_col, safety_col, min_count=3):
    """
    For each unique value in category_col, calculate average AGI and Safety scores
    """
    positions = []

    unique_values = df[category_col].dropna().unique()

    for value in unique_values:
        if not value or str(value).strip() == '':
            continue

        # Get all rows with this value
        mask = df[category_col] == value
        subset = df[mask]

        # Skip if too few responses
        if len(subset) < min_count:
            continue

        # Calculate averages
        agi_scores = pd.to_numeric(subset[agi_col], errors='coerce').dropna()
        safety_scores = pd.to_numeric(subset[safety_col], errors='coerce').dropna()

        if len(agi_scores) > 0 and len(safety_scores) > 0:
            avg_agi = agi_scores.mean()
            avg_safety = safety_scores.mean()
            count = len(subset)

            positions.append({
                'label': value,
                'agi': avg_agi,
                'safety': avg_safety,
                'count': count
            })

    return positions

# Get positions for each category
dinner_positions = get_category_positions(df, dinner_col, agi_col, safety_col, min_count=3)
workplace_positions = get_category_positions(df, workplace_col, agi_col, safety_col, min_count=3)
podcast_positions = get_category_positions(df, podcast_col, agi_col, safety_col, min_count=5)

# Create the plot
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
fig.suptitle('AI Researcher Political Compass\nAGI Timeline vs AI Safety Beliefs',
             fontsize=20, fontweight='bold', y=0.995)

# Color schemes
colors = {
    'dinner': '#FF6B6B',
    'workplace': '#4ECDC4',
    'podcast': '#FFE66D'
}

def plot_compass(ax, positions, title, color, category_name):
    """Plot a political compass style chart"""

    if not positions:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
        return

    # Extract data
    x = [p['agi'] for p in positions]
    y = [5 - p['safety'] for p in positions]  # Invert safety (5 - score)
    labels = [p['label'] for p in positions]
    sizes = [p['count'] * 20 for p in positions]  # Size based on count

    # Create scatter plot
    scatter = ax.scatter(x, y, s=sizes, c=color, alpha=0.6, edgecolors='black', linewidth=2)

    # Add quadrant lines at the mean
    ax.axhline(y=2.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax.axvline(x=3, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # Add quadrant labels
    ax.text(1.2, 4.8, 'Safety First\nAGI Skeptics', fontsize=10, ha='left', va='top',
            style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(4.8, 4.8, 'Safety First\nAGI Believers', fontsize=10, ha='right', va='top',
            style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(1.2, 0.2, 'Move Fast\nAGI Skeptics', fontsize=10, ha='left', va='bottom',
            style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax.text(4.8, 0.2, 'Move Fast\nAGI Believers', fontsize=10, ha='right', va='bottom',
            style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # Label each point
    for i, label in enumerate(labels):
        # Truncate long labels
        display_label = label if len(label) <= 20 else label[:17] + '...'
        ax.annotate(display_label, (x[i], y[i]),
                   fontsize=8, ha='center', va='bottom',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'))

    # Styling
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xlabel('AGI Likely Within 10 Years →', fontsize=12, fontweight='bold')
    ax.set_ylabel('← Prioritize AI Safety (Inverted)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.2)
    ax.set_aspect('equal')

    # Add size legend
    legend_sizes = [5, 15, 30]
    legend_labels = ['5 responses', '15 responses', '30 responses']
    legend_handles = [plt.scatter([], [], s=s*20, c=color, alpha=0.6, edgecolors='black', linewidth=2)
                     for s in legend_sizes]
    ax.legend(legend_handles, legend_labels, loc='upper left', framealpha=0.9, title='Response Count')

# Plot each category
plot_compass(axes[0, 0], dinner_positions,
            f'By Dream Dinner Companion\n({len(dinner_positions)} unique choices)',
            colors['dinner'], 'Dinner Guest')

plot_compass(axes[0, 1], workplace_positions,
            f'By Preferred Workplace\n({len(workplace_positions)} unique choices)',
            colors['workplace'], 'Workplace')

plot_compass(axes[1, 0], podcast_positions,
            f'By Favorite ML Podcast\n({len(podcast_positions)} unique choices)',
            colors['podcast'], 'Podcast')

# Combined plot in bottom right
ax_combined = axes[1, 1]

all_positions = []
all_colors = []
all_markers = []

for pos in dinner_positions:
    all_positions.append(pos)
    all_colors.append(colors['dinner'])
    all_markers.append('o')

for pos in workplace_positions:
    all_positions.append(pos)
    all_colors.append(colors['workplace'])
    all_markers.append('s')

for pos in podcast_positions:
    all_positions.append(pos)
    all_colors.append(colors['podcast'])
    all_markers.append('^')

if all_positions:
    x_all = [p['agi'] for p in all_positions]
    y_all = [5 - p['safety'] for p in all_positions]
    sizes_all = [p['count'] * 15 for p in all_positions]

    # Plot by category with different markers
    offset = 0
    for positions, color, marker, label in [
        (dinner_positions, colors['dinner'], 'o', 'Dinner'),
        (workplace_positions, colors['workplace'], 's', 'Workplace'),
        (podcast_positions, colors['podcast'], '^', 'Podcast')
    ]:
        if positions:
            x = [p['agi'] for p in positions]
            y = [5 - p['safety'] for p in positions]
            sizes = [p['count'] * 15 for p in positions]
            ax_combined.scatter(x, y, s=sizes, c=color, alpha=0.6,
                              marker=marker, edgecolors='black', linewidth=2, label=label)

    # Add quadrant lines
    ax_combined.axhline(y=2.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    ax_combined.axvline(x=3, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    # Add quadrant labels
    ax_combined.text(1.2, 4.8, 'Safety First\nAGI Skeptics', fontsize=10, ha='left', va='top',
                    style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax_combined.text(4.8, 4.8, 'Safety First\nAGI Believers', fontsize=10, ha='right', va='top',
                    style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax_combined.text(1.2, 0.2, 'Move Fast\nAGI Skeptics', fontsize=10, ha='left', va='bottom',
                    style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    ax_combined.text(4.8, 0.2, 'Move Fast\nAGI Believers', fontsize=10, ha='right', va='bottom',
                    style='italic', alpha=0.5, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    ax_combined.set_xlim(0.5, 5.5)
    ax_combined.set_ylim(0.5, 5.5)
    ax_combined.set_xlabel('AGI Likely Within 10 Years →', fontsize=12, fontweight='bold')
    ax_combined.set_ylabel('← Prioritize AI Safety (Inverted)', fontsize=12, fontweight='bold')
    ax_combined.set_title('Combined View - All Categories', fontsize=14, fontweight='bold', pad=10)
    ax_combined.grid(True, alpha=0.2)
    ax_combined.legend(loc='upper left', framealpha=0.9, title='Category')
    ax_combined.set_aspect('equal')

plt.tight_layout()
plt.savefig('political_compass_chart.png', dpi=300, bbox_inches='tight')
print("\n✓ Political compass chart saved as 'political_compass_chart.png'")

# Print summary statistics
print("\n" + "="*70)
print("POLITICAL COMPASS SUMMARY")
print("="*70)

print(f"\n📊 Dinner Companions analyzed: {len(dinner_positions)}")
for pos in sorted(dinner_positions, key=lambda x: x['agi'], reverse=True)[:5]:
    print(f"   {pos['label']:30s} AGI:{pos['agi']:.2f} Safety:{pos['safety']:.2f} (n={pos['count']})")

print(f"\n💼 Workplaces analyzed: {len(workplace_positions)}")
for pos in sorted(workplace_positions, key=lambda x: x['agi'], reverse=True):
    print(f"   {pos['label']:30s} AGI:{pos['agi']:.2f} Safety:{pos['safety']:.2f} (n={pos['count']})")

print(f"\n🎧 Podcasts analyzed: {len(podcast_positions)}")
for pos in sorted(podcast_positions, key=lambda x: x['agi'], reverse=True):
    print(f"   {pos['label']:30s} AGI:{pos['agi']:.2f} Safety:{pos['safety']:.2f} (n={pos['count']})")

plt.show()
