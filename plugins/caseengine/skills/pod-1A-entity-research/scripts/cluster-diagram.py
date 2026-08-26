#!/usr/bin/env python3
"""TEST: Cluster Architecture diagram - one bubble per cluster with its entities
listed inside (uniform text, bridges bold), black bridge links whose line weight
= bridge strength, cluster border weight = average member weight.
Text widths are measured exactly (TextPath), so labels always fit their circle.
"""
import argparse
import json
import math
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

CE_BLUE = "#3573ff"
DARK = "#0f172a"
GRAY = "#64748b"
BAND = "#eef2fb"
LINK = "#0f172a"
DPI = 300

FIG_W, FIG_H = 13.0, 9.0
XLIM, YLIM = 7.4, 5.2
DATA_PER_PT = (2 * XLIM / FIG_W) / 72.0   # exact: data units per point
FS_MEMBER = 6.2
FS_TITLE = 7.6
LINE_H = 0.205


def short(name, cap=40):
    s = re.sub(r"\s*\(.*?\)", "", name).strip()
    s = re.sub(r"^(Florida|Texas|California|Georgia)\s+", "", s)
    return s if len(s) <= cap else s[: cap - 1].rstrip() + "…"


def text_w(s, fs, bold=False):
    fp = FontProperties(size=fs, weight="bold" if bold else "normal")
    return TextPath((0, 0), s, prop=fp).get_extents().width * DATA_PER_PT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("research_dir")
    ap.add_argument("--output", "-o", required=True)
    args = ap.parse_args()

    d = json.load(open(os.path.join(args.research_dir, "entity-map.json")))
    ents = {e["id"]: e for e in d["entities"]}
    vs = {eid: (e.get("prominence", 0) * 0.45 + e.get("relatedness", 0) * 0.35
                + e.get("popularity", 0) * 0.20) for eid, e in ents.items()}
    clusters = d["connection_graph"]["clusters"]
    bridges = {b["id"]: b["clusters_connected"] for b in d["connection_graph"]["bridge_entities"]}

    keys = sorted(clusters.keys(), key=lambda k: -len(clusters[k]["entities"]))
    n = len(keys)

    # radii from exact text widths + vertical need
    radii = {}
    for k in keys:
        rows = clusters[k]["entities"]
        widest = max((text_w(short(ents[e]["name"]), FS_MEMBER, e in bridges)
                      for e in rows if e in ents), default=0.6)
        r_v = LINE_H * (len(rows) + 1) / 2 + 0.24
        radii[k] = max(0.72, r_v, widest / 2 + 0.18)

    # ring layout, expand until no adjacent bubbles touch
    def layout(scale):
        c = {}
        for i, k in enumerate(keys):
            ang = 2 * math.pi * i / n - math.pi / 2
            c[k] = (scale * math.cos(ang) * 1.30, scale * math.sin(ang) * 0.90)
        return c

    scale = 3.9
    while scale < 6.0:
        centers = layout(scale)
        ok = True
        for i in range(n):
            a, b = keys[i], keys[(i + 1) % n]
            dist = math.hypot(centers[a][0] - centers[b][0], centers[a][1] - centers[b][1])
            if dist < radii[a] + radii[b] + 0.12:
                ok = False
                break
        if ok:
            break
        scale += 0.1
    centers = layout(scale)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), facecolor="white")
    ax.set_aspect("equal")
    ax.set_xlim(-XLIM, XLIM)
    ax.set_ylim(-YLIM, YLIM)
    ax.axis("off")

    # bridge links (under the bubbles); line weight = bridge strength
    for eid, conn in bridges.items():
        s = vs.get(eid, 0.6)
        lw = 0.6 + 3.2 * max(0.0, min(1.0, (s - 0.5) / 0.5))
        pts = [centers[c] for c in conn if c in centers]
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]],
                        color=LINK, lw=lw, alpha=0.45, zorder=1)

    for k in keys:
        cx, cy = centers[k]
        rows = sorted(clusters[k]["entities"], key=lambda e: -vs.get(e, 0))
        r = radii[k]
        cluster_w = sum(vs.get(e, 0) for e in rows) / max(len(rows), 1)
        border = 0.8 + 3.0 * max(0.0, min(1.0, (cluster_w - 0.45) / 0.45))
        ax.add_patch(plt.Circle((cx, cy), r, facecolor=BAND, edgecolor="#8fadf0",
                                lw=border, zorder=2))
        ax.text(cx, cy + r + 0.08, short(clusters[k]["name"], 30), ha="center", va="bottom",
                fontsize=FS_TITLE, fontweight="bold", color=CE_BLUE, zorder=4)
        block = LINE_H * (len(rows) - 1)
        top = cy + block / 2
        for j, eid in enumerate(rows):
            e = ents.get(eid)
            if not e:
                continue
            is_bridge = eid in bridges
            fs = FS_MEMBER
            ly = top - j * LINE_H
            dy = ly - cy
            avail = 2 * (max(r * r - dy * dy, 0.02) ** 0.5) - 0.12
            label = short(e["name"])
            while fs > 4.0 and text_w(label, fs, is_bridge) > avail:
                fs -= 0.3
            while len(label) > 8 and text_w(label, fs, is_bridge) > avail:
                label = label[:-2].rstrip() + "…"
            ax.text(cx, ly, label, ha="center", va="center", fontsize=fs,
                    color=DARK if is_bridge else GRAY,
                    fontweight="bold" if is_bridge else "normal", zorder=4)

    pa = d.get("practice_area", "").replace("-", " ").title()
    ax.set_title(f"Cluster Architecture: {pa}", fontsize=13, fontweight="bold",
                 color=DARK, pad=14)
    handles = [
        mpatches.Patch(facecolor=BAND, edgecolor="#8fadf0", label="Cluster (contextual layer)"),
        plt.Line2D([0], [0], color=LINK, lw=1.6, label="Bridge connection (weight = strength)"),
        plt.Line2D([0], [0], color="#8fadf0", lw=2.6, label="Border weight = cluster weight"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=True,
               facecolor="white", edgecolor="#e2e8f0", fontsize=7,
               bbox_to_anchor=(0.5, 0.02))
    fig.savefig(args.output, dpi=DPI, bbox_inches="tight", facecolor="white")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
