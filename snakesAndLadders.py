from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image 
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.config import Config
import random
import time
Config.set('graphics', 'resizable', 0)
Window.size = (500,550)


class MyFloat(FloatLayout):
	def __init__(self, **kwargs):
		super(MyFloat, self).__init__(**kwargs)
		self.board= Image(source = 'snl.jpg',size =(500,500),pos = (0,25))
		self.add_widget(self.board)

		self.p1 = Player('red.jpeg',size = (50,50),pos = (0,50))
		self.p2 = Player('blue.jpeg',size = (50,50),pos = (0,50))

		self.turn = 0
		self.dice = Button(size_hint = (0.2,0.09),pos_hint = {'x':0.4,'y':0})
		self.dice.bind(on_press = self.dice_roll)
		
		self.add_widget(self.p1)
		self.add_widget(self.p2)
		self.add_widget(self.dice)

		self.snakes = {17:7,54:34,62:19,64:60,87:36,93:73,95:75,98:79}
		self.ladders = {1:38,4:14,9:31,21:42,28:84,51:67,72:91,80:99}

	def dice_roll(self,event):
		dice_value = random.randint(1,6)	
		
		if(self.turn == 0):
			self.p1.movePawn(dice_value,self.snakes,self.ladders)
			self.turn = 1
		else:
			self.p2.movePawn(dice_value,self.snakes,self.ladders)
			self.turn = 0

		if (self.p1.score == 100 or self.p2.score == 100):
			self.remove_widget(self.dice)


class Player(Widget):
	def __init__(self,image_name,**kwargs):
		super(Player, self).__init__(**kwargs)
		
		self.pawn= Image(size =self.size,pos = self.pos,source = image_name)
		self.score = 0
		self.add_widget(self.pawn)

	def movePawn(self,dice_value,snakes,ladders):
		if(self.score+dice_value > 100):
			print("#",self.score+dice_value)
			return
		self.score = dice_value + self.score	
		x1,y1 = self.get_pos()	
		anim = Animation(x=x1, y=y1) 
		anim = self.checkSnakeOrLadder(anim,snakes)
		anim = self.checkSnakeOrLadder(anim,ladders)
		anim.start(self.pawn)	

	def checkSnakeOrLadder(self,anim,snakesOrLadders):
		if self.score in snakesOrLadders:
			self.score = snakesOrLadders[self.score]
			x1,y1 = self.get_pos()	
			anim = anim+Animation(x=x1, y=y1)
		return anim

	def get_pos(self):
		print("score: ",self.score)
		tensPlace = self.score//10
		unitsPlace = self.score%10
		if(self.score%10 == 0):
			y = tensPlace-1
			if(tensPlace%2 == 0):
				x = 0
			else:
				x = 9
		else:
			y = tensPlace
			if(tensPlace%2 == 0):
				x = unitsPlace-1
			else:
				x = 10-unitsPlace		
		
		return (50*x,50*y+50)


class MyApp(App):
	def build(self):
		return MyFloat()


if __name__ == "__main__":
	MyApp().run()
