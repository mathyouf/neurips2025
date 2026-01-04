#!/usr/bin/env python3
"""
Visualization script for NeurIPS Twin survey data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

# Load the data
df = pd.read_csv('data/neuripstwin7.csv')

print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

# Create a comprehensive visualization
fig, axes = plt.subplots(3, 3, figsize=(20, 15))
fig.suptitle('NeurIPS Twin Survey - Response Analysis', fontsize=16, fontweight='bold')

# 1. Who would you most want to have dinner with?
ax1 = axes[0, 0]
dinner_counts = df['Who would you most want to have dinner with?'].value_counts().head(10)
dinner_counts.plot(kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Top 10: Dream Dinner Companions')
ax1.set_xlabel('Count')

# 2. AGI beliefs
ax2 = axes[0, 1]
agi_col = 'I believe AGI is likely within the next 10 years.'
agi_data = df[agi_col].dropna()
agi_data.hist(bins=5, ax=ax2, color='coral', edgecolor='black')
ax2.set_title('AGI Likelihood (1-5 scale)')
ax2.set_xlabel('Rating')
ax2.set_ylabel('Count')
ax2.set_xticks([1, 2, 3, 4, 5])

# 3. Preferred workplace
ax3 = axes[0, 2]
workplace = df['I would most want to work at:'].value_counts()
workplace.plot(kind='bar', ax=ax3, color='lightgreen', edgecolor='black')
ax3.set_title('Preferred Workplace')
ax3.set_xlabel('')
ax3.tick_params(axis='x', rotation=45)

# 4. Training style
ax4 = axes[1, 0]
training_style = df['Your model training style is closest to:'].value_counts()
training_style.plot(kind='bar', ax=ax4, color='purple', alpha=0.7, edgecolor='black')
ax4.set_title('Model Training Style')
ax4.tick_params(axis='x', rotation=45)

# 5. Research style
ax5 = axes[1, 1]
research_style = df['Your research style is most like:'].value_counts()
research_style.plot(kind='barh', ax=ax5, color='teal')
ax5.set_title('Research Style')
ax5.set_xlabel('Count')

# 6. Solo vs Collaboration
ax6 = axes[1, 2]
collab_col = 'I prefer working solo rather than on large collaborations.'
collab_data = df[collab_col].dropna()
collab_data.hist(bins=5, ax=ax6, color='orange', edgecolor='black')
ax6.set_title('Solo vs Collaboration Preference (1-5)')
ax6.set_xlabel('Rating (1=Collab, 5=Solo)')
ax6.set_ylabel('Count')
ax6.set_xticks([1, 2, 3, 4, 5])

# 7. AI Safety - slow down progress
ax7 = axes[2, 0]
safety_col = 'We should slow down AI progress until safety is better understood.'
safety_data = df[safety_col].dropna()
safety_data.hist(bins=5, ax=ax7, color='red', alpha=0.6, edgecolor='black')
ax7.set_title('Slow AI Progress for Safety? (1-5)')
ax7.set_xlabel('Rating (1=No, 5=Yes)')
ax7.set_ylabel('Count')
ax7.set_xticks([1, 2, 3, 4, 5])

# 8. Primary bottleneck
ax8 = axes[2, 1]
bottleneck = df['What is the primary bottleneck right now?'].value_counts()
bottleneck.plot(kind='barh', ax=ax8, color='darkblue')
ax8.set_title('Primary Bottleneck in AI')
ax8.set_xlabel('Count')

# 9. Favorite podcast
ax9 = axes[2, 2]
podcasts = df['What is your favorite ML related podcast?'].value_counts().head(8)
podcasts.plot(kind='bar', ax=ax9, color='gold', edgecolor='black')
ax9.set_title('Top ML Podcasts')
ax9.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('neurips_twin_survey_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Visualization saved as 'neurips_twin_survey_analysis.png'")

# Additional insights
print("\n" + "="*60)
print("KEY INSIGHTS")
print("="*60)

print(f"\n📊 Total Responses: {len(df)}")

print(f"\n🍽️  Most Popular Dinner Companion:")
top_dinner = df['Who would you most want to have dinner with?'].value_counts().head(1)
print(f"   {top_dinner.index[0]}: {top_dinner.values[0]} votes")

print(f"\n🤖 AGI Belief Average: {df['I believe AGI is likely within the next 10 years.'].mean():.2f}/5")

print(f"\n💼 Most Popular Workplace:")
top_work = df['I would most want to work at:'].value_counts().head(1)
print(f"   {top_work.index[0]}: {top_work.values[0]} votes")

print(f"\n🔬 Most Common Research Style:")
top_research = df['Your research style is most like:'].value_counts().head(1)
print(f"   {top_research.index[0]}: {top_research.values[0]} researchers")

print(f"\n⚠️  AI Safety Concern Average: {df['We should slow down AI progress until safety is better understood.'].mean():.2f}/5")

# Show statement preferences
print(f"\n💭 Key Belief - Most Agreed Statement:")
statement_col = 'Which statement do you most agree with?'
top_statement = df[statement_col].value_counts().head(1)
print(f"   '{top_statement.index[0]}': {top_statement.values[0]} votes")

plt.show()
