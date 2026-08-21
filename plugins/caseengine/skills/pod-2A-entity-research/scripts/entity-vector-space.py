#!/usr/bin/env python3
"""
What: Generates a radial vector space visualization of entities from an entity map.
Input: Directory containing entity-map.json (filename per the canonical Podcast Drive
       doc: https://docs.google.com/document/d/1YhybGpp9DIqmV56P6OOHIQe7A6RxvjQGHLHKcUM0JmU).
Output: PNG at visuals/entity-vector-space.png.
Re-run: Safe — overwrites existing PNG.

Convention sync: if the Podcast Drive doc changes the canonical filename or scope-folder
layout, update this script to match. The doc is the single source of truth.
"""

import argparse
import json
import math
import os
import sys

import numpy as np

# Optional imports — visuals degrade gracefully
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

try:
    from adjustText import adjust_text
    HAS_ADJUST = True
except ImportError:
    HAS_ADJUST = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TIER_COLORS = {
    1: '#3b82f6',  # blue
    2: '#14b8a6',  # teal
    3: '#94a3b8',  # gray
}
BRIDGE_BORDER_COLOR = '#facc15'  # gold
BRIDGE_BORDER_WIDTH = 2.5
DPI = 150
FIG_SIZE = (12, 12)
MIN_DOT_SIZE = 30
MAX_DOT_SIZE = 400
LABEL_FONTSIZE_T1 = 8
LABEL_FONTSIZE_T2 = 7
TOP_T2_LABELED = 5


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_entity_map(research_dir):
    """Load and validate 00-entity-map.json from research directory."""
    path = os.path.join(research_dir, 'entity-map.json')
    if not os.path.exists(path):
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path, 'r') as f:
        data = json.load(f)
    # Validate required keys
    for key in ('practice_area', 'entities', 'connection_graph'):
        if key not in data:
            print(f"ERROR: missing key '{key}' in entity map", file=sys.stderr)
            sys.exit(1)
    return data


def build_cluster_map(clusters):
    """Map entity ID -> cluster key from the clusters dict."""
    entity_to_cluster = {}
    for cluster_key, cluster_data in clusters.items():
        for eid in cluster_data.get('entities', []):
            entity_to_cluster[eid] = cluster_key
    return entity_to_cluster


def build_bridge_set(bridge_entities):
    """Set of entity IDs that are bridge entities."""
    return {b['id'] for b in bridge_entities}


def compute_positions(entities, clusters, entity_to_cluster):
    """Compute (x, y) for each entity based on cluster angle and vector_strength distance."""
    cluster_keys = sorted(clusters.keys())
    n_clusters = max(len(cluster_keys), 1)
    cluster_angle_map = {}
    for i, ck in enumerate(cluster_keys):
        # Each cluster gets an equal angular slice, offset by -pi/2 so first cluster starts at top
        base_angle = (2 * math.pi * i / n_clusters) - (math.pi / 2)
        cluster_angle_map[ck] = base_angle

    positions = {}
    for entity in entities:
        eid = entity['id']
        vs = entity.get('vector_strength', 0.5)
        radius = 1.0 - vs  # higher strength = closer to center

        cluster_key = entity_to_cluster.get(eid)
        if cluster_key is not None and cluster_key in cluster_angle_map:
            base_angle = cluster_angle_map[cluster_key]
            # Add small jitter within the cluster's slice to avoid overlap
            cluster_entities = clusters[cluster_key].get('entities', [])
            if len(cluster_entities) > 1:
                idx = cluster_entities.index(eid) if eid in cluster_entities else 0
                spread = (2 * math.pi / n_clusters) * 0.7  # use 70% of the slice
                offset = spread * (idx / (len(cluster_entities) - 1) - 0.5) if len(cluster_entities) > 1 else 0
                angle = base_angle + offset
            else:
                angle = base_angle
        else:
            # Unclustered: random-ish angle based on entity ID
            angle = (2 * math.pi * (eid * 137.508 % 360) / 360)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        positions[eid] = (x, y)

    return positions


