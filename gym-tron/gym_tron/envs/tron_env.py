import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from turtle import *
from freegames import square, vector
from IPython.display import clear_output
import time
import random 

class Player:
		def __init__(self,jogo,x,y,dir):
			self.x = x
			self.y = y
			self.actions = [0,1,2,3]
			self.oposite = {0:2,1:3,2:0,3:1}
			self.dir = dir
			self.jogo = jogo
			
		def move(self,dir):
			possible_actions = self.actions.copy()
			possible_actions.remove(self.oposite[self.dir]) #remove a direcao oposta das possiveis acoes
			
			if dir not in possible_actions:
				dir = self.dir
			
			if (dir == 0):
				self.y += -1
			
			if (dir == 1):
				self.x += 1
				
			if (dir == 2):
				self.y += 1
			
			if (dir == 3):
				self.x += -1
			
			self.dir = dir
			
		def out_of_bounds(self):
			if (self.x not in range(0,self.jogo.width) or self.y not in range (0,self.jogo.height)):
				return True
			else:
				return False
				
				

class TronEnv(gym.Env):
			
	metadata = {'render.modes': ['human']}
	width = 11			
	height = 11
	scale = 10
	
	def devolveEstado(self):
		return np.append(self.state, [self.p1.x, self.p1.y, self.p1.dir, self.p2.x, self.p2.y, self.p2.dir])
	
	def isviable(self,x,y):
		try: 
			if (self.state[x][y] == 0):
				return True
			else:
				return True
		except:
			return False
			
	def __init__(self):	
		x1 = self.p1x_inicial = 2
		y1 = self.p1y_inicial = 5
		x2 = self.p2x_inicial = 10
		y2 = self.p2y_inicial = 5
		self.dir1 = 1
		self.dir2 = 3
		self.p1 = Player(self,x1,y1,self.dir1)						#	O--------► X
		self.p2 = Player(self,x2,y2,self.dir2) 						#	|																																												 	
		self.state = np.zeros((self.height,self.width))				#	| p1     p2				
		self.state[self.p1.x][self.p1.y] = 1						#	|
		self.state[self.p2.x][self.p2.y] = -1						# Y ▼
		self.done = 0
		self.size = 10
		self.directions = [0,1,2,3]
		
	def step(self, action):
		
		#		  0
		#		  ▲
		#		  |	
		#	3 ◄-- O --► 1
		#		  |
		#		  ▼
		#		  2
		
			self.p1.move(action)
			
			clean_directions = self.directions.copy()
			
			#vendo quais direcoes podem ser escolhidas
			if not self.isviable(self.p2.x,self.p2.y-1):
				clean_directions.remove(0)
			
			if not self.isviable(self.p2.x+1,self.p2.y):
				clean_directions.remove(1)
				
			if not self.isviable(self.p2.x,self.p2.y+1):
				clean_directions.remove(2)
			
			if not self.isviable(self.p2.x-1,self.p2.y):
				clean_directions.remove(3)
				
			if not clean_directions:
				clean_directions.append(self.p2.dir)
			
			self.p2.move(random.choice(clean_directions)) 
			
			
			
			#jogador perdeu
			if (not self.p1.out_of_bounds()):
				if (self.state[self.p1.x][self.p1.y] != 0): 
					return devolveEstado(),-100,True
			else:
				return self.state,-100,True
			 	
			
			 #jogador ganhou
			if (not self.p2.out_of_bounds()):
				if (self.state[self.p2.x][self.p2.y] == 1): 
					return self.devolveEstado(),100, True
				if (self.state[self.p2.x][self.p2.y] == -1): 
					return self.devolveEstado(),0, True
			else:
				return self.devolveEstado(),100, True
			
			self.state[self.p1.x][self.p1.y] = 1
			self.state[self.p2.x][self.p2.y] = -1	
			
			return self.devolveEstado(),-1,False #jogo ainda nao acabou
			
				
	def render(self, mode='human', close=False):
		
		#clear_output()
		print()
		estado = self.state
		for j in range(0,self.height):
			print()
			for i in range (0,self.width):
				if (estado[i][j]!=0 ):
					if(estado[i][j]==1):
						print('X ',end='')
					elif (estado[i][j]==-1):
						print('O ',end='')
				else:
					print('- ',end='')
		print()
		time.sleep(0.5)
		'''
		size = self.size
		height = self.height * size
		width = self.width * size
		
		posX = self.p1_x
		posY = self.p1_y
		
		newX = posX*10 - width/2		
		newY = -posY*10 + height/2     
		square(newX,newY,size,'blue')
		
		posX = self.p2_x
		posY = self.p2_y
		
		newX = posX*10 - width/2		
		newY = -posY*10 + height/2     
		square(newX,newY,size,'red')
			
	def start_render(self):
		size = self.size
		height = self.height * size
		width = self.width * size
		
		speed(0)
		setup(1000,1000)
		up()
		goto(-width/2+size,height/2) # posicao (0,0)
		down()
		
		#desenhando o jogo
		goto(width/2+size,height/2)
		goto(width/2+size,-height/2)
		goto(-width/2+size,-height/2)
		goto(-width/2+size,height/2)
		
		hideturtle()
		'''
	def reset(self):	
		x1 = self.p1.x = self.p1x_inicial 
		y1 = self.p1.y = self.p1y_inicial 
		x2 = self.p2.x = self.p2x_inicial 
		y2 = self.p2.y = self.p2y_inicial 	
		self.state[::] = 0	
		self.state[x1][y1] = 1
		self.state[x2][y2] = -1
		self.done = 0
		self.dir1 = 1
		self.dir2 = 3
		

		
		