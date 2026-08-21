#!/usr/bin/env python3
"""
prep_ngram.py - render-prep a local n-gram table .md into a clean,
branded-body .md ready for Drive markdown->Doc upload.

For one source .md:
  - parse the H1 topic, metadata lines, the 4-col table
  - compute executive summary: row count, avg entities/row, localization scan
  - strip em dashes + curly quotes (house style)
  - emit: title H1, Executive Summary (generated narrative + stat bullets),
    Methodology (hard-coded), Collation Table, table explainer, and the
    INTERNAL section in the locked 4-block order:
      1. Cluster Architecture  - thematic pillars (lead block)
      2. Topic Entities        - universal practice-area entities, grouped
                                 by type (bold sub-label + bullet list)
      3. Local Anchors         - jurisdiction entities, grouped by type
                                 (Location/Extension scope only)
      4. Bridge Entity Coverage- cross-cutting entities mapped to Q numbers

The internal pipe-delimited metadata header line is INTENTIONALLY dropped
from the rendered Doc body - it lives in the raw source .md + metadata.json
+ the JSON `internal` block only.

Usage: prep_ngram.py <src_md> <out_md> [scope]
  scope (optional): "Topic Only" | "Location" | "Extension". When supplied
  it is authoritative - it decides whether the Local Anchors block renders.
  When omitted the scope is inferred from the table content.
Prints a JSON line of metadata (incl. the four INTERNAL blocks) to stdout.
"""
import sys, json, re, os
from collections import Counter, OrderedDict, defaultdict

EMDASH = "—"
ENDASH = "–"
CURLY = {
    "‘": "'", "’": "'",
    "“": '"', "”": '"',
    "′": "'", "″": '"',
}


def house_style(s: str) -> str:
    for k, v in CURLY.items():
        s = s.replace(k, v)
    s = s.replace(EMDASH, " - ")
    s = s.replace(ENDASH, "-")
    s = re.sub(r"  +", " ", s)
    return s


def _strip_balanced(s, opens, closes):
    """Remove every balanced bracketed span (handles nesting). Used to drop
    parenthetical statute citations like '(Fla. Stat. 627.736(1)(a))' and
    '[type]' tags cleanly, even when brackets nest."""
    out, depth = [], 0
    for ch in s:
        if ch in opens:
            depth += 1
            continue
        if ch in closes:
            depth = max(0, depth - 1)
            continue
        if depth == 0:
            out.append(ch)
    return "".join(out)


def _clean_entity(e):
    """Strip parenthetical citations / bracket type-tags for plain-language use."""
    e = e.replace("**", "")                   # drop markdown bold markers
    e = _strip_balanced(e, "(", ")")          # drop (Fla. Stat. ...) incl. nested
    e = _strip_balanced(e, "[", "]")          # drop [type] tags
    e = re.sub(r"\s*-\s*\d+%.*$", "", e)      # drop "- 51% Bar" tails
    e = re.sub(r"\s+", " ", e)                # collapse gaps left by strips
    return e.strip(" /;,-")


def split_entities(cell):
    """Split an Entities column cell into individual entity strings.

    The cell may be semicolon- or comma-delimited, and entity names can carry
    internal commas inside parentheses (e.g. 'Florida HB 837 (Tort Reform,
    2023)') or brackets. A naive `;|,` split shreds those names. Rule:
      - if the cell contains a semicolon, semicolons are the only delimiter;
      - otherwise split on commas, but only on commas at bracket/paren depth 0.
    """
    cell = cell.replace("**", "").strip()
    if not cell:
        return []
    # choose delimiter: semicolon if present, else comma. Either way split is
    # depth-aware so a delimiter inside ()/[] (e.g. '(Fla. Stat. 768.81; 2023
    # HB 837)') does not shred the entity name.
    delim = ";" if ";" in cell else ","
    parts, buf, depth = [], [], 0
    for ch in cell:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == delim and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def _raw_type_tag(e):
    """Pull a declared type tag from an entity string, if present.
    Handles both `[snake_case]` and `(Title Case)` annotation forms."""
    m = re.search(r"\[([^\]]+)\]", e)
    if m:
        return m.group(1).strip().lower()
    m = re.search(r"\(([^)]+)\)", e)
    if m:
        t = m.group(1).strip().lower()
        # only treat as a type tag when it reads like a category, not a citation
        if re.search(r"agency|concept|type|category|doctrine|process|"
                     r"regulation|standard|metric|database|program|discipline|"
                     r"resource|role|credential|party|method|condition|"
                     r"evidence|event", t):
            return t
    return None


