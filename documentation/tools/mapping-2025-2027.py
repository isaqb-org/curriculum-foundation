#!/usr/bin/env python3
"""Generate the LG mapping diagram 2025.1 -> 2027.1 (used in CHANGELOG.md, "Trainer Notes").

Usage (from the repository root):
    python3 documentation/tools/mapping-2025-2027.py documentation/Mapping-2025-2027.svg
    rsvg-convert -z 2 documentation/Mapping-2025-2027.svg -o documentation/Mapping-2025-2027.png

To update: edit OLD (2025.1 LGs per section), NEW (only LGs whose status
differs from "unchanged", with a short note) and NEWSEC (new section headers).
Status codes: u=unchanged, c=changed, n=new, d=removed, m=moved/merged, v=vacant.
Arrows for moved/merged LGs are defined near the end (arrow(...) calls).
No dependencies beyond the Python standard library.
"""
import html, sys
# status: u=unchanged, c=changed, n=new, d=deleted, m=moved/merged away, v=vacant
OLD = [
 ("1 Basic Concepts · 120 min", [
  ("01-01","Definitions of Software Architecture","R1","u"),
  ("01-02","Goals and Benefits of SW Architecture","R1","u"),
  ("01-03","Long-term Impact of SW Architecture","R3","u"),
  ("01-04","Tasks and Responsibilities of Architects","R1","u"),
  ("01-05","Distinction from other Architectural Domains","R3","d"),
  ("01-06","Role of Architects vs. Other Stakeholders","R1","u"),
  ("01-07","Importance of Data and Data Models","R2","u")]),
 ("2 Requirements and Constraints · 180 min", [
  ("02-01","Understand Stakeholder Concerns","R1,R3","u"),
  ("02-02","Clarify Requirements and Constraints","R1-R3","u"),
  ("02-03","Qualities of a Software System","R1","u"),
  ("02-04","Formulate Requirements on Qualities","R1-R3","u"),
  ("02-05","Prefer Explicit Statements over Assumptions","R1","u")]),
 ("3 Design and Development · 360 min", [
  ("03-01","Fulfilling Requirements through Architecture","R1","u"),
  ("03-02","Design Software Architectures","R1","u"),
  ("03-03","Approaches and Heuristics","R1,R3","u"),
  ("03-04","Design Principles","R1-R3","u"),
  ("03-05","Feedback Loops and Risks","R1,R2","u"),
  ("03-06","Manage Dependencies","R1","u"),
  ("03-07","Design and Define Interfaces","R1-R3","u"),
  ("03-08","Important Architectural Patterns","R1,R3","u"),
  ("03-09","Important Design Patterns","R3","m"),
  ("03-10","Cross-Cutting Concerns","R1","u"),
  ("03-11","Principles of Software Deployment","R3","u"),
  ("03-12","Challenges of Distributed Systems","R3","d")]),
 ("4 Specification and Communication · 240 min", [
  ("04-01","Requirements of Technical Documentation","R1","u"),
  ("04-02","Describe and Communicate Architectures","R1-R3","u"),
  ("04-03","Notations/Models","R2-R3","u"),
  ("04-04","Learning Goal not Found","R3","u"),
  ("04-05","Architectural Views","R1","u"),
  ("04-06","Document Interfaces","R1","u"),
  ("04-07","Document Cross-Cutting Concerns","R2","u"),
  ("04-08","Architectural Decisions","R1-R2","u"),
  ("04-09","Additional Resources and Tools","R3","u")]),
 ("5 Analysis and Assessment · 90 min", [
  ("05-01","Reasons for Architecture Analysis","R1","m"),
  ("05-02","Analyze the Qualities of a System","R1,R3","d"),
  ("05-03","Conformance to Architectural Decisions","R2","d")]),
 ("6 Examples · 90 min", [
  ("06-01","Requirements, Constraints, Solutions","R3","u"),
  ("06-02","Technical Implementation of a Solution","R3","u")]),
]
NEW = {
 "01-05":("— vacant —","","v",""),
 "02-05":("Prefer Explicit Statements over Assumptions","R1,R2","c","+ write explicit specifications (R2)"),
 "03-03":("Approaches and Heuristics","R1,R3","c","views ≠ method; −global analysis, −MDA; +2 approaches (R3)"),
 "03-04":("Design Principles","R1-R3","c","DRY ↑R2; + illegal states unrepresentable (R2); −SOLID"),
 "03-06":("Manage Dependencies","R1","c","Dependency Injection ↑R1; incoming/outgoing deps"),
 "03-08":("Important Patterns","R1,R3","c","DI now R1; design patterns merged in (R3)"),
 "03-09":("Analyze Architecture","R1","n","from former 05-01"),
 "03-12":None,
 "04-02":("Describe and Communicate Architectures","R1-R3","c","reworded; −harmonise contributions (R1)"),
 "04-03":("Notations/Models","R2-R3","c","read + create UML, choose notation (R2)"),
 "04-05":("Architectural Views","R1","c","example extra views removed (R3)"),
 "04-09":("Additional Resources and Tools","R2","c","↑R2 (arc42, C4); −ISO 42010"),
 "05-01":("Deciding on the Use of AI","R1,R2","n",""),
 "05-02":("Verification of AI-generated Artifacts","R1,R2","n",""),
 "05-03":("Risks and Externalities of AI","R2,R3","n",""),
}
NEWSEC = {0:"1 Basic Concepts · 120 min",1:"2 Requirements and Constraints · 180 min",2:"3 Design and Development · 360 min",
          3:"4 Specification and Communication · 240 min",4:"5 Use and Risks of AI · 60 min",5:"6 Examples · 90 min  ·  MUST be covered in training"}
