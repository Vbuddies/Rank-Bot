#xp.py
#holds all the xp stuff for users
import math
import random

class person:

	def get_name(self):
		#returns string of the users name
		return self.name

	def get_xp(self):
		#returns the xp of the user
		return self.xp

	def get_level(self):
		#returns the level of the user
		return self.level

	def get_money(self):
		#returns the users money
		return self.money

	def add_money(self, amount = 0.0):
		#add money to person
		if amount == 0:
			e = round(random.uniform(1, 20), 2)
			print(e)
			self.money += e
		else:
			self.money += amount

	def add_xp(self, amount = 0):
		#add xp to person
		if amount == 0:
			e = random.randint(1, 6)
			self.xp += e
		else:
			self.xp += amount

		if self.check() != self.level:
			return True
			#call self.level_up() from where it is returned
		else:
			return False

	def take_money(self, amount = 0.0):
		#remove money from person
		if amount == 0:
			e = round(random.uniform(1, 20), 2)
			self.money -= e
		else :
			self.money -= amount

		if self.money < 0:
			self.money = 0

	def take_xp(self, amount = 0):
		#remove xp from the person
		if amount == 0:
			e = random.randint(1, 6)
			self.xp -= e
		else:
			self.xp -= amount

		if self.xp < 0:
			self.xp = 0

		if self.check() != self.level:
			#call self.level_up() from where it is returned
			return True
		else:
			return False

	def level_up(self):
		self.level = self.check()

	def check(self):
		#check level of person
		#level = constant * sqrt(XP)......constant could be 0.2
		level = math.floor(0.2 * math.sqrt(self.xp))
		return level




	def __init__ (self, name, xp = 0, money = 0, master = None):
		self.name = name
		self.xp = xp
		self.money = money
		self.level = self.check()