# ----- LOCAL vs UNIVERSAL classification --------------------------------
LOCAL_KW = re.compile(
    r"\b(County|Police Department|Police Services|Sheriff|Superior Court|Circuit Court|"
    r"District Court|County Court|State Court|Municipal Court|City Court|"
    r"Highway Patrol|State Patrol|State Police|Hospital|Medical Center|"
    r"Medical Group|Trauma Center|Caltrans|HSMV|OCTA|Turnpike|Tollway|"
    r"Transit Authority|Transportation Authority|Airport|Bar Association|"
    r"City of|Town of|Township|Parish)\b", re.I)
HWY_KW = re.compile(
    r"\b(I-\d+\w*|US-\d+|SR-\d+|[A-Z]{2}-\d+|Route\s+\d+|Loop\s+\d+|"
    r"Highway\s+\d+|Interstate\s+\d+)\b")
# A named road / landmark: a proper-noun phrase ending in a road-type word
# (e.g. 'Roosevelt Bridge', 'Victory Drive', 'Jamboree Road'). Requires a
# capitalized lead word so generic phrases ('the bridge') do not match.
ROAD_LANDMARK = re.compile(
    r"\b([A-Z][A-Za-z.'-]+\s+)+(Bridge|Boulevard|Avenue|Parkway|Freeway|"
    r"Expressway|Turnpike|Tollway|Causeway|Drive|Road|Street|Corridor)\b")
STATE_NAMES = (
    "California|Colorado|Florida|Georgia|Texas|Arizona|Nevada|Oregon|"
    "Washington|Illinois|New York|Ohio|Michigan|Pennsylvania|"
    "North Carolina|South Carolina|Virginia|Tennessee|Massachusetts|"
    "Maryland|Missouri|Indiana|Kentucky|Alabama|Louisiana|Oklahoma|"
    "Kansas|Utah|Idaho|Montana|Wyoming|Nebraska|Iowa|Minnesota|"
    "Wisconsin|Arkansas|Mississippi|Connecticut|New Jersey|Hawaii|"
    "Alaska|Maine|New Hampshire|Vermont|Rhode Island|Delaware|"
    "West Virginia|New Mexico|North Dakota|South Dakota")
STATE_KW = re.compile(r"\b(" + STATE_NAMES + r")\b")


# Generic placeholders that look local but are not jurisdiction-tied. These
# are universal-class stand-ins from foundation (Topic Only) tables and must
# NOT be treated as local anchors. A placeholder is a generic noun phrase
# led by local/state/county/city/etc. - e.g. "state highway patrol",
# "local police department". Real place names like "City of Irvine" or
# "Orange County" are NOT placeholders (they are followed by a proper name
# or carry one), so the pattern requires the lead word be followed by a
# lowercase generic word, not "of {ProperName}" and not a capitalized name.
_PLACEHOLDER_LEAD = re.compile(
    r"^(local|state|county|city|municipal|regional)\s+(\S+)", re.I)


def _is_generic_placeholder(e):
    """A generic placeholder leads with local/state/county/etc. followed by a
    lowercase generic word - e.g. 'state highway patrol'. A real place name
    ('City of Irvine', 'Orange County') is followed by 'of' + a proper name
    or by a capitalized token, so it is not flagged."""
    m = _PLACEHOLDER_LEAD.match(e.strip())
    if not m:
        return False
    second = m.group(2)
    return second[:1].islower()


def is_local(e):
    """True when an entity is jurisdiction-specific (place-tied). Generic
    'state X' / 'local X' placeholders are explicitly NOT local."""
    if _is_generic_placeholder(e):
        return False
    return bool(LOCAL_KW.search(e) or HWY_KW.search(e)
                or ROAD_LANDMARK.search(e))


