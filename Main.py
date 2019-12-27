import sys, pygame, math, time, random
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 30)


size = width, height = 1200, 675
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size) #is blitted after alpha so no fade
k = pygame.Surface((size), pygame.SRCALPHA)  # per-pixel alpha

black = 0, 0, 0
white = 100, 200, 100
green = 100, 100, 100
purple = 200, 100, 200
red = 200, 100, 100
r= 2
ang= 45
dx=int
dy=int
x=width/2
y=height/2
rumble=0

boost=4
boostcol=0

score=0

a=0
turnspeed=0

px=random.randint(100,width-100)
py=random.randint(100,height-100)
psize=50

#----------------------------------AI STUFF---------------------------#
ex=random.randint(200,width-200)
ey=random.randint(200,height-200)
er=2
edx=int
edy=int
eang=random.randint(0,360)

et=0
ebx=0
eby=0
ebdx=0
ebdy=0
ebang=0
ebr=10
chase=0
angdif=0
hitime=0
hit=0
esight=30

angdif2=0


def distance(x1,y1,x2,y2):
    dist= math.sqrt(((x1-x2)**2)+(y1-y2)**2)
    return(dist);

def angle(x1, y1, x2, y2):
    ang=1
    if (y2 - y1) != 0: ang = math.degrees(math.atan2((x1 - x2), (y2 - y1)))
    if (ang < 0):
        ang = 360-abs(ang-90)
    else:
        ang = ang - 90+360
    while ang > 360: ang -= 360
    while ang < 0: ang += 360
    return (ang);

def ecos(x):
    a=0
    a=math.cos(math.radians(x))
    return a

