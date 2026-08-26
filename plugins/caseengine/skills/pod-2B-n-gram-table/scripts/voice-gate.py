#!/usr/bin/env python3
"""Voice gate for pod-2B-n-gram-table Guideline 2 / 2A / 4.
Usage: voice-gate.py <n-gram-table.json> [more.json ...]
Exit 1 on any FAIL. See SKILL.md -> Quality gates -> Voice gate."""
import json,re,sys

PATTERNS=[
 ("abstract subject",       r'^(What|How|Where|When|Why|Who)\b[^?]*\b(someone|anyone|people)\b(?=[^?]*\?)', 'soft'),
 ("intensifier",            r'\b(actually|really|truly)\b', 'soft'),
 ("personified vanishing",  r'\b(disappear|disappears|vanish|vanishes)\b', 'hard'),
 ("region pairing",         r'\b(and|or) across\b', 'hard'),
 ("covert listicle",        r'^(What|Which)\s+(documents|records|evidence|witnesses|things|steps|factors)\b', 'hard'),
 ("trailing purpose",       r'\bto (protect|preserve|ensure|maximize)\b[^?]*\?$', 'hard'),
]
def run(paths):
    fails=warns=0
    for p in paths:
        d=json.load(open(p)); scope=d.get("scope",p)
        rows=d["rows"]; qs=[r["question"] for r in rows]
        for r in rows:
            q=r["question"]
            for name,pat,sev in PATTERNS:
                if re.search(pat,q,re.I):
                    tag="FAIL" if sev=="hard" else "WARN"
                    print("%s [%s] %s :: %s"%(tag,name,scope,q))
                    if sev=="hard": fails+=1
                    else: warns+=1
        rank=[r for r in rows if r.get("geo_lane")=="ranking"]
        if len(rank)>3:
            print("FAIL [ranking-lane cap] %s :: %d (max 3)"%(scope,len(rank))); fails+=1
        forks=[q for q in qs if re.search(r'\?\s*$',q) and re.search(r',\s*(the\s+)?[A-Z][\w\. ]+ (or|vs\.?) ',q)]
        if len(forks)>1:
            print("FAIL [fork cap] %s :: %d forks (max 1)"%(scope,len(forks))); fails+=1
        if len(rows)%20:
            print("FAIL [row count] %s :: %d (must be 20 per location)"%(scope,len(rows))); fails+=1
        body=sum(1 for r in rows if r.get("placement")=="body")
        pool=sum(1 for r in rows if r.get("placement")=="swap_pool")
        if (body,pool)!=(15,5):
            print("FAIL [body/pool split] %s :: %d/%d (must be 15/5)"%(scope,body,pool)); fails+=1
    # cross-city verbatim overlap: tables must NOT be copies of each other
    if len(paths)>1:
        qs=[set(r["question"] for r in json.load(open(p))["rows"]) for p in paths]
        shared=set.intersection(*qs); total=min(len(q) for q in qs)
        pct=round(100*len(shared)/total)
        exc=None
        for p3 in paths:
            e=json.load(open(p3)).get("overlap_exception")
            if e: exc=e; break
        if pct>60 and exc:
            print("EXCEPTION [cross-city overlap] %d%% (cap 60%%) - ACCEPTED with recorded reason: %s"%(pct,exc))
            warns+=1
        elif pct>60:
            print("FAIL [cross-city overlap] %d%% of questions identical across all locations (max 60%%). "
                  "Tables are generated PER LOCATION and must not overlap verbatim - "
                  "shared legal ground gets reworded per city. If the topic is genuinely uniform across "
                  "cities (doctrine/mechanics rather than scene-and-place), record an `overlap_exception` "
                  "with a REASON rather than forcing unnatural rewording."%pct); fails+=1
        else:
            print("PASS [cross-city overlap] %d%% verbatim overlap across %d locations"%(pct,len(paths)))
        # local-signal floor: every row needs local weight somewhere.
        # Local signal is NOT just the city name - a trauma center, county court, county sheriff,
        # CHP area office, or named freeway is local signal too. The table declares its own anchor
        # set in `local_anchors`; falling back to the city name alone under-counts badly
        # (e.g. "UCI Medical Center" is Irvine signal and contains no "Irvine").
        import re as _re
        for p2 in paths:
            d2=json.load(open(p2)); city=d2.get("city","")
            if not city: continue
            anchors=d2.get("local_anchors") or [city]
            pat=_re.compile("|".join(_re.escape(a) for a in anchors if a),_re.I)
            body=[r for r in d2["rows"] if r.get("placement")=="body"]
            dead=[r for r in body if not pat.search(r["question"])
                  and not any(pat.search(e) for e in r["entities"])
                  and not any(pat.search(n) for n in r["ngrams"])]
            share=round(100*(len(body)-len(dead))/len(body)) if body else 0
            if share<50:
                print("FAIL [local-signal floor] %s :: only %d%% of body rows carry ANY local signal "
                      "(question, entity, or n-gram); floor is 50%%. Localization lives in the ANSWER too."%(d2.get("scope",p2),share)); fails+=1
            else:
                print("PASS [local-signal floor] %s :: %d%% of body rows carry local signal"%(d2.get("scope",p2),share))
    print("\n%s  hard-fails=%d  warnings=%d"%("FAILED" if fails else "PASSED",fails,warns))
    return 1 if fails else 0
if __name__=="__main__": sys.exit(run(sys.argv[1:]))