def is_state_scoped(e):
    """True when an entity names a real state and is itself a state-level
    jurisdiction body (state court, state patrol, state DOT, etc.) - i.e. a
    genuine local anchor, not a generic placeholder. A federal agency that
    merely contains a state name in passing is excluded by requiring a
    jurisdiction-body keyword alongside the state name."""
    if _is_generic_placeholder(e):
        return False
    if not STATE_KW.search(e):
        return False
    if is_local(e):
        return False
    return bool(re.search(
        r"\b(Court|Patrol|Police|Sheriff|Highway|Department of Transportation|"
        r"Department of Motor|Division of Insurance|Department of Insurance|"
        r"Judicial|Bar|Turnpike|Tollway|General Assembly|Legislature|"
        r"Attorney General|Public Utilities)\b", e, re.I))


# ----- LOCAL ANCHOR typing ---------------------------------------------
def local_type(e):
    """Group a local anchor by type for the Local Anchors block."""
    if HWY_KW.search(e) or re.search(
            r"\b(Turnpike|Tollway|Freeway|Expressway|Parkway|Boulevard|"
            r"Avenue|Bridge|Caltrans|Transportation)\b", e, re.I):
        return "Roads / Highways"
    if re.search(r"\b(Police|Sheriff|Highway Patrol|State Patrol|"
                 r"State Police|911|Emergency)\b", e, re.I):
        return "Law Enforcement"
    if re.search(r"\b(Hospital|Medical Center|Medical Group|Health|"
                 r"Clinic|Trauma|Kaiser|Permanente)\b", e, re.I):
        return "Medical Providers"
    if re.search(r"\bBar\b", e, re.I):
        return "Courts"
    if re.search(r"\b(Court|Judicial|Judiciary)\b", e, re.I):
        return "Courts"
    if re.search(r"\b(County|City of|Town of|Township|Parish|"
                 r"Department of Motor|Division of Insurance|"
                 r"Department of Insurance|General Assembly|Legislature|"
                 r"Attorney General|Public Utilities)\b", e, re.I):
        return "County / Municipal & State Bodies"
    return "Other Local"


LOCAL_TYPE_ORDER = ["Roads / Highways", "Law Enforcement", "Medical Providers",
                    "Courts", "County / Municipal & State Bodies",
                    "Other Local"]


# ----- TOPIC ENTITY typing ---------------------------------------------
def topic_type(e):
    """Group a universal (non-local) entity by type for the Topic Entities
    block. Uses any declared [type]/(type) tag first, then keyword fallback."""
    tag = _raw_type_tag(e)
    clean = _clean_entity(e)
    low = clean.lower()
    if tag:
        if any(k in tag for k in ("injury",)):
            return "Injury Types"
        if any(k in tag for k in ("damage", "damages")):
            return "Damages Concepts"
        if any(k in tag for k in ("agency", "government", "regulation",
                                  "program", "database", "regulatory")):
            return "Agencies & Regulators"
        if any(k in tag for k in ("statute", "standard", "law", "code",
                                  "rule")):
            return "Legal Standards & Statutes"
        if any(k in tag for k in ("doctrine", "concept", "process",
                                  "legal_concept")):
            return "Legal Standards & Statutes"
        if any(k in tag for k in ("cause", "event", "accident", "vehicle",
                                  "collision", "crash")):
            return "Accident Types"
        if any(k in tag for k in ("evidence", "discipline")):
            return "Evidence & Proof"
        if any(k in tag for k in ("case_type", "case type", "person",
                                  "role", "party")):
            return "Case Roles & Parties"
    # keyword fallback for un-tagged entities
    if re.search(r"\b(injury|injuries|whiplash|fracture|concussion|"
                 r"brain injury|spinal|paralysis|amputation|burn|"
                 r"soft tissue|catastrophic)\b", low):
        return "Injury Types"
    if re.search(r"\b(damages|compensation|pain and suffering|lost wages|"
                 r"loss of consortium|punitive|economic|non-economic|"
                 r"settlement value|multiplier)\b", low):
        return "Damages Concepts"
    if re.search(r"\b(administration|commission|commissioners|bureau|"
                 r"department of transportation|department of motor|"
                 r"safety board|federal|national highway|fmcsa|nhtsa|"
                 r"ntsb)\b", low):
        return "Agencies & Regulators"
    if re.search(r"\b(statute|statutes|code|rule|rules of|act\b|"
                 r"comparative negligence|negligence|tort|liability|"
                 r"limitations|professional conduct|restatement|"
                 r"eggshell|spoliation|contingency|contingent fee)\b", low):
        return "Legal Standards & Statutes"
    if re.search(r"\b(accident|collision|crash|rollover|jackknife|"
                 r"distracted driving|drowsy|drunk|dui|rear-end|"
                 r"hit and run|truck|rideshare|commercial vehicle|"
                 r"head-on|t-bone)\b", low):
        return "Accident Types"
    if re.search(r"\b(evidence|reconstruction|black box|dashcam|"
                 r"surveillance|witness|expert|medical records|"
                 r"police report|logbook|hours of service|eld|"
                 r"camera footage|demand letter)\b", low):
        return "Evidence & Proof"
    if re.search(r"\b(adjuster|attorney|lawyer|driver|trucking company|"
                 r"carrier|insurer|insurance company|plaintiff|"
                 r"defendant|claimant|passenger|employer)\b", low):
        return "Case Roles & Parties"
    return "Other Practice-Area Entities"


