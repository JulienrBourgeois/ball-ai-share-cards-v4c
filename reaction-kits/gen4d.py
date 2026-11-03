# v4d: special kits (reaction / athleticism) with distinct bottom visuals; reuses v4 + v4c chrome
import os,sys,math,json
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(HERE,'../pack-v4c'));sys.path.insert(0,os.path.join(HERE,'../pack-v4'))
import gen4 as B;import gen4c as C
os.chdir(HERE)
from PIL import Image,ImageDraw,ImageFilter
G=B.G;f=B.f
ATH=G.hx('#F43F5E');DRB=G.hx('#22D3EE')
def glow(im,cx,cy,r,col,a=160):
    g=Image.new('RGBA',im.size,(0,0,0,0));ImageDraw.Draw(g).ellipse([cx-r*1.6,cy-r*1.6,cx+r*1.6,cy+r*1.6],fill=col+(a,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(r*.7)))
def draw_orbs(im,box,res,cols,u,rts=None,acc=ATH):
    x0,y0,x1,y1=box;B.glass(im,box,24*u,tint=(14,18,28,125));n=len(res);w=x1-x0
    top=y0+16*u
    if rts:  # sparkline of last-N reaction times
        dr=ImageDraw.Draw(im,'RGBA');sx0,sx1,sy0,sy1=x0+22*u,x1-22*u,top,top+40*u;lo,hi=min(rts),max(rts)
        pts=[(sx0+(sx1-sx0)*i/(len(rts)-1),sy1-(sy1-sy0)*(hi-v)/(hi-lo+1e-9)) for i,v in enumerate(rts)]  # faster = higher
        dr.text((sx0,sy0-2*u),'REACTION TIME · LAST %d'%len(rts),font=f('Bold',int(11*u)),fill=(255,255,255,150))
        dr.line(pts,fill=acc+(255,),width=int(3*u),joint='curve');bx,by=min(pts,key=lambda p:p[1]);dr.ellipse([bx-5*u,by-5*u,bx+5*u,by+5*u],fill='white')
        top=sy1+10*u
    r=min((w-44*u)/n*.36,30*u);cy=(top+y1)/2;step=(w-44*u)/n
    for i,h in enumerate(res):
        cx=x0+22*u+step*(i+.5);c=cols[i%len(cols)]
        if h:
            glow(im,cx,cy,r,c);dr=ImageDraw.Draw(im,'RGBA')
            dr.ellipse([cx-r-6*u,cy-r-6*u,cx+r+6*u,cy+r+6*u],outline=c+(220,),width=int(3*u))
            dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c);dr.ellipse([cx-r*.55,cy-r*.65,cx-r*.05,cy-r*.2],fill=(255,255,255,120))
        else:
            dr=ImageDraw.Draw(im,'RGBA');dr.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(255,255,255,90),width=int(2.5*u),fill=(255,255,255,12))
            k=r*.4;dr.line([cx-k,cy-k,cx+k,cy+k],fill=(255,255,255,150),width=int(3*u));dr.line([cx-k,cy+k,cx+k,cy-k],fill=(255,255,255,150),width=int(3*u))
def cone(dr,cx,base,h,lit,u):
    o=(255,122,26) if lit else (110,110,118);s=(255,255,255) if lit else (170,170,176);bw=h*.95
    dr.rounded_rectangle([cx-bw/2,base-h*.12,cx+bw/2,base],radius=4*u,fill=o)
    tw,bw2=h*.12,h*.62;tp=base-h
    def x(t,side): return cx+side*(tw/2+(bw2-tw)/2*t)
    dr.polygon([(x(0,-1),tp),(x(0,1),tp),(x(1,1),base-h*.12),(x(1,-1),base-h*.12)],fill=o)
    for t0,t1 in[(.32,.46),(.62,.76)]:
        dr.polygon([(x(t0,-1),tp+(h*.88)*t0),(x(t0,1),tp+(h*.88)*t0),(x(t1,1),tp+(h*.88)*t1),(x(t1,-1),tp+(h*.88)*t1)],fill=s)
