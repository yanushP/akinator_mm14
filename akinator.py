import pygame, sys 
from pygame.locals import *
import random as rn
import ask

FONT_SIZE = 50
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
	return res

class BButton:
	def __init__(self, Picture1, Picture2, coords):
		if Picture2 == "": Picture2 = Picture1
		self.image = pygame.image.load(Picture1)
		self.pressed = 0
		self.image2 = pygame.image.load(Picture1)
		self.imagerect = self.image.get_rect()
		self.imagerect.x += coords[0]
		self.imagerect.y += coords[1]
	def render(self, surface):
		if self.pressed > 0:
			surface.blit(self.image,(self.imagerect.x + 1, self.imagerect.y + 1))
			self.pressed -= 1
		else:
			surface.blit(self.image,(self.imagerect.x, self.imagerect.y))
	def collidepoint(self, mouse):
		if self.imagerect.collidepoint(mouse):
			self.pressed = 10
			return True
		return False

def put_str(s, surf, str_num):
	leng = int(len(s) * 23.3)
	x = (WIDTH - leng) / 2
	y = str_num*40 + 40
	myFont = pygame.font.Font("font.ttf", FONT_SIZE)
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

b0 = BButton('0.png','',(150 + 20,300))
b1 = BButton('1.png','',(400 + 20,300))
b2 = BButton('2.png','',(150 + 20,400))
b3 = BButton('3.png','',(400 + 20,400))
b4 = BButton('4.png','',(275 + 20,500))
brestart = BButton('restart.png','',(150,300))
bnew_game = BButton('new_game.png','',(0,0))

while mainLoop: 
	pe_event = pygame.event.get()
	for event in pe_event: 
		ans, result = GAME.ask()
		if result != -1:
			end_game = True
		if event.type == QUIT: 
			mainLoop = False 
		screen.fill(bgColor) 
		if end_game:
			bgColor = (0,255,255)
			screen.fill(bgColor)
			put_text("Мы думаем это " + GAME.get_name(result), screen)
			mouse = pygame.mouse.get_pos()
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				if brestart.collidepoint(mouse):
					GAME = ask.kernel()
					end_game = False
					bgColor = (255,255,255)
			break
		put_text(GAME.get_question(ans), screen)
		mouse = pygame.mouse.get_pos()
		picked = -1
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			if b0.collidepoint(mouse):
				picked = 0
			if b1.collidepoint(mouse):
				picked = 1
			if b2.collidepoint(mouse):
				picked = 2
			if b3.collidepoint(mouse):
				picked = 3
			if b4.collidepoint(mouse):
				picked = 4
			if bnew_game.collidepoint(mouse):
				GAME = ask.kernel()
				bgColor = (255,255,255)
				break

		if picked >= 0:
			bgColor = (bgColor[0],max(100,bgColor[1]*0.95),max(100,bgColor[2]*0.95))
			GAME.answer(picked)


	if not end_game:
		b0.render(screen)
		b1.render(screen)
		b2.render(screen)
		b3.render(screen)
		b4.render(screen)
		bnew_game.render(screen)
	else:
		brestart.render(screen)
	pygame.display.update() 
pygame.quit() 
