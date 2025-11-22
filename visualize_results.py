"""
Visualize Association Rule Mining Results

Creates comprehensive visualizations of the Apriori analysis results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from pathlib import Path
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create output directory for visualizations
VIZ_DIR = Path("visualizations")
VIZ_DIR.mkdir(exist_ok=True)

print("="*80)
print("VISUALIZING ASSOCIATION RULE MINING RESULTS")
print("="*80)
print()

# Load the results
results_file = Path("apriori_results/association_rules_by_segment.csv")
if not results_file.exists():
    print("❌ Error: Results file not found!")
    print("   Please run apriori_analysis.py first.")
    exit(1)

df = pd.read_csv(results_file)
print(f"✓ Loaded {len(df)} association rules")
print()

# ============================================================================
# VISUALIZATION 1: Confidence by Time Segment
# ============================================================================

print("Creating Visualization 1: Confidence Comparison by Time Segment...")

fig, ax = plt.subplots(figsize=(12, 6))

# Prepare data
segments = df['Time_Segment'].tolist()
confidence = df['Confidence'].tolist()

# Color map (gradient from yellow to red based on confidence)
colors = plt.cm.YlOrRd(np.array(confidence) / max(confidence))

# Create bar chart
bars = ax.bar(segments, confidence, color=colors, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar, conf in zip(bars, confidence):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{conf:.1%}',
            ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add reference lines
ax.axhline(y=0.6, color='green', linestyle='--', alpha=0.7, label='60% (Very High Confidence)')
ax.axhline(y=0.4, color='orange', linestyle='--', alpha=0.7, label='40% (Minimum Threshold)')

# Formatting
ax.set_ylabel('Confidence', fontsize=14, fontweight='bold')
ax.set_xlabel('Time Segment', fontsize=14, fontweight='bold')
ax.set_title('Association Rule Confidence by Time Segment\nOuro Brasileiro shot → Ginger Scone',
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
plt.xticks(rotation=45, ha='right')
ax.legend(loc='upper right', fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = VIZ_DIR / "1_confidence_by_segment.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# VISUALIZATION 2: Lift Comparison by Time Segment
# ============================================================================

print("Creating Visualization 2: Lift Comparison by Time Segment...")

fig, ax = plt.subplots(figsize=(12, 6))

# Prepare data
lift = df['Lift'].tolist()

# Color map
colors = plt.cm.RdYlGn(np.array(lift) / max(lift))

# Create bar chart
bars = ax.bar(segments, lift, color=colors, edgecolor='black', linewidth=1.5)

# Add value labels on bars
for bar, l in zip(bars, lift):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
            f'{l:.2f}x',
            ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add reference line at lift = 1 (no correlation)
ax.axhline(y=1, color='red', linestyle='--', alpha=0.7, linewidth=2,
           label='Lift = 1.0 (No Correlation)')

# Formatting
ax.set_ylabel('Lift (Correlation Strength)', fontsize=14, fontweight='bold')
ax.set_xlabel('Time Segment', fontsize=14, fontweight='bold')
ax.set_title('Association Rule Lift by Time Segment\nHow Much MORE Likely vs Random',
             fontsize=16, fontweight='bold', pad=20)
ax.set_ylim(0, max(lift) + 1)
plt.xticks(rotation=45, ha='right')
ax.legend(loc='upper right', fontsize=10)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
output_file = VIZ_DIR / "2_lift_by_segment.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# VISUALIZATION 3: Support-Confidence Scatter Plot
# ============================================================================

print("Creating Visualization 3: Support-Confidence Scatter with Lift...")

fig, ax = plt.subplots(figsize=(12, 8))

# Prepare data
support = df['Support'].tolist()
confidence = df['Confidence'].tolist()
lift = df['Lift'].tolist()

# Create scatter plot with size proportional to lift
scatter = ax.scatter(support, confidence,
                     s=[l * 100 for l in lift],  # Size based on lift
                     c=lift,  # Color based on lift
                     cmap='YlOrRd',
                     alpha=0.7,
                     edgecolors='black',
                     linewidth=2)

# Add labels for each point
for i, seg in enumerate(segments):
    ax.annotate(seg,
                (support[i], confidence[i]),
                xytext=(10, 10), textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

# Add reference lines
ax.axhline(y=0.6, color='green', linestyle='--', alpha=0.5, label='60% Confidence')
ax.axhline(y=0.4, color='orange', linestyle='--', alpha=0.5, label='40% Confidence (Threshold)')
ax.axvline(x=0.02, color='blue', linestyle='--', alpha=0.5, label='2% Support (Threshold)')

# Color bar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Lift (Correlation Strength)', fontsize=12, fontweight='bold')

# Formatting
ax.set_xlabel('Support (How Often Pattern Occurs)', fontsize=14, fontweight='bold')
ax.set_ylabel('Confidence (Prediction Accuracy)', fontsize=14, fontweight='bold')
ax.set_title('Association Rules: Support vs Confidence\n(Bubble Size = Lift Strength)',
             fontsize=16, fontweight='bold', pad=20)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax.legend(loc='lower right', fontsize=10)
ax.grid(alpha=0.3)

plt.tight_layout()
output_file = VIZ_DIR / "3_support_confidence_scatter.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# VISUALIZATION 4: Network Diagram of Association
# ============================================================================

print("Creating Visualization 4: Association Network Diagram...")

fig, ax = plt.subplots(figsize=(14, 10))

# Create network graph
G = nx.DiGraph()

# Add nodes and edges
for idx, row in df.iterrows():
    antecedent = row['Antecedent_Items']
    consequent = row['Consequent_Items']
    segment = row['Time_Segment']
    confidence = row['Confidence']
    lift = row['Lift']

    # Add nodes
    G.add_node(antecedent, node_type='antecedent')
    G.add_node(consequent, node_type='consequent')

    # Add edge with attributes
    G.add_edge(antecedent, f"{consequent}\n({segment})",
               confidence=confidence, lift=lift, segment=segment)

# Layout
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Draw nodes
antecedent_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'antecedent']
consequent_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'consequent']
other_nodes = [n for n in G.nodes() if n not in antecedent_nodes and n not in consequent_nodes]

# Draw antecedent (coffee) in blue
nx.draw_networkx_nodes(G, pos, nodelist=antecedent_nodes,
                       node_color='lightblue', node_size=5000,
                       node_shape='o', edgecolors='black', linewidths=3,
                       ax=ax)

# Draw consequents (labeled by segment) in different colors
if other_nodes:
    nx.draw_networkx_nodes(G, pos, nodelist=other_nodes,
                           node_color='lightcoral', node_size=4000,
                           node_shape='s', edgecolors='black', linewidths=3,
                           ax=ax)

# Draw edges with varying widths based on confidence
edges = G.edges()
confidences = [G[u][v]['confidence'] for u, v in edges]
widths = [c * 10 for c in confidences]  # Scale for visibility

nx.draw_networkx_edges(G, pos, edge_color='gray', width=widths,
                       alpha=0.7, arrows=True, arrowsize=30,
                       arrowstyle='->', connectionstyle='arc3,rad=0.1',
                       ax=ax)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

# Draw edge labels with confidence
edge_labels = {(u, v): f"{d['confidence']:.1%}\nLift: {d['lift']:.1f}x"
               for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8,
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.8),
                             ax=ax)

# Formatting
ax.set_title('Association Rule Network\nOuro Brasileiro shot → Ginger Scone by Time Segment',
             fontsize=16, fontweight='bold', pad=20)
ax.axis('off')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='lightblue', edgecolor='black', label='Antecedent (Item Purchased First)'),
    Patch(facecolor='lightcoral', edgecolor='black', label='Consequent (Item Purchased After)'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=12)

plt.tight_layout()
output_file = VIZ_DIR / "4_association_network.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# VISUALIZATION 5: All Metrics Combined (Dashboard)
# ============================================================================

print("Creating Visualization 5: Combined Metrics Dashboard...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Sort by time segment for consistent display
df_sorted = df.sort_values('Time_Segment')
segments_sorted = df_sorted['Time_Segment'].tolist()
confidence_sorted = df_sorted['Confidence'].tolist()
support_sorted = df_sorted['Support'].tolist()
lift_sorted = df_sorted['Lift'].tolist()

# Panel 1: Confidence
ax1 = fig.add_subplot(gs[0, 0])
colors_conf = plt.cm.YlOrRd(np.array(confidence_sorted) / max(confidence_sorted))
bars1 = ax1.barh(segments_sorted, confidence_sorted, color=colors_conf, edgecolor='black')
for i, (bar, conf) in enumerate(zip(bars1, confidence_sorted)):
    ax1.text(conf + 0.01, i, f'{conf:.1%}', va='center', fontweight='bold')
ax1.set_xlabel('Confidence', fontweight='bold')
ax1.set_title('Confidence by Segment', fontweight='bold', fontsize=12)
ax1.set_xlim(0, 1)
ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
ax1.grid(axis='x', alpha=0.3)

# Panel 2: Lift
ax2 = fig.add_subplot(gs[0, 1])
colors_lift = plt.cm.RdYlGn(np.array(lift_sorted) / max(lift_sorted))
bars2 = ax2.barh(segments_sorted, lift_sorted, color=colors_lift, edgecolor='black')
for i, (bar, l) in enumerate(zip(bars2, lift_sorted)):
    ax2.text(l + 0.2, i, f'{l:.2f}x', va='center', fontweight='bold')
ax2.set_xlabel('Lift', fontweight='bold')
ax2.set_title('Lift by Segment', fontweight='bold', fontsize=12)
ax2.grid(axis='x', alpha=0.3)

# Panel 3: Support
ax3 = fig.add_subplot(gs[1, 0])
colors_supp = plt.cm.Blues(np.array(support_sorted) / max(support_sorted))
bars3 = ax3.barh(segments_sorted, support_sorted, color=colors_supp, edgecolor='black')
for i, (bar, supp) in enumerate(zip(bars3, support_sorted)):
    ax3.text(supp + 0.001, i, f'{supp:.2%}', va='center', fontweight='bold', fontsize=9)
ax3.set_xlabel('Support', fontweight='bold')
ax3.set_title('Support by Segment', fontweight='bold', fontsize=12)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
ax3.grid(axis='x', alpha=0.3)

# Panel 4: Comparative Metrics Table
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('tight')
ax4.axis('off')

table_data = []
for idx, row in df_sorted.iterrows():
    table_data.append([
        row['Time_Segment'],
        f"{row['Confidence']:.1%}",
        f"{row['Lift']:.2f}x",
        f"{row['Support']:.2%}"
    ])

table = ax4.table(cellText=table_data,
                  colLabels=['Time Segment', 'Confidence', 'Lift', 'Support'],
                  cellLoc='center',
                  loc='center',
                  colWidths=[0.4, 0.2, 0.2, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style header row
for i in range(4):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows
for i in range(1, len(table_data) + 1):
    for j in range(4):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#f0f0f0')

ax4.set_title('Metrics Summary Table', fontweight='bold', fontsize=12, pad=10)

# Panel 5 & 6: Interpretation Guide (spanning bottom row)
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')

interpretation_text = """
INTERPRETATION GUIDE:

