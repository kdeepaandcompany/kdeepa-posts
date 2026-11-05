# Original mascot "Ravi Sir" — friendly tax expert in coat-pant (flat vector). Poses: point, explain, think, happy.
SK="#E8B48C"; SKD="#C98F68"; HR="#1E1512"
COAT="var(--r-coat,#1F3A68)"; SLV="var(--r-sleeve,#172C50)"; PANT="var(--r-pant,#3A3F4A)"; TIE="var(--r-tie,#E4572E)"
def arm(x1,y1,x2,y2,x3,y3):
    return (f'<path d="M{x1},{y1} Q{x2},{y2} {x3},{y3}" stroke="{SLV}" stroke-width="28" fill="none" stroke-linecap="round"/>'
            f'<circle cx="{x3}" cy="{y3}" r="15" fill="{SK}"/>')
def head(mouth,eyes):
    m={'smile':'<path d="M130,168 Q150,186 170,168" stroke="#6B2A22" stroke-width="5" fill="#A8413A" stroke-linecap="round"/>',
       'o':'<ellipse cx="150" cy="174" rx="8" ry="10" fill="#6B2A22"/>',
       'hmm':'<path d="M136,174 Q150,168 164,176" stroke="#6B2A22" stroke-width="5" fill="none" stroke-linecap="round"/>'}[mouth]
    e={'open':'<circle cx="128" cy="138" r="6.5" fill="#1b1b1b"/><circle cx="172" cy="138" r="6.5" fill="#1b1b1b"/><circle cx="130" cy="136" r="2" fill="#fff"/><circle cx="174" cy="136" r="2" fill="#fff"/>',
       'up':'<circle cx="132" cy="133" r="6.5" fill="#1b1b1b"/><circle cx="176" cy="133" r="6.5" fill="#1b1b1b"/>',
       'happy':'<path d="M119,140 Q128,130 137,140" stroke="#1b1b1b" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M163,140 Q172,130 181,140" stroke="#1b1b1b" stroke-width="5" fill="none" stroke-linecap="round"/>'}[eyes]
    return f'''
<rect x="136" y="186" width="28" height="30" rx="8" fill="{SKD}"/>
<circle cx="88" cy="142" r="12" fill="{SK}"/><circle cx="212" cy="142" r="12" fill="{SK}"/>
<ellipse cx="150" cy="140" rx="60" ry="64" fill="{SK}"/>
<path d="M88,132 Q84,72 140,70 Q206,64 214,128 Q204,100 176,98 Q150,92 118,104 Q100,110 92,140Z" fill="{HR}"/>
<path d="M112,116 Q126,108 140,114" stroke="{HR}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M160,114 Q174,108 188,116" stroke="{HR}" stroke-width="6" fill="none" stroke-linecap="round"/>
{e}
<path d="M150,146 Q145,158 152,160" stroke="{SKD}" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M128,160 Q150,152 172,160 Q160,166 150,162 Q140,166 128,160Z" fill="{HR}"/>
{m}'''
def body():
    return f'''
<rect x="104" y="400" width="40" height="130" rx="10" fill="{PANT}"/><rect x="156" y="400" width="40" height="130" rx="10" fill="{PANT}"/>
<ellipse cx="120" cy="534" rx="30" ry="12" fill="#1b1b1b"/><ellipse cx="180" cy="534" rx="30" ry="12" fill="#1b1b1b"/>
<path d="M86,236 Q150,206 214,236 L222,420 L78,420 Z" fill="{COAT}"/>
<path d="M126,214 L150,330 L174,214 Z" fill="#fff"/>
<path d="M144,226 L156,226 L160,300 L150,316 L140,300 Z" fill="{TIE}"/>
<path d="M140,214 L150,228 L160,214 Z" fill="{TIE}"/>
<path d="M120,214 L150,330 L132,300 L112,236Z" fill="{SLV}"/><path d="M180,214 L150,330 L168,300 L188,236Z" fill="{SLV}"/>
<circle cx="150" cy="360" r="5" fill="#E7C873"/><circle cx="150" cy="390" r="5" fill="#E7C873"/>
<rect x="176" y="262" width="26" height="6" rx="2" fill="#fff" opacity=".9"/>'''
POSES={
 'point': (arm(94,244,58,310,90,360)+arm(206,244,252,204,262,132)+'<line x1="262" y1="132" x2="292" y2="22" stroke="#6B3E26" stroke-width="7" stroke-linecap="round"/><circle cx="292" cy="22" r="6" fill="#F2B134"/>','smile','open',False),
 'explain': (arm(94,244,44,264,40,214)+arm(206,244,256,264,260,214),'o','open',False),
 'think': (arm(94,244,66,330,112,330)+'<rect x="82" y="304" width="66" height="50" rx="6" fill="#0E7C84"/><rect x="90" y="310" width="50" height="38" rx="4" fill="#fff"/>'+arm(206,244,238,252,196,192),'hmm','up',True),
 'happy': (arm(94,244,38,194,56,114)+arm(206,244,262,194,244,114),'smile','happy',False),
}
for n,(a,mo,ey,front) in POSES.items():
    inner = body()+head(mo,ey)+a if front else body()+a+head(mo,ey)
    open(f'ravi_{n}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 0 320 560">{inner}</svg>')
