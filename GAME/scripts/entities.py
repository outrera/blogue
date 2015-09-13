#	Factories for creating Entities
#
#
'''
	things Reference:
	
		Later
'''
from .things import Thing, Fighter, BasicMonster, Item
from .things import Potion_Heal
from .sprite_wrapper import Sprite

from random import randint as roll

def Player(own):
	f = Fighter(HP=200, power=6, defense=1)
	a = BasicMonster()
	return Thing(own, "Player", fighter=f, ai=a)

def Zombie(own,sprite):
	f = Fighter(HP=roll(15,25), power=6, defense=1)
	a = BasicMonster()
	s = Sprite(sprite, 'zombie', active=True, direction=True, loop=True, action='walk')
	return Thing(own, 'Zombie', sprite=s, fighter=f, ai=a)

def ZombieCorpse(own):
	s = Sprite(own, 'zombie_death', active=True, direction=False, loop=False)
	return Thing(own, 'Zombie Corpse', sprite=s)

'''
def Ettin(own,sprite):
	f = Fighter(HP=roll(20,30), power=8, defense=2)
	a = BasicMonster()
	s = Sprite(sprite, "Ettin")
	return Thing(own, "Ettin", sprite=s, fighter=f, ai=a)
'''

def LifePotion(own):
	i = Item(Potion_Heal)
	return Thing(own, "Life Potion", item=i)