CONFIDENCE (Prediction Accuracy):
  • 60%+ = Very Reliable (Strong pattern, use for inventory decisions)
  • 40-60% = Moderately Reliable
  • <40% = Weak pattern
  YOUR RESULTS: 70-79% = EXCELLENT! Highly reliable for inventory planning.

LIFT (Correlation Strength):
  • Lift > 1 = Positive correlation (items go together)
  • Lift = 1 = No correlation (random)
  • Lift < 1 = Negative correlation
  YOUR RESULTS: 8-11x = VERY STRONG! These items have powerful association.

SUPPORT (Pattern Frequency):
  • Shows how often the pattern occurs in all transactions
  • 2%+ = Significant enough for inventory decisions
  YOUR RESULTS: 2-3% = Appears in 2-3 out of 100 transactions (significant over time).

KEY INSIGHT: When customers buy "Ouro Brasileiro shot", they buy "Ginger Scone" 70-79% of the time.
             This pattern is 8-11x stronger than random chance. Stock them in 10:7 ratio (shots:scones).
"""

ax5.text(0.5, 0.5, interpretation_text, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Main title
fig.suptitle('Association Rule Mining Dashboard\nOuro Brasileiro shot → Ginger Scone',
             fontsize=18, fontweight='bold', y=0.98)

output_file = VIZ_DIR / "5_combined_dashboard.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# VISUALIZATION 6: Inventory Recommendation Visual
# ============================================================================

print("Creating Visualization 6: Inventory Stocking Recommendation...")

fig, ax = plt.subplots(figsize=(14, 8))

# Create visual representation of stocking ratio
segments_clean = ['Morning\nWeekday', 'Morning\nWeekend',
                  'Afternoon\nWeekday', 'Afternoon\nWeekday']
confidences_pct = [72, 70, 79, 73]

# Create grouped bar chart showing stock recommendations
x = np.arange(len(segments_clean))
width = 0.35

# Bars for shots (always 10 as baseline)
shots = [10] * 4
scones = [int(c/100 * 10) for c in confidences_pct]  # Calculate scones based on confidence

bars1 = ax.bar(x - width/2, shots, width, label='Ouro Brasileiro Shots',
               color='#8B4513', edgecolor='black', linewidth=2)
bars2 = ax.bar(x + width/2, scones, width, label='Ginger Scones (Based on Confidence)',
               color='#F4A460', edgecolor='black', linewidth=2)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=12)

for bar, conf in zip(bars2, confidences_pct):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
            f'{int(height)}\n({conf}%)', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Formatting
ax.set_ylabel('Inventory Units to Stock', fontsize=14, fontweight='bold')
ax.set_xlabel('Time Segment', fontsize=14, fontweight='bold')
ax.set_title('Recommended Inventory Stocking Ratios\nBased on Association Rule Confidence',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(segments_clean)
ax.legend(loc='upper right', fontsize=12)
ax.set_ylim(0, 12)
ax.grid(axis='y', alpha=0.3)

# Add annotation box
textstr = 'Stock Ratio Guide:\nFor every 10 Ouro Brasileiro shots,\nstock 7-8 Ginger Scones'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props, fontweight='bold')

plt.tight_layout()
output_file = VIZ_DIR / "6_inventory_recommendations.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================

print()
print("="*80)
print("VISUALIZATION COMPLETE!")
print("="*80)
print()
print("Generated visualizations:")
print(f"  1. {VIZ_DIR}/1_confidence_by_segment.png")
print(f"     → Bar chart comparing confidence across time segments")
print()
print(f"  2. {VIZ_DIR}/2_lift_by_segment.png")
print(f"     → Bar chart comparing lift (correlation strength) across segments")
print()
print(f"  3. {VIZ_DIR}/3_support_confidence_scatter.png")
print(f"     → Scatter plot showing relationship between support and confidence")
print()
print(f"  4. {VIZ_DIR}/4_association_network.png")
print(f"     → Network diagram showing the association relationships")
print()
print(f"  5. {VIZ_DIR}/5_combined_dashboard.png")
print(f"     → Complete dashboard with all metrics and interpretation guide")
print()
print(f"  6. {VIZ_DIR}/6_inventory_recommendations.png")
print(f"     → Visual guide for inventory stocking ratios")
print()
print("All visualizations saved to the 'visualizations/' directory!")
print()
print("TIP: Open the files to see your data visualized!")
print("     Start with #5 (combined_dashboard.png) for a complete overview.")
print()
