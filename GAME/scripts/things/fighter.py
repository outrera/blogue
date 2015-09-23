from bge import logic
from random import randint



def find_xp_for_level(L):
	M = 50
	N = 100		#this is the XP curve for Zodiac FFRPG!
	if L == 1:
		return 0
	else:
		return XP_to_lvl(L-1) + M + (N*(L-2))
		

class Fighter:
	def __init__(self, HP, power, defense):
		self.maxHP = HP
		self.HP = HP
		self.power = power
		self.defense  = defense
		
		#All this needs to be getted from __init__
		self.turn_rate = 0.08
		self.move_speed = 0.3
		self.attack_range = 3.0
		self.attack_rate = 60
		self.attack_counter = self.attack_rate
		
		self.target = None

	def __repr__(self):
		return "FIGHTER component of {}".format(self.owner)
	
	
	#Lost Life points from an origin		
	def hurt(self, damage, origin=None):
		if origin == None:
			origin = self.owner
		self.HP -= damage
		
		if self.HP <= 0:
			print("R.I.P.   {} has died at the hands of {}".format(self.owner.Name, origin.Name))
			self.owner.kill(origin)

		elif self.HP >= self.maxHP:	self.HP = self.maxHP
		print("{}/{} HP remaining for {}".format(self.HP, self.maxHP, self.owner.Name))
			
			
	def heal(self, amt):
		self.HP += amt
		if self.HP >= self.maxHP:	
			self.HP = self.maxHP

		
	#Attempt a melee attack
	def attack(self):
		d = self.attack_range
		ray = self.owner.ai.sight_ray(d)

		if ray and 'ent' in ray:
			if hasattr(ray['ent'], 'fighter') and ray['ent'].fighter:
				#################################
				#	Combat mechanics go here!	#
				#################################
				ray['ent'].get_hit(self.power, self.owner)	#Deal damage to the target
			
				#impact blood spray
				brush = self.owner.own.scene.objects['System']
				brush.worldPosition = ray.worldPosition
				brush.worldPosition.z += 1.0
				emitter = self.owner.own.scene.addObject('Blood Spray', brush, 2)
				emitter['impact'] = self.power
		
		#Attacked, but no target..
		else:
			print("{} swings at the air!".format(self.owner.Name))
			
			
			
			
			
			
			

class PlayerFighter:
	def __init__(self, HP, power, defense):
		self.level = 1
		self.xp = 0
		
		self.maxHP = HP
		self.HP = HP
		self.power = power
		self.defense  = defense
		
		#All this needs to be getted from __init__
		self.turn_rate = 0.08
		self.move_speed = 0.3
		self.attack_range = 3.0
		self.attack_rate = 60
		self.attack_counter = self.attack_rate
		
		self.target = None
	
	@property
	def xp_to_next(self):
		return find_xp_for_level(self.level + 1)
	
	def __repr__(self):
		return "PLAYER-FIGHTER component of {}".format(self.owner)
	
	
	#Lost Life points from an origin		
	def hurt(self, damage, origin=None):
		if origin == None:
			origin = self.owner
		self.HP -= damage
		
		if self.HP <= 0:
			#self.owner.state = 'dead'
			print("R.I.P.   {} has died at the hands of {}".format(self.owner.Name, origin.Name))
			self.owner.player_kill(origin)
			
		elif self.HP >= self.maxHP:	self.HP = self.maxHP

		self.announce_life()
		print("{}/{} HP remaining for {}".format(self.HP, self.maxHP, self.owner.Name))
			
	def heal(self, amt):
		self.HP += amt
		if self.HP >= self.maxHP:	
			self.HP = self.maxHP
		
		self.announce_life()
	
	#Player gains XP points, maybe levels up
	def gain_xp(self, amt):
		self.xp += amt
		if self.xp >= self.xp_to_next:
			self.level += 1
			logic.sendMessage('update_level_number', str(self.level))
		value = find_xp_for_level(self.level) / find_xp_for_level(self.level+1)
		logic.sendMessage('update_player_xp', str(value))
		
	#send our Life info to the HUD for display	
	def announce_life(self):
		value = self.HP / self.maxHP
		logic.sendMessage('update_player_hp', str(value))
		logic.sendMessage('hp_number', str(self.HP))
		
	#Attempt a melee attack
	def attack(self):
		d = self.attack_range
		ray = self.owner.ai.sight_ray(d)

		if ray and 'ent' in ray:
			if hasattr(ray['ent'], 'fighter') and ray['ent'].fighter:
				#################################
				#	Combat mechanics go here!	#
				#################################
				ray['ent'].get_hit(self.power, self.owner)	#Deal damage to the target
			
				#impact blood spray
				brush = self.owner.own.scene.objects['System']
				brush.worldPosition = ray.worldPosition
				brush.worldPosition.z += 1.0
				emitter = self.owner.own.scene.addObject('Blood Spray', brush, 2)
				emitter['impact'] = self.power
		
		#Attacked, but no target..
		else:
			print("{} swings at the air!".format(self.owner.Name))
			
			

