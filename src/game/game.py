import pygame as pg

pg.init()

bgSize = 500
window = pg.display.set_mode((bgSize,bgSize))

pg.display.set_caption("Super Smash Bros")

x = 40
y = 440
width = 40
height = 60
velocity = 5
left = False
right = False
walkCount = 0

isJump = False
jumpCount = 10

run = True
while(run):
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] and x > velocity:
        x -= velocity
    
    if keys[pg.K_RIGHT] and x < bgSize-width-velocity:
        x += velocity

    if not isJump:
        if keys[pg.K_UP]:
            isJump = True
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

    window.fill((0,0,0))
    pg.draw.rect(window, (255,0,0), (x,y,width,height))
    pg.display.update()
    
pg.quit()