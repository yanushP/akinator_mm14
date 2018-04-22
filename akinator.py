import pygame, sys 
from pygame.locals import *
import random as rn
import ask

FONT_SIZE = 40
WIDTH = 800
HEIGHT = 600

def rand_str():
	ln = rn.randint(0,100)
	res = ''
	w = True
	for i in range(ln):
		x = rn.randint(0,1)
		if x == 0 and not w:
			res += ' '
			w = True
		else: 
			res += 'a'
			w = False
	#res = 'Я ебал твою телку ууу ты ебал мою собаку трах трах, а денис иванов полнейшая хуйня сука в рот ебббаааааал!!!!!???'
	return res

def Buttonify(Picture, coords, surface):
    image = pygame.image.load(Picture)
    imagerect = image.get_rect()
    imagerect.x += coords[0]
    imagerect.y += coords[1]
    surface.blit(image,(imagerect.x, imagerect.y))
    return (image,imagerect)

def put_str(s, surf, str_num):
	leng = len(s) * 24
	x = (WIDTH - leng) / 2
	y = str_num*40 + 40
	myFont = pygame.font.SysFont("Courier", FONT_SIZE, bold = 1)
	fontColor = (0,0,0)
	fontImage = myFont.render(s, 0, (fontColor)) 
	surf.blit(fontImage,(x,y))
def put_text(s, surf):
	words = s.split(' ')
	num = 0
	now_s = ''
	for w in words:
		now_s += w + ' '
		if len(now_s) > 20:
			put_str(now_s[:-1], surf, num)
			num += 1
			now_s = ''
	if len(now_s) != 0:
		put_str(now_s[:-1], surf, num)

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

bgColor = (255,255,255)

mainLoop = True

end_game = False

now_text = rand_str()

GAME = ask.kernel()

while mainLoop: 
	for event in pygame.event.get(): 
		ans, result = GAME.ask()
		if result != -1:
			end_game = True
		if event.type == QUIT: 
			mainLoop = False 
		screen.fill(bgColor) 
		if end_game:
			put_text("Мы думаем это " + GAME.get_name(result), screen)
			brestart = Buttonify('restart.png',(150,300), screen)
			mouse = pygame.mouse.get_pos()
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				if brestart[1].collidepoint(mouse):
					GAME = ask.kernel()
					end_game = False
			pygame.display.update() 
			continue

		put_text(GAME.get_question(ans), screen)
		b0 = Buttonify('0.png',(150 + 20,300), screen)
		b1 = Buttonify('1.png',(400 + 20,300), screen)
		b2 = Buttonify('2.png',(150 + 20,400), screen)
		b3 = Buttonify('3.png',(400 + 20,400), screen)
		b4 = Buttonify('4.png',(275 + 20,500), screen)
		mouse = pygame.mouse.get_pos()
		picked = -1
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			if b0[1].collidepoint(mouse):
				picked = 0
			if b1[1].collidepoint(mouse):
				picked = 1
			if b2[1].collidepoint(mouse):
				picked = 2
			if b3[1].collidepoint(mouse):
				picked = 3
			if b4[1].collidepoint(mouse):
				picked = 4
				end_game = True

		if picked >= 0:
			GAME.answer(picked)
		pygame.display.update() 
pygame.quit() 