C = {"u":("#f4f5f7","#c4c8cf","#55595f"),"c":("#fff4d6","#d9a200","#3d3000"),"n":("#dcf3e1","#2e9e4f","#123d1f"),
     "d":("#fbe1e3","#cc3344","#7a1622"),"m":("#e3ecfd","#3b6fd8","#173a80"),"v":("#ffffff","#c4c8cf","#9aa0a6")}
X0,BW,GUT,NW = 24,350,120,330
X1 = X0+BW+GUT; XN = X1+BW+14
RH,SH,TOP = 27,30,96
W = XN+NW+16
out=[]; y=TOP; rowpos_old={}; rowpos_new={}
def esc(s): return html.escape(s)
def box(x,y,num,title,r,st,strike=False):
    f,s,t = C[st]
    out.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{RH-5}" rx="4" fill="{f}" stroke="{s}" stroke-width="{1.6 if st!="u" else 1}"/>')
    deco = ' text-decoration="line-through"' if strike else ''
    out.append(f'<text x="{x+8}" y="{y+15.5}" font-size="12" fill="{t}"><tspan font-weight="700">{num}</tspan><tspan dx="8"{deco}>{esc(title)}</tspan></text>')
    if r: out.append(f'<text x="{x+BW-8}" y="{y+15.5}" font-size="11" text-anchor="end" fill="{t}" opacity="0.8">{r}</text>')
