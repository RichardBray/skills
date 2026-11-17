from PIL import Image
W,H=26,40
INK=(20,20,20,255); HAIR=(107,63,29,255); HAIR2=(74,42,18,255); SKIN=(242,199,160,255); SKIN2=(220,170,130,255)
RED=(229,56,45,255); WHITE=(255,255,255,255); PINK=(255,111,168,255); PINK2=(217,79,136,255); ORG=(250,93,25,255)
TAN=(200,161,101,255); LIPS=(190,60,70,255)
def make(pose):
    g={}
    def r(x,y,w,h,c):
        for i in range(x,x+w):
            for j in range(y,y+h): g[(i,j)]=c
    r(10,0,6,3,HAIR); r(11,0,4,1,HAIR2)          # bun
    r(7,3,12,3,HAIR); r(6,5,14,10,HAIR)          # hair
    r(8,7,10,8,SKIN)                              # face
    r(8,7,10,1,HAIR2); r(8,7,2,3,HAIR2); r(16,7,2,3,HAIR2)  # fringe
    for ox in (9,14):                             # glasses
        r(ox,9,4,4,RED); r(ox+1,10,2,2,WHITE); r(ox+1,11,1,1,INK)
    r(13,10,1,1,RED)
    r(11,14,4,1,LIPS); r(10,13,1,1,LIPS); r(15,13,1,1,LIPS)
    r(11,15,4,1,SKIN2)
    r(7,16,12,11,PINK); r(7,25,12,2,PINK2)        # blazer
    r(11,16,4,5,WHITE); r(12,16,2,1,SKIN2)        # shirt
    r(12,17,1,5,ORG); r(11,21,3,3,WHITE); r(12,22,1,1,ORG)  # lanyard+badge
    r(8,27,10,6,INK)                              # skirt
    r(10,33,2,5,SKIN); r(14,33,2,5,SKIN)
    r(9,38,3,2,INK); r(14,38,3,2,INK)
    # left arm holding clipboard
    r(4,17,3,7,PINK); r(4,24,3,2,SKIN)
    r(1,20,6,10,TAN); r(2,22,4,7,WHITE); r(3,21,2,1,INK)
    r(3,24,3,1,(180,180,180,255)); r(3,26,3,1,(180,180,180,255))
    if pose=='wave':
        r(19,16,3,4,PINK); r(21,10,3,7,PINK); r(21,7,3,3,SKIN); r(23,6,1,2,SKIN)
    else:
        r(19,17,3,4,PINK); r(21,15,3,3,PINK); r(20,11,4,4,SKIN); r(22,8,2,3,SKIN)
    img=Image.new('RGBA',(W,H),(0,0,0,0))
    for (x,y),c in g.items(): img.putpixel((x,y),c)
    out=img.copy()
    for x in range(W):
        for y in range(H):
            if img.getpixel((x,y))[3]==0:
                for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<W and 0<=ny<H and img.getpixel((nx,ny))[3]>0:
                        out.putpixel((x,y),INK);break
    return out
for pose,scale in (('wave',7),('thumb',6)):
    im=make(pose); im=im.resize((W*scale,H*scale),Image.NEAREST); im.save(f'char/char-{pose}.png'); print(pose,im.size)
