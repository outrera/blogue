#	events.py	#
#	misc hard-coded game events	#

def LifePotion(target, amt):
	target.fighter.heal(amt)
	print("{} restored {} Life".format(target.Name, amt))