for i,(sec,lgs) in enumerate(OLD):
    sec_changed = i==4
    for (x,label,col) in ((X0,sec,"#d9dce1" if not sec_changed else "#f3c6cb"),(X1,NEWSEC[i],"#d9dce1" if i not in (4,5) else ("#bfe6c9" if i==4 else "#ffe7a3"))):
        out.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{SH-6}" rx="4" fill="{col}"/>')
        out.append(f'<text x="{x+8}" y="{y+16.5}" font-size="12.5" font-weight="700" fill="#24292f">{esc(label)}</text>')
    y+=SH
    for (num,title,r,st) in lgs:
        box(X0,y,num,title,r,st,strike=(st=="d"))
        rowpos_old[num]=y
        key=num
        if i==4:  # section 5 replaced entirely
            t,rr,s2,note = NEW[num]
            box(X1,y,num,t,rr,s2); rowpos_new[num]=y
        elif key in NEW:
            v=NEW[key]
            if v is not None:
                t,rr,s2,note=v
                box(X1,y,num,t,rr,s2); rowpos_new[num]=y
                if note: out.append(f'<text x="{XN}" y="{y+15.5}" font-size="11" fill="#3d3000" font-style="italic">{esc(note)}</text>')
        else:
            box(X1,y,num,title,r,"u"); rowpos_new[num]=y
        if num=="03-12": out.append(f'<text x="{XN}" y="{y+15.5}" font-size="11" fill="#7a1622" font-style="italic">03-12 removed, moved to "FL II" by FLWG decision</text>')
        if st=="d":
            lab = {"01-05":"removed","03-12":"removed","05-02":"removed","05-03":"removed"}[num]
            out.append(f'<text x="{X0+BW+8}" y="{y+15.5}" font-size="11" fill="#cc3344" font-weight="600">✕ {lab}</text>')
        if i==4:
            out.append(f'<text x="{XN}" y="{y+15.5}" font-size="11" fill="#123d1f" font-style="italic">new</text>')
        y+=RH
    y+=8
H=y+70
# arrows
def arrow(y1,y2,label,lx,ly):
    xa=X0+BW+2; xb=X1-4; a=y1+11; b=y2+11
    out.append(f'<path d="M{xa},{a} C{xa+70},{a} {xb-70},{b} {xb},{b}" fill="none" stroke="#3b6fd8" stroke-width="2" marker-end="url(#ah)"/>')
    out.append(f'<text x="{lx}" y="{ly}" font-size="10.5" fill="#173a80" font-weight="600" text-anchor="middle">{label}</text>')
arrow(rowpos_old["03-09"],rowpos_new["03-08"],"merged",X0+BW+30,rowpos_old["03-09"]+30)
arrow(rowpos_old["05-01"],rowpos_new["03-09"],"moved",X0+BW+28,(rowpos_old["05-01"]+rowpos_new["03-09"])/2+18)
# legend
ly=H-46; lx=X0
items=[("u","unchanged (editorial only)"),("c","content or R-level changed"),("n","new"),("d","removed"),("m","moved / merged")]
for st,lab in items:
    f,s,t=C[st]
    out.append(f'<rect x="{lx}" y="{ly}" width="22" height="14" rx="3" fill="{f}" stroke="{s}" stroke-width="1.4"/>')
    out.append(f'<text x="{lx+28}" y="{ly+11.5}" font-size="11.5" fill="#24292f">{lab}</text>'); lx+=60+len(lab)*6.3
out.append(f'<text x="{X0}" y="{ly+34}" font-size="10.5" fill="#6a737d">Titles shortened. R-levels as in the LG titles. Details: CHANGELOG.md, "Trainer Notes". Source: 2025.1-rev2 vs. 2027.1-RC1 (+ RC-2 cleanup).</text>')
hdr=[f'<text x="{X0}" y="34" font-size="20" font-weight="700" fill="#24292f">CPSA-F Curriculum: 2025.1 → 2027.1-RC1</text>',
     f'<text x="{X0}" y="58" font-size="12.5" fill="#55595f">Mapping of learning goals (LG), with the changes relevant for trainings</text>',
     f'<text x="{X0}" y="86" font-size="13" font-weight="700" fill="#24292f">2025.1 (rev2) · 1080 min</text>',
     f'<text x="{X1}" y="86" font-size="13" font-weight="700" fill="#24292f">2027.1-RC1 · 1050 min</text>',
     f'<text x="{XN}" y="86" font-size="13" font-weight="700" fill="#24292f">What changed</text>']
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">
<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#3b6fd8"/></marker></defs>
<rect width="100%" height="100%" fill="#ffffff"/>
{chr(10).join(hdr)}
{chr(10).join(out)}
</svg>'''
open(sys.argv[1],"w").write(svg)
