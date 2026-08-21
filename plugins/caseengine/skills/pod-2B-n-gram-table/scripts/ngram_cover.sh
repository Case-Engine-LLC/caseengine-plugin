#!/usr/bin/env bash
# ngram_cover.sh — apply the branded Case Engine cover page to an n-gram-table
# Google Doc. Applies the branded Case Engine cover page.
#
# Assumes the markdown body has ALREADY been uploaded to $DOC_ID as a Google
# Doc (Drive auto-convert). This script only builds the cover + header/footer
# + strips the auto-injected H1 + applies Roboto.
#
# Usage:
#   ngram_cover.sh --doc-id <docId> --subtitle "<topic>" \
#       --scope "<scope line>" --date "<Month D, YYYY>" --header-anchor "<short>"

set -euo pipefail
LOGO_ID="1pAZESV-Roq_fh0-1n8xMcMCJvtOiWAN2"   # CE 350x90 dark, shared anyoneWithLink
CE_BLUE_R="0.2078"; CE_BLUE_G="0.4510"; CE_BLUE_B="1.0"
DARK_R="0.0588"; DARK_G="0.0902"; DARK_B="0.1647"

DOC_ID=""; SUBTITLE=""; SCOPE=""; DATE_STR=""; HEADER_ANCHOR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --doc-id) DOC_ID="$2"; shift 2 ;;
    --subtitle) SUBTITLE="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --date) DATE_STR="$2"; shift 2 ;;
    --header-anchor) HEADER_ANCHOR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done
for v in DOC_ID SUBTITLE SCOPE DATE_STR HEADER_ANCHOR; do
  [ -z "${!v}" ] && { echo "Missing --$v" >&2; exit 1; }
done

LOGO_URI="https://drive.google.com/uc?export=view&id=${LOGO_ID}"
strip_noise() { grep -v '^Using keyring' | grep -v '^Warning:' || true; }

sleep 2  # let Drive conversion settle

