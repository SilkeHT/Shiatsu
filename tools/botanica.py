import math, sys
OUT = sys.argv[1]
INK="#231A17"; OLIVA="#8C8A3A"; OLIVA_CL="#C9C27A"; ROSA="#B4485A"; SALMON="#EE9090"; AMBAR="#F7A93B"; BEIGE="#F1E3D6"; CREMA="#FCF0EA"; NARANJA="#F07A21"

def leaf(x,y,ln,w,ang,fill=OLIVA_CL,stroke=OLIVA):
    veins="".join(f'<path d="M0,{-ln*t:.1f} L{s*w*0.28:.1f},{-ln*(t+0.14):.1f}" />' for t in (0.25,0.45,0.65) for s in (-1,1))
    return (f'<g transform="translate({x},{y}) rotate({ang})">'
            f'<path d="M0,0 Q{w/2:.1f},{-ln*0.45:.1f} 0,{-ln} Q{-w/2:.1f},{-ln*0.45:.1f} 0,0 Z" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
            f'<g stroke="{stroke}" stroke-width=".6" fill="none"><path d="M0,0 L0,{-ln*0.92:.1f}"/>{veins}</g></g>')

def pompon(cx,cy,r,c1=SALMON,c2=ROSA,n=72):
    s=[]
    for i in range(n):
        a=2*math.pi*i/n; rr=r*(0.82 if i%2 else 1)
        s.append(f'<line x1="{cx+math.cos(a)*r*0.22:.1f}" y1="{cy+math.sin(a)*r*0.22:.1f}" x2="{cx+math.cos(a)*rr:.1f}" y2="{cy+math.sin(a)*rr:.1f}" stroke="{c1 if i%2 else c2}" stroke-width="1.1" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.22:.1f}" fill="{AMBAR}" stroke="{INK}" stroke-width=".8"/>')
    for i in range(10):
        a=2*math.pi*i/10
        s.append(f'<circle cx="{cx+math.cos(a)*r*0.12:.1f}" cy="{cy+math.sin(a)*r*0.12:.1f}" r=".9" fill="{INK}"/>')
    return "".join(s)

def flor(cx,cy,r,fill=SALMON,stroke=ROSA,n=8,inner=ROSA):
    s=[]
    def petals(rad,rot,f,st):
        p=f'M0,0 C{rad*0.3:.1f},{-rad*0.2:.1f} {rad*0.32:.1f},{-rad*0.8:.1f} 0,{-rad} C{-rad*0.32:.1f},{-rad*0.8:.1f} {-rad*0.3:.1f},{-rad*0.2:.1f} 0,0 Z'
        v=f'M0,{-rad*0.15:.1f} L0,{-rad*0.85:.1f} M0,{-rad*0.2:.1f} L{rad*0.1:.1f},{-rad*0.75:.1f} M0,{-rad*0.2:.1f} L{-rad*0.1:.1f},{-rad*0.75:.1f}'
        for i in range(n):
            s.append(f'<g transform="translate({cx},{cy}) rotate({rot+360*i/n:.1f})"><path d="{p}" fill="{f}" stroke="{st}" stroke-width="1"/><path d="{v}" stroke="{st}" stroke-width=".6" fill="none"/></g>')
    petals(r,0,fill,stroke); petals(r*0.62,180/n,inner,INK)
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.18:.1f}" fill="{AMBAR}" stroke="{INK}" stroke-width=".8"/>')
    for i in range(12):
        a=2*math.pi*i/12
        s.append(f'<line x1="{cx+math.cos(a)*r*0.2:.1f}" y1="{cy+math.sin(a)*r*0.2:.1f}" x2="{cx+math.cos(a)*r*0.32:.1f}" y2="{cy+math.sin(a)*r*0.32:.1f}" stroke="{INK}" stroke-width=".6"/><circle cx="{cx+math.cos(a)*r*0.34:.1f}" cy="{cy+math.sin(a)*r*0.34:.1f}" r="1" fill="{INK}"/>')
    return "".join(s)