def draw_cones(im,box,lit,u,label=None):
    x0,y0,x1,y1=box;B.glass(im,box,24*u,tint=(14,18,28,125));n=len(lit);w=x1-x0;step=(w-40*u)/n;h=min(y1-y0-46*u,step*1.05);base=y1-22*u
    dr=ImageDraw.Draw(im,'RGBA')
    # lateral lane + shuffle arrows
    dr.line([x0+22*u,base+6*u,x1-22*u,base+6*u],fill=(255,255,255,70),width=int(2*u))
    for i,l in enumerate(lit):
        cx=x0+20*u+step*(i+.5)
        if l: glow(im,cx,base-h*.45,h*.35,(255,122,26),120)
        cone(ImageDraw.Draw(im,'RGBA'),cx,base,h,l,u)
    dr=ImageDraw.Draw(im,'RGBA')
    if label: dr.text((x0+22*u,y0+12*u),label,font=f('Bold',int(11*u)),fill=(255,255,255,160))
    fo=f('Black',int(14*u));t='◀ ▶';dr.text((x1-22*u-dr.textlength('<  >',font=fo),y0+10*u),'<  >',font=fo,fill=(255,140,60,230))
def draw_cadence_ring(im,cx,cy,R,frac,val,lab,acc,u,ticks=60,hot=None):
    dr=ImageDraw.Draw(im,'RGBA');bb=[cx-R,cy-R,cx+R,cy+R];wd=int(16*u)
    glow(im,cx,cy,R*.55,acc,70);dr=ImageDraw.Draw(im,'RGBA')
    dr.ellipse([cx-R+wd,cy-R+wd,cx+R-wd,cy+R-wd],fill=(12,16,24,150))
    dr.arc(bb,0,360,fill=(255,255,255,45),width=wd);dr.arc(bb,-90,-90+360*frac,fill=acc+(255,),width=wd)
    ex=cx+R*math.cos(math.radians(-90+360*frac))-0;ey=cy+R*math.sin(math.radians(-90+360*frac))
    for i in range(ticks):  # per-second hash marks (cadence), brighter = hotter 10s
        ang=math.radians(-90+360*i/ticks);r0,r1=R+wd*.2+6*u,R+wd*.2+(14*u if hot and hot[0]<=i<hot[1] else 9*u)
        c=acc+(255,) if hot and hot[0]<=i<hot[1] else (255,255,255,110)
        dr.line([cx+r0*math.cos(ang),cy+r0*math.sin(ang),cx+r1*math.cos(ang),cy+r1*math.sin(ang)],fill=c,width=int(2*u))
    dr.ellipse([ex-wd*.75+wd/2-wd/2,ey-wd*.75,ex+wd*.75,ey+wd*.75],fill='white')
    fo=f('Black',int(R*.62));tw=dr.textlength(val,font=fo);dr.text((cx-tw/2,cy-fo.size*.62),val,font=fo,fill='white')
    fl=f('Bold',int(R*.13));tw=dr.textlength(lab,font=fl);dr.text((cx-tw/2,cy+fo.size*.42),lab,font=fl,fill=acc+(255,))
# ---- mock data ----
def seq(n,hits,seed):
    import random;r=random.Random(seed);s=[1]*hits+[0]*(n-hits);r.shuffle(s);return s
OC=[G.hx(c) for c in['#F43F5E','#22D3EE','#FACC15','#2DD4A7','#A855F7','#FF8A1F']]
def rts(seed,avg,best,n=16):
    import random;r=random.Random(seed);v=[max(best,int(r.gauss(avg,45))) for _ in range(n)];v[r.randrange(n)]=best;return v
