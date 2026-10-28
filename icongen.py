import math
from PIL import Image, ImageDraw, ImageFilter
def _fish(S):
    # horizontal koi facing right, drawn on transparent layer S x S, centered
    L=Image.new("RGBA",(S,S),(0,0,0,0)); d=ImageDraw.Draw(L); c=S/2; u=S/100
    # tail
    d.polygon([(c-22*u,c),(c-44*u,c-20*u),(c-38*u,c),(c-44*u,c+20*u)],fill=(255,112,36,255))
    # dorsal + pelvic fins
    d.polygon([(c-8*u,c-17*u),(c+2*u,c-30*u),(c+14*u,c-17*u)],fill=(255,112,36,255))
    d.polygon([(c-6*u,c+15*u),(c+2*u,c+27*u),(c+12*u,c+15*u)],fill=(255,150,50,255))
    # body
    d.ellipse([c-30*u,c-19*u,c+36*u,c+19*u],fill=(255,190,36,255))
    # belly highlight
    hl=Image.new("RGBA",(S,S),(0,0,0,0)); ImageDraw.Draw(hl).ellipse([c-24*u,c+2*u,c+30*u,c+17*u],fill=(255,229,140,140)); L.alpha_composite(hl.filter(ImageFilter.GaussianBlur(u*2.5)))
    # koi patches (clipped to body)
    m=Image.new("L",(S,S),0); ImageDraw.Draw(m).ellipse([c-30*u,c-19*u,c+36*u,c+19*u],fill=255)
    p=Image.new("RGBA",(S,S),(0,0,0,0)); pd=ImageDraw.Draw(p)
    pd.ellipse([c-12*u,c-22*u,c+10*u,c-2*u],fill=(232,57,41,255)); pd.ellipse([c+12*u,c-6*u,c+26*u,c+8*u],fill=(232,57,41,255)); pd.ellipse([c-26*u,c-4*u,c-12*u,c+10*u],fill=(255,255,255,235))
    pa=Image.new("RGBA",(S,S),(0,0,0,0)); pa.paste(p,(0,0),m); L.alpha_composite(pa)
    # eye
    d=ImageDraw.Draw(L); d.ellipse([c+22*u,c-10*u,c+31*u,c-1*u],fill=(255,255,255,255)); d.ellipse([c+25*u,c-8*u,c+31*u,c-2*u],fill=(16,34,47,255)); d.ellipse([c+27*u,c-7.5*u,c+29*u,c-5.5*u],fill=(255,255,255,255))
    return L
def make(n, scale=1.0, transparent=False):
    S=n*2 if n<1024 else n*2
    Z=S; im=Image.new("RGBA",(Z,Z),(0,0,0,0)); u=Z/100
    if not transparent:
        bgd=ImageDraw.Draw(im)
        for y in range(Z):
            k=y/Z; bgd.line([(0,y),(Z,y)],fill=(int(30+(8-30)*k),int(150+(42-150)*k),int(190+(86-190)*k),255))
        sun=Image.new("RGBA",(Z,Z),(0,0,0,0)); sd=ImageDraw.Draw(sun); sd.ellipse([22*u,10*u,78*u,66*u],fill=(255,222,140,255)); 
        glow=sun.filter(ImageFilter.GaussianBlur(5*u)); glow.putalpha(glow.getchannel("A").point(lambda a:int(a*0.55))); im.alpha_composite(glow); im.alpha_composite(sun)
        wv=Image.new("RGBA",(Z,Z),(0,0,0,0)); wd=ImageDraw.Draw(wv)
        for i,(yy,col) in enumerate([(66,(30,124,168,255)),(74,(20,92,140,255)),(84,(10,58,102,255))]):
            pts=[(x,(yy+1.6*math.sin(x/Z*math.pi*(4+i)+i*1.7))*u) for x in range(0,Z+1,6)]
            wd.polygon(pts+[(Z,Z),(0,Z)],fill=col)
        im.alpha_composite(wv)
    art=Image.new("RGBA",(Z,Z),(0,0,0,0)); ad=ImageDraw.Draw(art)
    # fish rotated leaping
    fl=_fish(int(Z*0.74)).rotate(38,resample=Image.BICUBIC,expand=True)
    fx=int(Z*0.47-fl.width/2); fy=int(Z*0.43-fl.height/2)
    sh=Image.new("RGBA",art.size,(0,0,0,0)); sh.paste((0,0,0,60),(fx+int(u*1.2),fy+int(u*2.4)),fl.getchannel("A")); art.alpha_composite(sh.filter(ImageFilter.GaussianBlur(u*1.6)))
    art.alpha_composite(fl,(fx,fy))
    # line and hook near mouth (mouth ~ upper right of fish)
    mx,my=Z*0.47+math.cos(math.radians(-38))*Z*0.74*0.38, Z*0.43+math.sin(math.radians(-38))*Z*0.74*0.38
    ad=ImageDraw.Draw(art); lw=max(2,int(u*0.9))
    pts=[]
    for t in range(0,101):
        tt=t/100; x=Z*0.86+(mx+u*4-Z*0.86)*tt; y=-2*u+(my-u*4+2*u)*tt+math.sin(tt*math.pi)*u*(-5); pts.append((x,y))
    ad.line(pts,fill=(235,245,255,255),width=lw,joint="curve")
    ad.arc([mx-u*1.5,my-u*9,mx+u*5,my-u*2],20,250,fill=(235,245,255,255),width=lw)
    # splash droplets and ripples
    for (dx,dy,r) in [(-10,6,1.6),(-4,12,1.1),(14,10,1.4),(20,3,1.0),(-16,14,1.0)]:
        x=Z*0.46+dx*u*2.4; y=Z*0.74+dy*u*0.6; ad.ellipse([x-r*u,y-r*u,x+r*u,y+r*u],fill=(220,242,255,255))
    for k,(w,h) in enumerate([(42,7),(58,10)]):
        cx,cy=Z*0.46,Z*0.80; ad.ellipse([cx-w*u/2*1.15,cy-h*u/2,cx+w*u/2*1.15,cy+h*u/2],outline=(220,242,255,200-60*k),width=max(2,int(u*0.8)))
    if scale!=1.0:
        s2=int(Z*scale); art=art.resize((s2,s2),Image.LANCZOS); pad=Image.new("RGBA",(Z,Z),(0,0,0,0)); pad.alpha_composite(art,((Z-s2)//2,(Z-s2)//2)); art=pad
    im.alpha_composite(art)
    return im.resize((n,n),Image.LANCZOS)
if __name__=="__main__":
    make(1024).convert("RGB").save("icon.png"); make(1024,0.66,True).save("fg.png")
    # adaptive mask preview (circle)
    ic=make(512).convert("RGBA"); m=Image.new("L",(512,512),0); ImageDraw.Draw(m).ellipse([0,0,511,511],fill=255); ic.putalpha(m); ic.save("circle.png")
