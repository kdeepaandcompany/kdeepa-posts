# Original mascot "Tara Ma'am" — friendly tax teacher (flat vector). Poses: point, explain, think, happy.
SK="#F1BE95"; SKD="#D99A72"; HR="#2A1A16"; INK="#2A1A16"
OUT="var(--m-outfit,#E4572E)"; DUP="var(--m-dupatta,#F2B134)"; BRD="#FFFFFF"
def arm(x1,y1,x2,y2,x3,y3,w=26):
    return f'<path d="M{x1},{y1} Q{x2},{y2} {x3},{y3}" stroke="var(--m-sleeve,#C94422)" stroke-width="{w}" fill="none" stroke-linecap="round"/><circle cx="{x3}" cy="{y3}" r="15" fill="{SK}"/>'
def head(mouth='smile', eyes='open'):
    m={'smile':'<path d="M128,165 Q150,186 172,165" stroke="#7A2E25" stroke-width="5" fill="#B5473A" stroke-linecap="round"/>',
       'o':'<ellipse cx="150" cy="172" rx="9" ry="11" fill="#7A2E25"/>',
       'hmm':'<path d="M134,172 Q150,166 166,174" stroke="#7A2E25" stroke-width="5" fill="none" stroke-linecap="round"/>'}[mouth]
    e={'open':'<circle cx="127" cy="138" r="6" fill="#1b1b1b"/><circle cx="173" cy="138" r="6" fill="#1b1b1b"/><circle cx="129" cy="136" r="2" fill="#fff"/><circle cx="175" cy="136" r="2" fill="#fff"/>',
       'up':'<circle cx="131" cy="133" r="6" fill="#1b1b1b"/><circle cx="177" cy="133" r="6" fill="#1b1b1b"/>',
       'happy':'<path d="M118,140 Q127,130 136,140" stroke="#1b1b1b" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M164,140 Q173,130 182,140" stroke="#1b1b1b" stroke-width="5" fill="none" stroke-linecap="round"/>'}[eyes]
    return f'''
<ellipse cx="150" cy="128" rx="74" ry="76" fill="{HR}"/>
<circle cx="150" cy="52" r="30" fill="{HR}"/>
<rect x="136" y="185" width="28" height="30" rx="8" fill="{SKD}"/>
<circle cx="86" cy="140" r="12" fill="{SK}"/><circle cx="214" cy="140" r="12" fill="{SK}"/>
<circle cx="86" cy="156" r="5" fill="{DUP}"/><circle cx="214" cy="156" r="5" fill="{DUP}"/>
<ellipse cx="150" cy="138" rx="62" ry="64" fill="{SK}"/>
<path d="M88,120 Q100,66 150,68 Q200,66 212,120 Q190,92 150,96 Q112,92 88,120Z" fill="{HR}"/>
<circle cx="150" cy="112" r="4.5" fill="#C8102E"/>
<path d="M112,118 Q127,111 140,118" stroke="{HR}" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M160,118 Q173,111 188,118" stroke="{HR}" stroke-width="4" fill="none" stroke-linecap="round"/>
{e}
<circle cx="127" cy="138" r="19" fill="none" stroke="{INK}" stroke-width="4"/>
<circle cx="173" cy="138" r="19" fill="none" stroke="{INK}" stroke-width="4"/>
<path d="M146,137 Q150,133 154,137" stroke="{INK}" stroke-width="4" fill="none"/>
<path d="M150,145 Q146,156 152,158" stroke="{SKD}" stroke-width="4" fill="none" stroke-linecap="round"/>
<circle cx="112" cy="162" r="9" fill="#F28B82" opacity=".45"/><circle cx="188" cy="162" r="9" fill="#F28B82" opacity=".45"/>
{m}'''
def body():
    return f'''<path d="M88,232 Q150,205 212,232 L238,420 L62,420 Z" fill="{OUT}"/>
<path d="M126,212 L150,246 L174,212" fill="none" stroke="{BRD}" stroke-width="5" stroke-linejoin="round"/>
<path d="M104,222 Q140,300 120,420 L150,420 Q170,300 132,214Z" fill="{DUP}" opacity=".95"/>'''
POSES={
 'point': (arm(96,240,60,300,92,345)+arm(204,240,250,200,262,128)+'<line x1="262" y1="128" x2="292" y2="18" stroke="#6B3E26" stroke-width="7" stroke-linecap="round"/><circle cx="292" cy="18" r="6" fill="#F2B134"/>', 'smile','open'),
 'explain': (arm(96,240,46,260,42,212)+arm(204,240,254,260,258,212)+'<rect x="0" y="0" width="0" height="0"/>', 'o','open'),
 'think': (arm(96,240,70,330,118,326)+'<rect x="88" y="300" width="64" height="48" rx="6" fill="#0E7C84"/><rect x="96" y="306" width="48" height="36" rx="4" fill="#fff"/>'+arm(204,240,236,250,196,190), 'hmm','up'),
 'happy': (arm(96,240,40,190,58,110)+arm(204,240,260,190,242,110), 'smile','happy'),
}
for name,(arms,mouth,eyes) in POSES.items():
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 320 420">{body()}{arms if name!="think" else ""}{head(mouth,eyes)}{arms if name=="think" else ""}</svg>'
    if name=='think':  # hand to chin must be above head layer
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 320 420">{body()}{head(mouth,eyes)}{arms}</svg>'
    open(f'tara_{name}.svg','w').write(svg)