KITS=[
 dict(title='Reaction',kit='orbs',cat='athleticism',acc=ATH,hero=('SCORE','980'),orbs=seq(10,8,1),cols=OC,rts=rts(1,340,201),
      tiles=[('HITS','41/50'),('AVG RT','340ms'),('BEST RT','201ms'),('STREAK','8'),('TIME','2:10'),('CLEAN','82%')]),
 dict(title='Ordered Reaction',kit='orbs',cat='athleticism',acc=ATH,hero=('SCORE','1368'),orbs=[1,1,1,1,0,1,1,1,1,1],cols=OC,numbered=True,rts=rts(2,312,184),
      tiles=[('HITS','54/60'),('AVG RT','312ms'),('BEST RT','184ms'),('STREAK','12'),('TIME','2:48'),('CLEAN','90%')]),
 dict(title='Single Target',kit='orbs',cat='athleticism',acc=DRB,hero=('HITS','38/45'),orbs=seq(9,8,3),cols=[DRB],rts=rts(3,290,160),
      tiles=[('SCORE','720'),('AVG RT','290ms'),('BEST RT','160ms'),('CLEAN','84%'),('TIME','1:55')]),
 dict(title='Double Target',kit='orbs',cat='athleticism',acc=DRB,hero=('HITS','52/70'),orbs=seq(10,7,4),cols=[DRB,ATH],rts=rts(4,355,190),
      tiles=[('SCORE','610'),('AVG RT','355ms'),('BEST RT','190ms'),('CLEAN','74%'),('TIME','2:20')]),
 dict(title='Lateral Shuffle',kit='cones',cat='athleticism',acc=G.hx('#FF8A1F'),hero=('REPS','86'),cones=[1,1,1,0,1],
      tiles=[('SCORE','430'),('CLEAN','94%'),('BEST SPLIT','0.82s'),('DIR CHANGES','42'),('TIME','1:00')]),
 dict(title='Jumping Jacks',kit='ring',cat='athleticism',acc=ATH,hero=('REPS','68'),frac=1.0,goal='60s GOAL ✓',hot=(20,30),
      tiles=[('AVG CADENCE','72/min'),('BEST 10s','14'),('GOAL','60s'),('TIME','1:00')]),
 dict(title='High Knees',kit='ring',cat='athleticism',acc=ATH,hero=('REPS','94'),frac=1.0,hot=(40,50),
      tiles=[('AVG CADENCE','96/min'),('BEST 10s','18'),('GOAL','60s'),('TIME','1:00')]),
]
def card(k,W,H,u,bh,thumb=False):
    x=dict(title=k['title'],category=k['cat'],id=k['title']);a=k['acc']
    bn,fx={'orbs':('athlete-playground',.33),'cones':('court-portrait',.5),'ring':('ball-hoop-sunset',.5)}[k['kit']]
    im=B.photo(bn,fx,W,H);C.brand(im,x,u,a,W,bh);M=(18 if thumb else 20)*u;hl,hv=k['hero'];T=k['tiles']
    if k['kit']=='ring':
        if thumb:
            R=130*u;cx=M+R+22*u;cy=H-M-R-22*u;draw_cadence_ring(im,cx,cy,R,k['frac'],hv,hl,a,u,hot=k['hot'])
            rx=cx+R+40*u;B.grid(im,T,rx,cy-R-10*u,W-M-rx,2*R+20*u,1,8*u,a,u,26,60*u)
        else:
            gh=2*78*u+10*u;ty=H-M-gh;R=150*u;cy=ty-30*u-R;cx=W/2
            draw_cadence_ring(im,cx,cy,R,k['frac'],hv,hl,a,u,hot=k['hot'])
            dr=ImageDraw.Draw(im,'RGBA');fo=f('Bold',int(13*u))
            dr.text((M+6*u,cy-R),'60s',font=f('Black',int(30*u)),fill='white');dr.text((M+6*u,cy-R+36*u),'GOAL ✓' if True else '',font=fo,fill=a+(255,))
            t='HOT 10s';dr.text((W-M-6*u-dr.textlength(t,font=fo),cy-R+36*u),t,font=fo,fill=a+(255,));t2=T[1][1]+' reps'
            dr.text((W-M-6*u-dr.textlength(t2,font=f('Black',int(30*u))),cy-R),t2,font=f('Black',int(30*u)),fill='white')
            B.grid(im,T,M,ty,W-2*M,gh,2,10*u,a,u,34,78*u)
    else:
        n=len(T);cols=3 if not thumb else min(5,n)
        if thumb: T=T[:5];cols=len(T);gh=70*u
        else: gh=(2*72*u+10*u) if n>3 else 72*u
        ty=H-M-gh;vh=(150 if thumb else (200 if k['kit']=='orbs' else 190))*u;vy=ty-12*u-vh
        box=(M,vy,W-M,vy+vh)
        if k['kit']=='orbs':
            draw_orbs(im,box,k['orbs'],k['cols'],u,None if thumb else k['rts'],a)
            if k.get('numbered'):  # sequence numbers on orbs
                dr=ImageDraw.Draw(im,'RGBA');n2=len(k['orbs']);step=(W-2*M-44*u)/n2;top=vy+16*u+(0 if thumb else 50*u);cy=(top+vy+vh)/2;fo=f('Black',int(15*u))
                for i in range(n2):
                    cx=M+22*u+step*(i+.5);t=str(i+1);dr.text((cx-dr.textlength(t,font=fo)/2,cy-fo.size*.6),t,font=fo,fill=(10,12,18,230) if k['orbs'][i] else (255,255,255,120))
        else: draw_cones(im,box,k['cones'],u,None if thumb else 'CONE SPLITS · LIT = CLEAN TOUCH')
        lhero = C.lhero
        lhero(im,M+6*u,vy-(112 if thumb else 150)*u,hv,hl,(84 if thumb else 120),a,u,maxw=W*.6)
        B.grid(im,T,M,ty,W-2*M,gh,cols,10*u,a,u,(26 if thumb else 34),72*u)
    return im.convert('RGB')