TOPIC_TYPE_ORDER = ["Accident Types", "Injury Types",
                    "Legal Standards & Statutes", "Damages Concepts",
                    "Agencies & Regulators", "Evidence & Proof",
                    "Case Roles & Parties", "Other Practice-Area Entities"]


# ----- CLUSTER ARCHITECTURE --------------------------------------------
# Each pillar carries a keyword set. A question scores against every pillar
# and is assigned to its best match (most keyword hits); order in this list
# breaks ties, so put the more specific pillars first.
CLUSTER_DEFS = OrderedDict([
    ("At the Scene & Immediate Steps",
     r"first (?:few )?(?:steps|things|minutes)|at the scene|immediately "
     r"after|what to do (?:right )?after|do in the first|right now|"
     r"very first"),
    ("Reporting, Police & Agencies",
     r"police|report to the (?:state|dmv)|agency|agencies|responds|"
     r"\bdmv\b|sr-1|hsmv|crash report|accident report|reporting "
     r"requirement|file (?:something|a report|with the state)"),
    ("Accident & Injury Types",
     r"accident type|crash type|types of (?:accident|crash|collision)|"
     r"head-on|rollover|rear-end|t-bone|injur(?:y|ies) (?:type|tend)|"
     r"catastrophic|traumatic brain|spinal|whiplash|how do .* hurt|"
     r"common .* (?:accident|crash)"),
    ("Medical Care & Documentation",
     r"medical (?:care|attention|treatment|documentation|record)|"
     r"hospital|see a doctor|prognosis|emergency room|er visit|"
     r"treatment gap|gap in (?:medical |)treatment|mmi|maximum "
     r"medical improvement"),
    ("Insurance, Fault & Negligence",
     r"insurance|adjuster|\bfault\b|negligen|comparative|coverage|"
     r"liabilit|first-party|third-party|claim type|tort threshold|"
     r"no-fault|\bpip\b|at-fault"),
    ("Evidence & Proving the Case",
     r"evidence|reconstruction|dashcam|camera footage|black box|"
     r"witness|proving|preserve|spoliation|expert (?:witness|"
     r"testimony)|life care plan"),
    ("Damages, Compensation & Claim Value",
     r"damages|compensation|recover|value of|how much|claim worth|"
     r"settlement value|pain and suffering|non-economic|economic "
     r"damages|multiplier|per diem|calculat"),
    ("Deadlines & Statute of Limitations",
     r"statute of limitations|deadline|how long do you have|filing "
     r"deadline|\btoll(?:ing|ed|)\b|extend or shorten|time limit"),
    ("Settlement, Litigation & Trial",
     r"settle|settlement|\btrial\b|litigation|lawsuit|demand letter|"
     r"mediation|negotiat|low(?:ball)? (?:settlement|offer)|\bdenied\b|"
     r"go to court"),
    ("Hiring Counsel & Fees",
     r"attorney|lawyer|hire|counsel|contingency|\bfee\b|choosing|"
     r"good standing|legal representation"),
    ("Special Scenarios",
     r"uninsured|underinsured|hit and run|rideshare|uber|lyft|"
     r"commercial truck|out of state|pre-existing|government "
     r"(?:vehicle|entity)|\btruck\b|delivery vehicle|18.?wheeler|"
     r"wrongful death|eggshell"),
])