def crisantemo(cx,cy,r,fill=OLIVA_CL,stroke=OLIVA,n=22):
    s=[]
    for layer,(rad,rot) in enumerate(((r,0),(r*0.72,180/n),(r*0.45,0))):
        for i in range(n):
            w=rad*0.11
            s.append(f'<g transform="translate({cx},{cy}) rotate({rot+360*i/n:.1f})"><path d="M0,{-rad*0.15:.1f} Q{w:.1f},{-rad*0.6:.1f} 0,{-rad} Q{-w:.1f},{-rad*0.6:.1f} 0,{-rad*0.15:.1f} Z" fill="{fill if layer!=1 else BEIGE}" stroke="{stroke}" stroke-width=".8"/></g>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.16:.1f}" fill="{INK}"/>')
    for i in range(8):
        a=2*math.pi*i/8
        s.append(f'<circle cx="{cx+math.cos(a)*r*0.08:.1f}" cy="{cy+math.sin(a)*r*0.08:.1f}" r="1" fill="{AMBAR}"/>')
    return "".join(s)

def semilla(cx,cy,r):
    s=[f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width=".5" stroke-dasharray="1 2"/>']
    for i in range(28):
        a=2*math.pi*i/28
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.cos(a)*r:.1f}" y2="{cy+math.sin(a)*r:.1f}" stroke="{INK}" stroke-width=".4"/><circle cx="{cx+math.cos(a)*r:.1f}" cy="{cy+math.sin(a)*r:.1f}" r="1.3" fill="{ROSA}"/>')
    return "".join(s)

def jarron(cabeza):
    s=[]
    cols=[OLIVA,SALMON,INK,ROSA,OLIVA]
    for i,c in enumerate(cols):
        d=i*5
        s.append(f'<path d="M{45+d},178 L{45+d},340 Q{45+d},{392-d} 80,{392-d} Q{115-d},{392-d} {115-d},340 L{115-d},178" fill="{BEIGE if i==len(cols)-1 else "none"}" stroke="{c}" stroke-width="1"/>')
    s.append(f'<path d="M80,186 L80,370" stroke="{OLIVA}" stroke-width="1"/>')
    for k,y in enumerate(range(196,368,18)):
        s.append(leaf(80,y,13,7,(-55 if k%2 else 55)))
    s.append(f'<ellipse cx="80" cy="178" rx="36" ry="6" fill="{CREMA}" stroke="{INK}" stroke-width="1"/>')
    # tallos
    s.append(f'<path d="M80,176 C80,140 78,110 80,92" stroke="{INK}" stroke-width="1.2" fill="none"/>')
    s.append(f'<path d="M78,172 C62,150 44,140 34,124" stroke="{INK}" stroke-width="1" fill="none"/>')
    s.append(f'<path d="M82,172 C100,150 116,138 128,118" stroke="{INK}" stroke-width="1" fill="none"/>')
    s.append(leaf(80,170,46,22,-38)); s.append(leaf(80,170,46,22,38))
    s.append(leaf(70,150,30,14,-70)); s.append(leaf(92,148,30,14,72))
    if cabeza=="pompon":
        s.append(pompon(80,64,36)); s.append(semilla(32,114,13)); s.append(flor(130,108,14,fill=BEIGE,stroke=OLIVA,inner=SALMON))
    else:
        s.append(flor(80,66,36)); s.append(crisantemo(32,114,15)); s.append(semilla(130,108,13))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 400">{"".join(s)}</svg>'

def flor_sola():
    s=[leaf(0,0,62,26,a) for a in (45,135,225,315)]
    s.append(flor(0,0,46))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 140 140">{"".join(s)}</svg>'

def crisantemo_solo():
    s=[f'<path d="M0,40 C2,60 -2,80 0,96" stroke="{INK}" stroke-width="1.1" fill="none"/>', leaf(0,92,34,15,-40), leaf(0,92,34,15,40)]
    s.append(crisantemo(0,0,42))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -48 100 146">{"".join(s)}</svg>'

open(f"{OUT}/botanica-jarron-a.svg","w").write(jarron("pompon"))
open(f"{OUT}/botanica-jarron-b.svg","w").write(jarron("flor"))
open(f"{OUT}/botanica-flor.svg","w").write(flor_sola())
open(f"{OUT}/botanica-crisantemo.svg","w").write(crisantemo_solo())
print("ok")