def compute_dot_sizes(entities):
    """Map entity ID -> dot size proportional to connection count."""
    conn_counts = {e['id']: len(e.get('connections', [])) for e in entities}
    if not conn_counts:
        return {}
    max_conn = max(conn_counts.values()) if max(conn_counts.values()) > 0 else 1
    sizes = {}
    for eid, count in conn_counts.items():
        normalized = count / max_conn
        sizes[eid] = MIN_DOT_SIZE + normalized * (MAX_DOT_SIZE - MIN_DOT_SIZE)
    return sizes


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def render_vector_space(data, output_path):
    """Render the radial vector space visualization."""
    if not HAS_MPL:
        print("ERROR: matplotlib required for visualization", file=sys.stderr)
        sys.exit(1)

    practice_area = data['practice_area']
    entities = data['entities']
    clusters = data['connection_graph'].get('clusters', {})
    bridge_entities = data['connection_graph'].get('bridge_entities', [])

    entity_to_cluster = build_cluster_map(clusters)
    bridge_ids = build_bridge_set(bridge_entities)
    positions = compute_positions(entities, clusters, entity_to_cluster)
    dot_sizes = compute_dot_sizes(entities)

    # Build entity lookup
    entity_lookup = {e['id']: e for e in entities}

    # Determine which T2 entities get labels (top 5 by vector_strength)
    t2_entities = sorted(
        [e for e in entities if e.get('tier') == 2],
        key=lambda e: e.get('vector_strength', 0),
        reverse=True
    )
    t2_labeled_ids = {e['id'] for e in t2_entities[:TOP_T2_LABELED]}

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=FIG_SIZE, facecolor='white')
    ax.set_facecolor('white')
    ax.set_aspect('equal')

    # Draw faint concentric rings for distance reference
    for r in [0.25, 0.5, 0.75, 1.0]:
        circle = plt.Circle((0, 0), r, fill=False, color='#e2e8f0', linewidth=0.5, linestyle='--')
        ax.add_patch(circle)

    # Plot entities by tier (T3 first so T1 renders on top)
    texts = []
    for tier in [3, 2, 1]:
        tier_entities = [e for e in entities if e.get('tier') == tier]
        for entity in tier_entities:
            eid = entity['id']
            if eid not in positions:
                continue
            x, y = positions[eid]
            size = dot_sizes.get(eid, MIN_DOT_SIZE)
            color = TIER_COLORS.get(tier, '#94a3b8')
            is_bridge = eid in bridge_ids

            # Plot dot
            if is_bridge:
                ax.scatter(x, y, s=size, c=color, zorder=3, alpha=0.85,
                           edgecolors=BRIDGE_BORDER_COLOR, linewidths=BRIDGE_BORDER_WIDTH)
            else:
                ax.scatter(x, y, s=size, c=color, zorder=3, alpha=0.85,
                           edgecolors='white', linewidths=0.5)

            # Label logic
            should_label = (
                tier == 1 or
                (tier == 2 and eid in t2_labeled_ids)
            )
            if should_label:
                fontsize = LABEL_FONTSIZE_T1 if tier == 1 else LABEL_FONTSIZE_T2
                fontweight = 'bold' if tier == 1 else 'normal'
                txt = ax.annotate(
                    entity['name'],
                    (x, y),
                    fontsize=fontsize,
                    fontweight=fontweight,
                    color='#1e293b',
                    ha='center',
                    va='bottom',
                    xytext=(0, 6),
                    textcoords='offset points',
                    zorder=5,
                )
                texts.append(txt)

    # Center label
    ax.text(0, 0, practice_area.replace('-', ' ').title(),
            ha='center', va='center',
            fontsize=14, fontweight='bold', color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#cbd5e1', alpha=0.95),
            zorder=10)

    # Adjust labels if adjustText is available
    if HAS_ADJUST and texts:
        adjust_text(texts, ax=ax, expand_points=(1.5, 1.5), force_text=(0.3, 0.3))

    # Legend
    legend_handles = [
        mpatches.Patch(color=TIER_COLORS[1], label='Tier 1 (Core)'),
        mpatches.Patch(color=TIER_COLORS[2], label='Tier 2 (Supporting)'),
        mpatches.Patch(color=TIER_COLORS[3], label='Tier 3 (Peripheral)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#94a3b8',
                   markeredgecolor=BRIDGE_BORDER_COLOR, markeredgewidth=2.5,
                   markersize=10, label='Bridge Entity'),
    ]
    ax.legend(handles=legend_handles, loc='lower right', frameon=True,
              facecolor='white', edgecolor='#e2e8f0', fontsize=9)

    # Title
    title_text = f"Entity Vector Space: {practice_area.replace('-', ' ').title()}"
    ax.set_title(title_text, fontsize=16, fontweight='bold', color='#0f172a', pad=20)

    # Clean up axes
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.axis('off')

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Generate radial vector space visualization from entity map'
    )
    parser.add_argument('research_dir', help='Directory containing 00-entity-map.json')
    parser.add_argument('--output', '-o', default=None,
                        help='Output PNG path (default: <research-dir>/visuals/entity-vector-space.png)')
    args = parser.parse_args()

    research_dir = os.path.abspath(args.research_dir)
    if not os.path.isdir(research_dir):
        print(f"ERROR: {research_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or os.path.join(research_dir, 'visuals', 'entity-vector-space.png')
    output_path = os.path.abspath(output_path)

    data = load_entity_map(research_dir)

    entity_count = len(data.get('entities', []))
    cluster_count = len(data.get('connection_graph', {}).get('clusters', {}))
    bridge_count = len(data.get('connection_graph', {}).get('bridge_entities', []))
    print(f"Loaded: {entity_count} entities, {cluster_count} clusters, {bridge_count} bridges")

    render_vector_space(data, output_path)


if __name__ == '__main__':
    main()
