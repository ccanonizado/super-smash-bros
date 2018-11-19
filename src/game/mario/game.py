import pygame as pg

pg.init()
win = pg.display.set_mode((500,480))

bgSize = 500
window = pg.display.set_mode((bgSize,bgSize))

pg.display.set_caption("Super Smash Bros")
walkRight = [pg.image.load('1.png'), pg.image.load('2.png'), pg.image.load('3.png'), pg.image.load('4.png'), pg.image.load('5.png'), pg.image.load('6.png'), pg.image.load('7.png'), pg.image.load('8.png')]
walkLeft = [pg.transform.flip(pg.image.load('1.png'), True, False), pg.transform.flip(pg.image.load('2.png'), True, False),pg.transform.flip(pg.image.load('3.png'), True, False), pg.transform.flip(pg.image.load('4.png'), True, False), pg.transform.flip(pg.image.load('5.png'), True, False), pg.transform.flip(pg.image.load('6.png'), True, False), pg.transform.flip(pg.image.load('7.png'), True, False), pg.transform.flip(pg.image.load('8.png'), True, False)]
standingRight = pg.image.load('1.png')
standingLeft = pg.transform.flip(pg.image.load('1.png'), True, False)

clock = pg.time.Clock()
x = 40
y = 440
width = 29
height = 48
velocity = 5
left = False
right = False
walkCount = 0

isJump = False
jumpCount = 10

def redrawGameWindow(prevKey):
    global walkCount
    window.fill((0,0,0))
    if walkCount + 1 >=24:
        walkCount = 0
    if right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    elif left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    else:
        if(prevKey == 'left'):
            win.blit(standingLeft, (x,y))
        elif(prevKey == 'right'):
            win.blit(standingRight, (x,y))
    pg.display.update()
run = True
prevKey = ''
while(run):
    clock.tick(24)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] and x > velocity:
        x -= velocity
        left = True
        right = False
        prevKey = 'left'
    elif keys[pg.K_RIGHT] and x < bgSize-width-velocity:
        x += velocity
        right = True
        left = False
        prevKey = 'right'
    else:
        right = False
        left = False
        walkCount = 0
    if not isJump:
        if keys[pg.K_UP]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1

        else:
            isJump = False
            jumpCount = 10


    redrawGameWindow(prevKey)
    
pg.quit()