# precompile each pillar's keyword set for scoring
_CLUSTER_RX = OrderedDict((c, re.compile(p)) for c, p in CLUSTER_DEFS.items())


def build_clusters(question_texts):
    """Map each question to its best-matching thematic pillar; return ordered
    cluster -> [q numbers]. A question is scored against every pillar (count
    of distinct keyword hits) and assigned to the highest scorer; the pillar
    list order breaks ties. A pillar only appears if a question lands in it."""
    assigned = OrderedDict((c, []) for c in CLUSTER_DEFS)
    misc = []
    for qn, qt in enumerate(question_texts, start=1):
        low = qt.lower()
        best, best_score = None, 0
        for cname, rx in _CLUSTER_RX.items():
            score = len(rx.findall(low))
            if score > best_score:
                best, best_score = cname, score
        if best:
            assigned[best].append(qn)
        else:
            misc.append(qn)
    out = OrderedDict((c, v) for c, v in assigned.items() if v)
    if misc:
        out["Closing Guidance & Other"] = misc
    return out


# ----- BRIDGE ENTITY COVERAGE ------------------------------------------
def build_bridge(row_entities):
    """row_entities: list (per question, in order) of cleaned entity name
    lists. A bridge entity is one that recurs across 3+ DISTINCT questions.
    Returns ordered entity -> sorted [q numbers]."""
    ent_qs = defaultdict(set)
    for qn, ents in enumerate(row_entities, start=1):
        for e in ents:
            if e:
                ent_qs[e].add(qn)
    bridges = {e: sorted(qs) for e, qs in ent_qs.items() if len(qs) >= 3}
    # order by reach (most questions first), then name
    ordered = sorted(bridges.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    return OrderedDict(ordered)


# ----- research summary -------------------------------------------------
def research_summary(topic, data_rows, localized, row_count):
    ents = Counter()
    for r in data_rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) >= 3:
            for e in split_entities(cells[2]):
                ce = _clean_entity(e)
                if ce:
                    ents[ce] += 1
    top = [e for e, c in ents.most_common() if c >= 2][:6]
    if not top:
        top = [e for e, _ in ents.most_common(5)]

    juris = None
    m = re.search(r"\(([^)]*(?:Extension|Anchor|County)[^)]*)\)", topic)
    if m:
        juris = m.group(1)
    else:
        m = re.search(r"\bin ([A-Z][A-Za-z .'-]+,\s*[A-Za-z]+)", topic)
        if m:
            juris = m.group(1)

    rows_n = row_count
    parts = []
    if top:
        lead = ", ".join(top[:-1]) + (" and " + top[-1] if len(top) > 1 else top[0])
        parts.append(
            f"The research for this episode keeps returning to a core set of "
            f"names and ideas: {lead}. These are the people, places, and rules "
            f"that come up again and again whenever this topic is searched and "
            f"discussed, so the conversation should keep circling back to them.")
    if localized and juris:
        parts.append(
            f"The picture is strongly local. The questions are built around "
            f"{juris} specifically - its roads, hospitals, courts, and the "
            f"agencies that handle these cases - rather than generic, "
            f"anywhere-in-the-country advice.")
    elif localized:
        parts.append(
            "The picture is strongly local: the questions are built around "
            "the specific jurisdiction - its roads, hospitals, courts, and "
            "agencies - rather than generic advice.")
    else:
        parts.append(
            "This is a foundational topic episode: the questions cover the "
            "subject broadly and apply across locations, giving a base layer "
            "that local episodes can later build on.")
    parts.append(
        f"Across {rows_n} planned questions, the episode should emphasize the "
        f"entities above and walk the listener through them in plain terms - "
        f"answering the real questions people ask, in the order they would "
        f"naturally come up.")
    return " ".join(parts)


def _grouped_block(title, type_order, by_type):
    """Render one grouped-by-type block: a section heading, then per type a
    bold sub-label and a bullet list of entries. Identical format for the
    Topic Entities and Local Anchors blocks."""
    o = [f"## {title}", ""]
    any_written = False
    for t in type_order:
        items = by_type.get(t)
        if not items:
            continue
        any_written = True
        o.append(f"**{t}**")
        o.append("")
        for it in items:
            o.append(f"- {it}")
        o.append("")
    # any type not in the declared order, appended last
    for t, items in by_type.items():
        if t in type_order or not items:
            continue
        any_written = True
        o.append(f"**{t}**")
        o.append("")
        for it in items:
            o.append(f"- {it}")
        o.append("")
    if not any_written:
        o.append("- (none identified for this scope)")
        o.append("")
    return o