def esin(x):
    a=0
    a=math.sin(math.radians(x))
    return a

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        #----------------------------------------------------AI STUFF-----------------------------#

    if score >0:
        #enemy movement
        edx = er * (ecos(eang))
        edy = er * (esin(eang))
        if distance(ex,ey,px,py)<psize*3:
            angdif2 = eang - angle(x, y, px, py)
            eang -= angdif2 / (2*distance(ex,ey,px,py))

        ex = ex + edx
        ey = ey + edy
        pygame.draw.ellipse(screen, purple, (ex, ey, 5, 5), 2)



        if eang>360: eang-=360
        if eang<0:eang+=360

        #turning at walls
        if ey > height - 90:
            if (0 <= eang <=90)or (360-esight <= eang <=360):
                eang -=1 + esight /(height-ey)
            elif eang > 90 and eang <=180+esight:
                eang +=1 + esight /(height-ey)
        if ey < 100:
            if eang >= 180 - esight and eang <=270:
                eang -=1 + esight / ey
            elif (eang > 270 and eang <=360) or (eang >=0 and eang <= esight):
                eang +=1+ esight / ey

        if ex > width - 90:
            if eang >= 270-20 and eang <=360:
                eang -=1 + 20 /(width-ex)
            elif eang >= 0 and eang <=90+20:
                eang +=1 + 20 /(width-ex)

        if ex < 90:
            if eang >= 90 and eang <=180:
                eang -=1 + 20 / ex
            elif eang > 180 and eang <=270:
                eang +=1+ 20 / ex

        if ey > height-90 or ey < 100 or ex > width- 90 or ex < 90:
            chase= 0
        else:
            chase=1

        #enemy tracking
        angdif=eang-angle(x,y,ex,ey)

        if chase == 1:
            if angdif < esight and angdif > -esight:
                eang-=angdif/10
                purple=(200,200,100)
                et += 1
            else:
                purple=(200,100,200)

            #enemy bullet movement

            if et==30:
                et=0
                ebang=eang
                ebx=ex
                eby=ey
            ebdx= ebr * (ecos(ebang))
            ebdy = ebr * (esin(ebang))
            ebx=ebx+ebdx
            eby=eby+ebdy
            pygame.draw.ellipse(screen, red, (ebx, eby, 5, 5), 2)
            er=2.5
        else:
            er=2
            purple = (100, 100, 200)


        #getting hit!
        if distance(ebx, eby, x,y)<10 or distance(ex, ey, x, y)<12:
            hit=1
            hitime=0
            boost=0.1

        if hit ==1 and hitime< 200:
            hitime+=1
            white=150,100,200
            score=score/1.001
        else:
            hit=0
            white=100,200,100







    #green guy movement
    dx=r*(ecos(ang))
    dy=r*(esin(ang))
    x=x+dx
    y=y+dy

    if turnspeed < 8: turnspeed+=a

    dist=distance(x,y,px,py)
    psize=50+500/dist

    #drawing stuff
    pygame.draw.rect(screen, white, (200+rumble,20+rumble, 400, 10), 1)
    boostcol=80,boost**3/2.5,80
    pygame.draw.rect(screen, boostcol, (202+rumble, 22+rumble, 396*(boost/8), 6), 0)
    pygame.draw.line(screen, (0,0,0), (202+396*(1.5/8),22), (202+396*(1.5/8),28), 1)

    pygame.draw.ellipse(screen, white, (x, y, 5, 5), 2)
    pygame.draw.ellipse(screen, white, (px-psize/2, py-psize/2, psize, psize), 1)

    textsurface = myfont.render(str(int(score)), False, green)
    screen.blit(textsurface, (10+rumble, 10+rumble))

    #getting the powerup thing
    if dist<psize/2:
        px = random.randint(100, width-100)
        py = random.randint(100, height-100)
        score+=r*100
        boost=8


    #controls and movement and stuff
    key = pygame.key.get_pressed()
    if key[pygame.K_d]or key[pygame.K_RIGHT]:
        ang+= turnspeed
        pygame.draw.ellipse(screen, green, (x+ (5*ecos(ang+90)), y+(5*esin(ang+90)), 5, 5), 1)
    if key[pygame.K_a]or key[pygame.K_LEFT]:
        ang -= turnspeed
        pygame.draw.ellipse(screen, green, (x + (5 * ecos(ang - 90)), y + (5 * esin(ang - 90)), 5, 5), 1)
    if key[pygame.K_a] or key[pygame.K_d]or key[pygame.K_RIGHT]or key[pygame.K_LEFT]:
        if key[pygame.K_w] or key[pygame.K_UP]:
            boost = boost / 1.005
            r = 0.35 + boost
            a += 0.5
            rumble=random.randint(-3,3)
            pygame.draw.ellipse(screen, (200,150,100), (x, y, 5, 5), 2)
        else:
            r=1.8
            a+=0.01
            if boost < 8: boost += 0.005
    elif key[pygame.K_w] or key[pygame.K_UP]:
        boost=boost/1.01
        r=0.5+boost
        a=0.0
        turnspeed=1
        rumble = random.randint(-3, 3)
        pygame.draw.ellipse(screen, (200, 150, 100), (x, y, 5, 5), 2)
    else:
        if boost < 8: boost+=0.02
        r=2
        a = 0.0
        turnspeed = 0.01

    if chase==1:
        pygame.draw.line(screen2, green, (ex, ey), (ex + 100 * ecos(eang + esight), ey + 100 * esin(eang + esight)))#------before fade
        pygame.draw.line(screen2, green, (ex, ey), (ex + 100 * ecos(eang - esight), ey + 100 * esin(eang - esight)))

    k.fill((0, 0, 0, 8))  # notice the alpha value in the color
    screen.blit(k, (0, 0))
    screen.blit(screen2, (0, 0))

    time.sleep(0.001)
    pygame.display.flip()
    if chase == 1:
        pygame.draw.line(screen2, black, (ex, ey), (ex + 100 * ecos(eang + esight), ey + 100 * esin(eang + esight)))#------after fade :)
        pygame.draw.line(screen2, black, (ex, ey), (ex + 100 * ecos(eang - esight), ey + 100 * esin(eang - esight)))