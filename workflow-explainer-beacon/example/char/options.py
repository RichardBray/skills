from PIL import Image, ImageDraw
import sprite
W,H=26,40
INK=sprite.INK;HAIR=sprite.HAIR;HAIR2=sprite.HAIR2;SKIN=sprite.SKIN;SKIN2=sprite.SKIN2;RED=sprite.RED;WHITE=sprite.WHITE;PINK=sprite.PINK;PINK2=sprite.PINK2;ORG=sprite.ORG;TAN=sprite.TAN;LIPS=sprite.LIPS
CREAM=(240,228,196,255);BLUE=(70,100,170,255);BLUE2=(50,75,135,255);GREY=(180,180,180,255);WOOD=(150,100,50,255)
def canvas():
    g={}
    def r(x,y,w,h,c):
        for i in range(x,x+w):
            for j in range(y,y+h): g[(i,j)]=c
    return g,r
def finish(g):
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    for (x,y),c in g.items():
        if 0<=x<W and 0<=y<H: img.putpixel((x,y),c)
    out=img.copy()
    for x in range(W):
        for y in range(H):
            if img.getpixel((x,y))[3]==0:
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<W and 0<=ny<H and img.getpixel((nx,ny))[3]>0: out.putpixel((x,y),INK);break
    return out
def face(r,y=7):
    r(8,y,10,8,SKIN)
    for ox in (9,14):
        r(ox,y+2,4,4,RED); r(ox+1,y+3,2,2,WHITE); r(ox+1,y+4,1,1,INK)
    r(13,y+3,1,1,RED); r(11,y+7,4,1,LIPS); r(10,y+6,1,1,LIPS); r(15,y+6,1,1,LIPS); r(11,y+8,4,1,SKIN2)
def legs(r,c=SKIN,shoe=INK):
    r(10,33,2,5,c); r(14,33,2,5,c); r(9,38,3,2,shoe); r(14,38,3,2,shoe)
def prof():
    g,r=canvas()
    r(7,3,12,3,HAIR); r(6,5,14,12,HAIR); r(6,15,2,3,HAIR); r(18,15,2,3,HAIR); face(r); r(8,7,10,1,HAIR2); r(8,7,2,3,HAIR2); r(16,7,2,3,HAIR2)
    r(7,16,12,11,PINK); r(11,16,4,6,WHITE); r(12,16,2,1,SKIN2); r(12,18,2,1,RED)
    r(8,27,10,6,INK); legs(r)
    r(4,17,3,8,PINK); r(4,25,3,2,SKIN); r(19,17,3,6,PINK); r(19,23,3,2,SKIN)
    for i in range(14): r(22+i//5,22-i,1,1,WOOD)   # pointer stick
    return finish(g)
def board():
    g,r=canvas()
    r(7,3,12,3,HAIR); r(6,5,14,8,HAIR); r(19,6,3,9,HAIR); r(20,14,2,4,HAIR2); face(r); r(8,7,10,1,HAIR2); r(8,7,2,3,HAIR2); r(16,7,2,3,HAIR2)
    r(7,16,12,11,CREAM); r(11,16,4,3,WHITE); r(11,17,4,2,RED)
    r(7,27,12,6,PINK2); legs(r)
    r(4,17,3,8,CREAM); r(4,25,3,2,SKIN); r(19,15,3,4,CREAM); r(21,9,3,7,CREAM); r(21,6,3,3,SKIN); r(23,3,2,4,WHITE)
    return finish(g)
def recruiter(): return sprite.make('thumb')
def buddy():
    g,r=canvas()
    r(7,3,12,3,HAIR); r(5,5,16,10,HAIR); r(5,14,3,12,HAIR); r(18,14,3,12,HAIR); face(r); r(8,7,10,1,HAIR2); r(8,7,2,3,HAIR2); r(16,7,2,3,HAIR2)
    r(5,16,16,13,PINK); r(5,26,16,3,PINK2); r(11,16,4,1,SKIN2)
    r(8,29,10,4,BLUE); legs(r,BLUE,PINK)
    r(2,19,3,9,PINK); r(2,28,3,2,SKIN); r(21,19,3,6,PINK); r(21,25,3,2,SKIN)
    r(21,22,4,5,WHITE); r(22,23,2,1,TAN); r(25,23,1,3,WHITE); r(22,19,1,2,GREY); r(24,18,1,3,GREY)
    return finish(g)
def chibi():
    g,r=canvas()
    r(5,6,16,5,HAIR); r(4,9,18,14,HAIR); r(8,12,10,10,SKIN); r(8,12,10,2,HAIR2)
    for ox in (8,14):
        r(ox,15,5,5,RED); r(ox+1,16,3,3,WHITE); r(ox+2,17,1,2,INK)
    r(13,16,1,1,RED); r(11,21,4,1,LIPS)
    r(10,2,6,5,HAIR); r(11,1,4,2,HAIR2)
    r(8,23,10,8,PINK); r(12,23,2,3,WHITE); r(12,26,2,3,ORG)
    r(9,31,3,5,INK); r(14,31,3,5,INK); r(8,36,4,2,PINK2); r(14,36,4,2,PINK2)
    r(5,24,3,5,PINK); r(18,24,3,5,PINK); r(5,29,3,2,SKIN); r(18,29,3,2,SKIN)
    return finish(g)
opts=[('1  Professor',prof()),('2  Whiteboard',board()),('3  Recruiter',recruiter()),('4  Study buddy',buddy()),('5  Desk mascot',chibi())]
S=7;pad=30
sheet=Image.new('RGBA',(len(opts)*(W*S+pad)+pad,H*S+pad*2+40),(239,233,221,255))
d=ImageDraw.Draw(sheet)
for i,(n,im) in enumerate(opts):
    im=im.resize((W*S,H*S),Image.NEAREST); x=pad+i*(W*S+pad)
    sheet.paste(im,(x,pad),im); d.text((x,pad+H*S+12),n,fill=(20,20,20,255))
sheet.convert('RGB').save('options.png'); print(sheet.size)