def main():
    src, out = sys.argv[1], sys.argv[2]
    scope_arg = sys.argv[3].strip() if len(sys.argv) > 3 else None
    raw = open(src, encoding="utf-8").read()
    raw = house_style(raw)
    lines = raw.split("\n")

    # --- H1 topic ---
    topic = None
    h1_idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("# "):
            h1_idx = i
            h1 = ln[2:].strip()
            m = re.match(r"(?i)^n[- ]?gram table\s*[:\-]\s*(.+)$", h1)
            topic = m.group(1).strip() if m else h1
            break
    if topic is None:
        topic = os.path.basename(os.path.dirname(os.path.dirname(src)))

    # --- find the 4-col table ---
    tbl_start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("|") and "question text" in ln.lower():
            tbl_start = i
            break
    if tbl_start is None:
        sys.stderr.write(f"NO TABLE in {src}\n")
        sys.exit(3)

    tbl_end = tbl_start
    for i in range(tbl_start, len(lines)):
        if lines[i].strip().startswith("|"):
            tbl_end = i
        else:
            break
    table_lines = lines[tbl_start:tbl_end + 1]
    data_rows = [l for l in table_lines[2:] if l.strip().startswith("|")]
    row_count = len(data_rows)

    # --- parse each row into (question, entities[]) ---
    question_texts = []
    row_entities = []          # cleaned entity name lists, per question
    ent_counts = []
    for r in data_rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) < 4:
            cells += [""] * (4 - len(cells))
        qt = re.sub(r"^Q\d+\s*[:.\-]\s*", "", cells[0]).strip()
        question_texts.append(qt)
        raw_ents = split_entities(cells[2])
        ent_counts.append(len(raw_ents))
        cleaned = []
        seen = set()
        for e in raw_ents:
            ce = _clean_entity(e)
            if ce and ce.lower() not in seen:
                seen.add(ce.lower())
                cleaned.append((ce, e))   # keep raw for type detection
        row_entities.append(cleaned)

    avg_ent = round(sum(ent_counts) / len(ent_counts), 1) if ent_counts else 0.0

    # --- localization scan ---
    loc_hits = 0
    for r in data_rows:
        if LOCAL_KW.search(r) or HWY_KW.search(r) or STATE_KW.search(r):
            loc_hits += 1
    localized = loc_hits >= max(3, row_count // 3)

    # --- determine scope: Topic Only vs Location/Extension ---
    # The explicit scope argument (from the manifest scope_leaf) is
    # authoritative. When absent, infer from real local-anchor presence.
    if scope_arg:
        is_location_scope = scope_arg.lower() in ("location", "extension")
    else:
        has_local_anchor = any(
            is_local(raw_e) or is_state_scoped(raw_e)
            for ents in row_entities for (_, raw_e) in ents)
        juris_in_topic = bool(
            re.search(r"\(([^)]*(?:Extension|Anchor|County)[^)]*)\)|"
                      r"\bin [A-Z][A-Za-z .'-]+,", topic))
        is_location_scope = has_local_anchor and (localized or juris_in_topic)

    # --- INTERNAL block 1: Cluster Architecture ---
    clusters = build_clusters(question_texts)

    # --- INTERNAL block 2: Topic Entities (universal, grouped by type) ---
    topic_by_type = OrderedDict((t, []) for t in TOPIC_TYPE_ORDER)
    topic_seen = set()
    for ents in row_entities:
        for (clean, raw_e) in ents:
            if is_local(raw_e) or is_state_scoped(raw_e):
                continue
            key = clean.lower()
            if key in topic_seen:
                continue
            topic_seen.add(key)
            topic_by_type[topic_type(raw_e)].append(clean)
    topic_by_type = OrderedDict(
        (t, sorted(v)) for t, v in topic_by_type.items() if v)

    # --- INTERNAL block 3: Local Anchors (jurisdiction, grouped by type) ---
    local_by_type = OrderedDict((t, []) for t in LOCAL_TYPE_ORDER)
    local_seen = set()
    for ents in row_entities:
        for (clean, raw_e) in ents:
            if not (is_local(raw_e) or is_state_scoped(raw_e)):
                continue
            key = clean.lower()
            if key in local_seen:
                continue
            local_seen.add(key)
            local_by_type[local_type(raw_e)].append(clean)
    local_by_type = OrderedDict(
        (t, sorted(v)) for t, v in local_by_type.items() if v)

    # --- INTERNAL block 4: Bridge Entity Coverage ---
    bridge = build_bridge([[c for (c, _) in ents] for ents in row_entities])

    # --- localization scan string ---
    if localized:
        loc_str = (f"Localized - {loc_hits} of {row_count} rows reference "
                   f"jurisdiction-specific entities.")
    else:
        loc_str = (f"Topic-level - {loc_hits} of {row_count} rows carry "
                   f"location-specific entities (foundation table).")

    # --- build output md ---
    o = []
    o.append(f"# N-Gram Table: {topic}")
    o.append("")
    o.append("## Executive Summary")
    o.append("")
    o.append(research_summary(topic, data_rows, localized, row_count))
    o.append("")
    o.append(f"- Question rows: {row_count}")
    o.append(f"- Average entities per row: {avg_ent}")
    o.append(f"- Localization scan: {loc_str}")
    o.append("")
    o.append("## Methodology")
    o.append("")
    o.append(
        "Every question in this table is built from a structured entity "
        "analysis of the practice area and its jurisdiction. We map the "
        "people, places, institutions, and legal concepts that define how "
        "the topic is searched and discussed, score and weight each entity "
        "by relevance and authority, and group them into thematic clusters. "
        "Each cluster is then translated into episode questions engineered "
        "to surface the precise entities, terms, and actions that search "
        "engines and AI answer systems reward.")
    o.append("")
    o.append("## Collation Table")
    o.append("")
    o.extend(table_lines)
    o.append("")
    o.append(
        "The table above is the complete question framework for this "
        "episode. Each row is a planned conversation beat, paired with the "
        "entities, terms, and actions to surface as it is discussed; "
        "together they form the content backbone the Run of Show and final "
        "script are built from.")
    o.append("")

    # ===== INTERNAL section - locked 4-block order ======================
    o.append("# INTERNAL")
    o.append("")

    # Block 1 - Cluster Architecture
    o.append("## Cluster Architecture")
    o.append("")
    o.append(
        "The episode questions group into the following thematic pillars. "
        "Each pillar is a content arc the Run of Show is built around.")
    o.append("")
    for cname, qns in clusters.items():
        qref = ", ".join(f"Q{n}" for n in qns)
        o.append(f"- **{cname}** - {qref}")
    o.append("")

    # Block 2 - Topic Entities (always present, every scope)
    o.extend(_grouped_block("Topic Entities", TOPIC_TYPE_ORDER, topic_by_type))

    # Block 3 - Local Anchors (Location/Extension scope only)
    if is_location_scope and local_by_type:
        o.extend(_grouped_block("Local Anchors", LOCAL_TYPE_ORDER,
                                local_by_type))

    # Block 4 - Bridge Entity Coverage
    o.append("## Bridge Entity Coverage")
    o.append("")
    if bridge:
        o.append(
            "Cross-cutting entities that recur across multiple questions. "
            "These are the connective tissue of the episode - mention them "
            "consistently wherever their questions land.")
        o.append("")
        for ent, qns in bridge.items():
            qref = ", ".join(f"Q{n}" for n in qns)
            o.append(f"- **{ent}** - {qref}")
        o.append("")
    else:
        o.append("- (no entity recurs across 3+ questions in this table)")
        o.append("")

    open(out, "w", encoding="utf-8").write("\n".join(o))

    print(json.dumps({
        "topic": topic,
        "row_count": row_count,
        "avg_entities_per_row": avg_ent,
        "localization": loc_str,
        "localized": localized,
        "is_location_scope": is_location_scope,
        "internal": {
            "cluster_architecture": {c: qns for c, qns in clusters.items()},
            "topic_entities": topic_by_type,
            "local_anchors": (local_by_type if is_location_scope else {}),
            "bridge_entity_coverage": {e: qns for e, qns in bridge.items()},
        },
    }))


if __name__ == "__main__":
    main()
