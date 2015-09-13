from random import choice, randint

words = [
"shadow",
"vengeance",
"ruin",
"glory",
"battle",
"death",
'blood',
'life',
'stone',
'fire',
'water',
'wind',
'chasm',
'ravine',
'tomb',
'slave',
'prison',
'dungeon',
'castle',
'duck',
'fate',
'destiny',
'sword',
'axe',
'shield',
'helm',
'coin',
'spear',
'gold',
'silver',
'copper',
'iron',
'steel',
'magma',
'sky',
'night',
'knight',
'hole',
'storm',
'wave',
'pit',
'seeker',
'slayer',
'king',
'prince',
#insert more here!
]
def grab(cap=False):
	if not cap:
		return choice(words)
	return choice(words).capitalize()
	
def makeTitle():
	R = randint(0,2)
	title = ""
	#The N of Nn
	if R == 0:
		title = "The {} of {}{}".format( grab(1), grab(1),grab() )
	#Nn's N
	elif R == 1:
		title = "{}{}'s {}".format( grab(1),grab(), grab(1) )
	#Nn
	elif R == 2:
		title = "{}{}".format( grab(1),grab() )
	
	S = randint(0,3)
	sub = ""
	#Ns of the N
	if S == 0:
		sub = "{}s of The {}".format( grab(1), grab(1) )
	#Ns of N's N
	elif S == 1:
		sub = "{}s of {}'s {}".format( grab(1),grab(), grab(1), grab(1) )
	#Ns and Ns
	elif S == 2:
		sub = "{}s & {}s".format( grab(1), grab(1) )
	#Ns over Nn
	elif S == 3:
		sub = "{}s Over {}{}".format( grab(1), grab(1),grab() )
		
	return "{}:  {}".format(title, sub)