if __name__=='__main__':
    for d in['share','thumb']: os.makedirs(f'reaction-kits/{d}',exist_ok=True)
    man=[]
    for k in KITS:
        s=G.slug(k['title'])
        card(k,1080,1920,2,104).resize((540,960),Image.LANCZOS).save(f'reaction-kits/share/{s}-share.jpg',quality=88,optimize=True)
        u=2*640/540;card(k,1280,1280,u,40*u,True).resize((640,640),Image.LANCZOS).save(f'reaction-kits/thumb/{s}-thumb.jpg',quality=86,optimize=True)
        man.append(dict(title=k['title'],kit=k['kit'],hero=k['hero'],tiles=k['tiles'],share=f'reaction-kits/share/{s}-share.jpg',thumb=f'reaction-kits/thumb/{s}-thumb.jpg',sample=True))
    import shutil
    for c,s in[('shooting','rate-my-form'),('dribbling','rate-my-handles')]:
        shutil.copy(f'../pack-v4c/share/{c}/{s}-share.jpg','reaction-kits/share/');shutil.copy(f'../pack-v4c/thumb/{c}/{s}-thumb.jpg','reaction-kits/thumb/')
        man.append(dict(title=s,kit='rate',share=f'reaction-kits/share/{s}-share.jpg',thumb=f'reaction-kits/thumb/{s}-thumb.jpg'))
    json.dump(dict(version='4d',drills=man),open('reaction-kits/manifest.json','w'),indent=1)
    fs=[m['share'] for m in man];cs=Image.new('RGB',(5*270+60,2*480+30),(10,12,18))
    for i,p in enumerate(fs): cs.paste(Image.open(p).resize((270,480)),(10+(i%5)*280,10+(i//5)*490))
    cs.save('reaction-kits/contact-sheet.jpg',quality=88)