# --- compute style index spans ---
# Order printed below MUST match the read order: title, subtitle, scope,
# prepared, date, total_end.
read -r TITLE_S TITLE_E SUB_S SUB_E SCOPE_S SCOPE_E PREP_S PREP_E DATE_S DATE_E TOTAL_END < <(python3 -c "
sub='''$SUBTITLE'''
scope='''$SCOPE'''
date='''$DATE_STR'''
lines=[('s1','\n'),('s2','\n'),('s3','\n'),
       ('title','N-Gram Table\n'),
       ('subtitle',sub+'\n'),
       ('smid','\n'),
       ('scope',scope+'\n'),
       ('s5','\n'),
       ('prepared','Prepared by Case Engine\n'),
       ('date',date+'\n')]
cur=1; spans={}
for n,c in lines:
    s=cur; e=cur+len(c); spans[n]=(s,e); cur=e
def to(n):
    s,e=spans[n]; return s,e-1
print(*to('title'),*to('subtitle'),*to('scope'),*to('prepared'),*to('date'),cur)
")

COVER_TEXT=$'\n\n\nN-Gram Table\n'"$SUBTITLE"$'\n\n'"$SCOPE"$'\n\nPrepared by Case Engine\n'"$DATE_STR"$'\n'

# Phase A: insert cover text + page break
PHASE_A=$(python3 -c "
import json
print(json.dumps({'requests':[
  {'insertText':{'location':{'index':1},'text':'''$COVER_TEXT'''}},
  {'insertPageBreak':{'location':{'index':$TOTAL_END}}}
]}))
")
gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_A" 2>&1 | strip_noise > /dev/null

# Phase B: style cover + insert logo
PHASE_B=$(python3 <<PYEOF
import json
sub_s,sub_e=$SUB_S,$SUB_E
title_s,title_e=$TITLE_S,$TITLE_E
scope_s,scope_e=$SCOPE_S,$SCOPE_E
prep_s,prep_e=$PREP_S,$PREP_E
date_s,date_e=$DATE_S,$DATE_E
total_end=$TOTAL_END
dark={'red':$DARK_R,'green':$DARK_G,'blue':$DARK_B}
blue={'red':$CE_BLUE_R,'green':$CE_BLUE_G,'blue':$CE_BLUE_B}
def color(c): return {'color':{'rgbColor':c}}
req=[]
req.append({'updateParagraphStyle':{'range':{'startIndex':1,'endIndex':total_end},
  'paragraphStyle':{'alignment':'CENTER'},'fields':'alignment'}})
req.append({'updateTextStyle':{'range':{'startIndex':1,'endIndex':total_end},
  'textStyle':{'weightedFontFamily':{'fontFamily':'Roboto','weight':400},'foregroundColor':color(dark)},
  'fields':'weightedFontFamily,foregroundColor'}})
# Title "N-Gram Table" - CE Blue 36pt bold
req.append({'updateTextStyle':{'range':{'startIndex':title_s,'endIndex':title_e},
  'textStyle':{'bold':True,'fontSize':{'magnitude':36,'unit':'PT'},
    'weightedFontFamily':{'fontFamily':'Roboto','weight':700},'foregroundColor':color(blue)},
  'fields':'bold,fontSize,weightedFontFamily,foregroundColor'}})
# Subtitle (topic) - CE Dark 22pt bold
req.append({'updateTextStyle':{'range':{'startIndex':sub_s,'endIndex':sub_e},
  'textStyle':{'bold':True,'fontSize':{'magnitude':22,'unit':'PT'},
    'weightedFontFamily':{'fontFamily':'Roboto','weight':700},'foregroundColor':color(dark)},
  'fields':'bold,fontSize,weightedFontFamily,foregroundColor'}})
# Scope line - 14pt regular dark
req.append({'updateTextStyle':{'range':{'startIndex':scope_s,'endIndex':scope_e},
  'textStyle':{'bold':False,'fontSize':{'magnitude':14,'unit':'PT'},
    'weightedFontFamily':{'fontFamily':'Roboto','weight':400},'foregroundColor':color(dark)},
  'fields':'bold,fontSize,weightedFontFamily,foregroundColor'}})
for s,e in ((prep_s,prep_e),(date_s,date_e)):
    req.append({'updateTextStyle':{'range':{'startIndex':s,'endIndex':e},
      'textStyle':{'bold':False,'fontSize':{'magnitude':11,'unit':'PT'},
        'weightedFontFamily':{'fontFamily':'Roboto','weight':400},'foregroundColor':color(dark)},
      'fields':'bold,fontSize,weightedFontFamily,foregroundColor'}})
# CE logo at index 2
req.append({'insertInlineImage':{'location':{'index':2},'uri':'$LOGO_URI',
  'objectSize':{'width':{'magnitude':216,'unit':'PT'},'height':{'magnitude':55.5,'unit':'PT'}}}})
print(json.dumps({'requests':req}))
PYEOF
)
gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_B" 2>&1 | strip_noise > /dev/null

# Phase C: strip Drive auto-injected H1 + Roboto across body
DOC_JSON=$(mktemp)
trap 'rm -f "$DOC_JSON"' EXIT
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"

read -r AUTO_H1_S AUTO_H1_E < <(python3 -c "
import json
total_end=$TOTAL_END
d=json.load(open('$DOC_JSON'))
auto_s=auto_e=0
for e in d['body']['content']:
    si=e.get('startIndex',0)
    if si<=total_end: continue
    if 'paragraph' not in e: continue
    p=e['paragraph']
    style=p.get('paragraphStyle',{}).get('namedStyleType','')
    text=''.join(el['textRun'].get('content','') for el in p.get('elements',[]) if 'textRun' in el)
    if not text.strip(): continue
    if style=='HEADING_1':
        auto_s,auto_e=e['startIndex'],e['endIndex']
    break
print(auto_s,auto_e)
")
if [ "$AUTO_H1_S" -gt 0 ]; then
  STRIP=$(python3 -c "import json;print(json.dumps({'requests':[{'deleteContentRange':{'range':{'startIndex':$AUTO_H1_S,'endIndex':$AUTO_H1_E}}}]}))")
  gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$STRIP" 2>&1 | strip_noise > /dev/null
  gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
fi

BODY_END=$(python3 -c "import json;d=json.load(open('$DOC_JSON'));print(d['body']['content'][-1].get('endIndex',1))")
PHASE_C=$(python3 -c "
import json
total_end=$TOTAL_END; body_end=$BODY_END
start=total_end+1; end=max(body_end-1,start+1)
print(json.dumps({'requests':[{'updateTextStyle':{'range':{'startIndex':start,'endIndex':end},
  'textStyle':{'weightedFontFamily':{'fontFamily':'Roboto','weight':400}},'fields':'weightedFontFamily'}}]}))
")
gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_C" 2>&1 | strip_noise > /dev/null

# Phase C2: strip Drive auto-injected bookmark anchors
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
STRIP_BM=$(python3 <<PYEOF
import json
d=json.load(open('$DOC_JSON'))
ranges=[]
def walk(content):
    for elem in content:
        if 'paragraph' in elem:
            for el in elem['paragraph'].get('elements',[]):
                if 'bookmark' in el:
                    ranges.append((el['startIndex'],el['endIndex']))
        if 'table' in elem:
            for row in elem['table'].get('tableRows',[]):
                for cell in row.get('tableCells',[]):
                    walk(cell.get('content',[]))
walk(d['body']['content'])
ranges.sort(key=lambda r:r[0],reverse=True)
print(json.dumps({'count':len(ranges),'body':{'requests':[
  {'deleteContentRange':{'range':{'startIndex':s,'endIndex':e}}} for s,e in ranges]}}))
PYEOF
)
BM_COUNT=$(echo "$STRIP_BM" | python3 -c "import json,sys;print(json.load(sys.stdin)['count'])")
if [ "$BM_COUNT" -gt 0 ]; then
  BM_BODY=$(echo "$STRIP_BM" | python3 -c "import json,sys;print(json.dumps(json.load(sys.stdin)['body']))")
  gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$BM_BODY" 2>&1 | strip_noise > /dev/null
fi

# Phase D: running header + footer
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
HEADER_ID=$(python3 -c "import json;d=json.load(open('$DOC_JSON'));print(next(iter(d.get('headers',{}).keys()),''))")
FOOTER_ID=$(python3 -c "import json;d=json.load(open('$DOC_JSON'));print(next(iter(d.get('footers',{}).keys()),''))")
if [ -z "$HEADER_ID" ] || [ -z "$FOOTER_ID" ]; then
  HF=$(gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" \
    --json '{"requests":[{"createHeader":{"type":"DEFAULT"}},{"createFooter":{"type":"DEFAULT"}}]}' 2>&1 | strip_noise)
  HEADER_ID=$(echo "$HF" | python3 -c "import json,sys;d=json.load(sys.stdin);[print(r['createHeader']['headerId']) for r in d.get('replies',[]) if 'createHeader' in r]")
  FOOTER_ID=$(echo "$HF" | python3 -c "import json,sys;d=json.load(sys.stdin);[print(r['createFooter']['footerId']) for r in d.get('replies',[]) if 'createFooter' in r]")
fi
HEADER_TEXT="Case Engine | N-Gram Table | $HEADER_ANCHOR"
FOOTER_TEXT="Case Engine | Confidential    Page "
PHASE_D=$(python3 <<PYEOF
import json
hid="$HEADER_ID"; fid="$FOOTER_ID"
ht='''$HEADER_TEXT'''; ft='''$FOOTER_TEXT'''
dark={'red':$DARK_R,'green':$DARK_G,'blue':$DARK_B}
req=[
 {'insertText':{'location':{'index':0,'segmentId':hid},'text':ht}},
 {'updateTextStyle':{'range':{'startIndex':0,'endIndex':len(ht),'segmentId':hid},
   'textStyle':{'italic':True,'fontSize':{'magnitude':9,'unit':'PT'},
     'weightedFontFamily':{'fontFamily':'Roboto','weight':400},'foregroundColor':{'color':{'rgbColor':dark}}},
   'fields':'italic,fontSize,weightedFontFamily,foregroundColor'}},
 {'updateParagraphStyle':{'range':{'startIndex':0,'endIndex':len(ht),'segmentId':hid},
   'paragraphStyle':{'alignment':'END'},'fields':'alignment'}},
 {'insertText':{'location':{'index':0,'segmentId':fid},'text':ft}},
 {'updateTextStyle':{'range':{'startIndex':0,'endIndex':len(ft),'segmentId':fid},
   'textStyle':{'fontSize':{'magnitude':9,'unit':'PT'},
     'weightedFontFamily':{'fontFamily':'Roboto','weight':400},'foregroundColor':{'color':{'rgbColor':dark}}},
   'fields':'fontSize,weightedFontFamily,foregroundColor'}},
 {'updateParagraphStyle':{'range':{'startIndex':0,'endIndex':len(ft),'segmentId':fid},
   'paragraphStyle':{'alignment':'START'},'fields':'alignment'}}
]
print(json.dumps({'requests':req}))
PYEOF
)
gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_D" 2>&1 | strip_noise > /dev/null

# Phase D2: page break before the "Collation Table" heading so the table
# starts at the top of a fresh page (helps it land on ~2 pages cleanly).
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
PHASE_D2=$(python3 <<PYEOF
import json
d=json.load(open('$DOC_JSON'))
ins=None
for e in d['body']['content']:
    if 'paragraph' not in e:
        continue
    p=e['paragraph']
    if p.get('paragraphStyle',{}).get('namedStyleType','')!='HEADING_2':
        continue
    txt=''.join(el['textRun'].get('content','') for el in p.get('elements',[]) if 'textRun' in el)
    if txt.strip().lower()=='collation table':
        ins=e['startIndex']
        break
req=[]
if ins is not None and ins>1:
    req.append({'insertPageBreak':{'location':{'index':ins}}})
print(json.dumps({'requests':req}))
PYEOF
)
NREQ_D2=$(echo "$PHASE_D2" | python3 -c "import json,sys;print(len(json.load(sys.stdin)['requests']))")
if [ "$NREQ_D2" -gt 0 ]; then
  gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_D2" 2>&1 | strip_noise > /dev/null
fi

# Phase E: polish the collation table - branded shaded header row, column
# widths, cell padding, Roboto across every cell.
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
PHASE_E=$(python3 <<PYEOF
import json
d=json.load(open('$DOC_JSON'))
blue={'red':$CE_BLUE_R,'green':$CE_BLUE_G,'blue':$CE_BLUE_B}
dark={'red':$DARK_R,'green':$DARK_G,'blue':$DARK_B}
white={'red':1.0,'green':1.0,'blue':1.0}
# header tint = very light CE blue for body alt? keep header solid blue.
# find the first (and only) collation table
tbl=None; tbl_start=None
for e in d['body']['content']:
    if 'table' in e:
        tbl=e['table']; tbl_start=e['startIndex']; break
req=[]
if tbl is not None:
    ncols=tbl.get('columns',4)
    # column widths (usable width 468pt): Question 132 / N-grams 114 / Entities 108 / Predicates 114
    widths=[132,114,108,114][:ncols]
    for ci,w in enumerate(widths):
        req.append({'updateTableColumnProperties':{
            'tableStartLocation':{'index':tbl_start},
            'columnIndices':[ci],
            'tableColumnProperties':{'widthType':'FIXED_WIDTH',
                'width':{'magnitude':w,'unit':'PT'}},
            'fields':'widthType,width'}})
    rows=tbl['tableRows']
    nrows=len(rows)
    # COMPACT table - tuned to land the collation table at ~2 pages.
    # cell padding on EVERY cell - tableRange spanning all rows x all cols.
    # L/R padding renders reliably; vertical sizing via minRowHeight below.
    req.append({'updateTableCellStyle':{
        'tableRange':{'tableCellLocation':{
            'tableStartLocation':{'index':tbl_start},
            'rowIndex':0,'columnIndex':0},
            'rowSpan':nrows,'columnSpan':ncols},
        'tableCellStyle':{
            'paddingTop':{'magnitude':1.5,'unit':'PT'},
            'paddingBottom':{'magnitude':1.5,'unit':'PT'},
            'paddingLeft':{'magnitude':5,'unit':'PT'},
            'paddingRight':{'magnitude':5,'unit':'PT'},
            'contentAlignment':'TOP'},
        'fields':'paddingTop,paddingBottom,paddingLeft,paddingRight,contentAlignment'}})
    # tight minimum row height - rows still grow to fit content
    for ri in range(nrows):
        req.append({'updateTableRowStyle':{
            'tableStartLocation':{'index':tbl_start},
            'rowIndices':[ri],
            'tableRowStyle':{'minRowHeight':{
                'magnitude':(16 if ri==0 else 12),'unit':'PT'}},
            'fields':'minRowHeight'}})
    # header row 0 - CE blue background (whole-row range)
    req.append({'updateTableCellStyle':{
        'tableRange':{'tableCellLocation':{
            'tableStartLocation':{'index':tbl_start},
            'rowIndex':0,'columnIndex':0},
            'rowSpan':1,'columnSpan':ncols},
        'tableCellStyle':{'backgroundColor':{'color':{'rgbColor':blue}}},
        'fields':'backgroundColor'}})
    # text styling: walk every cell. Roboto everywhere; header white bold
    # 8.5pt, body 8pt. Tight 1.0 line spacing + 0 space-before/after to
    # reclaim vertical room and pull the table toward 2 pages.
    for ri,row in enumerate(rows):
        for ci,cell in enumerate(row['tableCells']):
            for ce in cell.get('content',[]):
                if 'paragraph' not in ce: continue
                pe=ce['paragraph'].get('elements',[])
                if pe:
                    p_s=pe[0].get('startIndex')
                    p_e=pe[-1].get('endIndex')
                    if p_s is not None and p_e is not None and p_e>p_s:
                        req.append({'updateParagraphStyle':{
                            'range':{'startIndex':p_s,'endIndex':p_e},
                            'paragraphStyle':{
                                'lineSpacing':100,
                                'spaceAbove':{'magnitude':0,'unit':'PT'},
                                'spaceBelow':{'magnitude':0,'unit':'PT'}},
                            'fields':'lineSpacing,spaceAbove,spaceBelow'}})
                for el in pe:
                    if 'textRun' not in el: continue
                    s,e=el['startIndex'],el['endIndex']
                    if e<=s: continue
                    if ri==0:
                        req.append({'updateTextStyle':{
                            'range':{'startIndex':s,'endIndex':e},
                            'textStyle':{'bold':True,
                                'fontSize':{'magnitude':8.5,'unit':'PT'},
                                'weightedFontFamily':{'fontFamily':'Roboto','weight':700},
                                'foregroundColor':{'color':{'rgbColor':white}}},
                            'fields':'bold,fontSize,weightedFontFamily,foregroundColor'}})
                    else:
                        req.append({'updateTextStyle':{
                            'range':{'startIndex':s,'endIndex':e},
                            'textStyle':{
                                'fontSize':{'magnitude':7.5,'unit':'PT'},
                                'weightedFontFamily':{'fontFamily':'Roboto','weight':400},
                                'foregroundColor':{'color':{'rgbColor':dark}}},
                            'fields':'fontSize,weightedFontFamily,foregroundColor'}})
print(json.dumps({'requests':req}))
PYEOF
)
NREQ=$(echo "$PHASE_E" | python3 -c "import json,sys;print(len(json.load(sys.stdin)['requests']))")
if [ "$NREQ" -gt 0 ]; then
  gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_E" 2>&1 | strip_noise > /dev/null
fi

# Phase F: color the "INTERNAL" H1 heading CE Blue. The markdown body emits
# `# INTERNAL` which Drive converts to a HEADING_1; this recolors its text
# run to CE Blue (#3573FF) so it reads as a clear production-side divider.
gws docs documents get --params "{\"documentId\":\"$DOC_ID\"}" 2>&1 | strip_noise > "$DOC_JSON"
PHASE_F=$(python3 <<PYEOF
import json
d=json.load(open('$DOC_JSON'))
blue={'red':$CE_BLUE_R,'green':$CE_BLUE_G,'blue':$CE_BLUE_B}
req=[]
for e in d['body']['content']:
    if 'paragraph' not in e:
        continue
    p=e['paragraph']
    if p.get('paragraphStyle',{}).get('namedStyleType','')!='HEADING_1':
        continue
    txt=''.join(el['textRun'].get('content','') for el in p.get('elements',[]) if 'textRun' in el)
    if txt.strip().upper()!='INTERNAL':
        continue
    for el in p.get('elements',[]):
        if 'textRun' not in el:
            continue
        s,en=el['startIndex'],el['endIndex']
        if en<=s:
            continue
        req.append({'updateTextStyle':{
            'range':{'startIndex':s,'endIndex':en},
            'textStyle':{'bold':True,
                'weightedFontFamily':{'fontFamily':'Roboto','weight':700},
                'foregroundColor':{'color':{'rgbColor':blue}}},
            'fields':'bold,weightedFontFamily,foregroundColor'}})
print(json.dumps({'requests':req}))
PYEOF
)
NREQ_F=$(echo "$PHASE_F" | python3 -c "import json,sys;print(len(json.load(sys.stdin)['requests']))")
if [ "$NREQ_F" -gt 0 ]; then
  gws docs documents batchUpdate --params "{\"documentId\":\"$DOC_ID\"}" --json "$PHASE_F" 2>&1 | strip_noise > /dev/null
fi
echo "COVER_OK https://docs.google.com/document/d/$DOC_ID/edit"
