from bge import logic, render
from mathutils import Vector
from math import pi, sqrt
from random import randint

from .sprite_wrapper import Sprite

framerate = 4	#FPS for sprite animation

def head_kick(head, impact):
	r_z = randint(-10,10)*0.01*(impact)
	r_x = randint(-10,10)*0.01*(impact)
	head.parent.applyRotation([0,0,r_z], False)
	head.applyRotation([r_x,0,0], True)

def Potion_Heal():
	target = logic.getCurrentScene().objects['System']['sys'].player['ent']
	target.fighter.hurt(-25)
	print("HEALED 25")

class Item:
	def __init__(self,use_effect, owned_by=None):
		self.use_effect = use_effect
		self.owned_by = owned_by
		
class BasicMonster:
	
	def __init__(self):
		self.target = None
		self.ai_timer = 0
		
		self.state = 'idle'
		
		self.last_attacker = None	#The last creature to hurt me
		
		self.frame_track = None
		
	def __repr__(self):
		return "AI component of {}".format(self.owner)
	
	def think(self):
		if self.state == 'idle':
			self.owner.sprite.action = 'walk'
			self.owner.sprite.own['rate'] = 10
		elif self.state == 'attack':
			self.owner.sprite.action = 'strike'
			self.owner.sprite.own['rate'] = 8
			
		#print("The {} growls!").format(self.owner.Name)
		"""My standard AI cycle"""	
		if self.target:
			if self.target.invalid:
				self.target = None
			if self.target == self.owner.own:
				self.target = None
		
		if not self.target:
			self.target = self.owner.sys['sys'].player

		self.face(self.target)
		if self.owner.own.getDistanceTo(self.target) > 1.5 and self.state == 'idle':
			if self.owner.sprite.current_frame != self.frame_track:
				self.advance()
				self.frame_track = self.owner.sprite.current_frame
	
		if self.state == 'attack':
			self.ai_timer += 1
			if self.ai_timer >= self.owner.fighter.attack_rate:
				if self.owner.own.getDistanceTo(self.target) <= self.owner.fighter.attack_range:
					self.fight()

				self.ai_timer = 0
				self.state = 'idle'

				#self.owner.sprite.action = 'walk'
			
		elif self.state == 'hurt':
			self.ai_timer += 1
			if self.ai_timer >= 30:
				self.ai_timer = 0
				self.state = 'idle'
				self.target = self.last_attacker
	
	


					
	def fight(self):
		self.owner.fighter.attack()

							
	def advance(self, mod=1.0):
		"""Move our object forward at our movement rate, multiplied by mod"""
		obstacle = self.sight_ray(1.25)
		if not obstacle:
			
			new_pos = self.owner.own.worldPosition + (self.owner.own.localOrientation.col[1]*(self.owner.fighter.move_speed*mod))
			self.owner.own.worldPosition = new_pos
		else:
			if randint(1,10) <= 3 and 'ent' in obstacle:
				self.target = obstacle
				self.state = 'attack'
				
	def face(self, target):
		"""Turn my object to face its target"""
		v = self.owner.own.getVectTo(target)		#get the vector to the target
		rate = self.owner.fighter.turn_rate
		self.owner.own.alignAxisToVect(v[1],1,rate)	#steer toward the vector
		self.owner.own.alignAxisToVect([0,0,1],2,1)	#keep local +Z snapped to global +Z
		if v[0] <= self.owner.fighter.attack_range:
			if self.state != 'hurt':
				self.state = 'attack'

	def los_ray(self, other):
		#check for line of sight to the player
		ray = self.owner.own.rayCast(other, self.owner.own, 0, 'wall',0,1,0)
		for ob in ray:
			if ob != None:
				return False
		#render.drawLine(self.owner.own.worldPosition, other.worldPosition, [1,1,0])
		return True

	def sight_ray(self, distance):
		"""check for objects directly in front of me, up to distance"""
		vec = (self.owner.own.localOrientation.col[1]*100)+Vector(self.owner.own.worldPosition)
		#render.drawLine(self.owner.own.worldPosition, vec, [1,0,0])	#test line
		wall = self.owner.own.rayCastTo(vec,distance,'wall')
		thing = self.owner.own.rayCastTo(vec,distance,'thing')
		if thing:
			return thing
		if wall:
			return wall
	
class Fighter:
	def __init__(self, HP, power, defense):
		self.maxHP = HP
		self.HP = HP
		self.power = power
		self.defense  = defense
		
		self.turn_rate = 0.08
		self.move_speed = 0.3
		self.attack_range = 3.0
		self.attack_rate = 60
		self.attack_counter = self.attack_rate
		
		self.target = None

	def __repr__(self):
		return "FIGHTER component of {}".format(self.owner)
			
	def hurt(self, damage, origin=None):
		if origin == None:
			origin = self.owner
		self.HP -= damage
		
		if self.HP <= 0:
			#self.owner.state = 'dead'
			print("R.I.P.   {} has died at the hands of {}".format(self.owner.Name, origin.Name))
			#self.owner.sys['sys'].props.remove(self.owner.own)
			if self.owner.Name != 'Player':
				self.owner.own.scene.addObject(self.owner.Name+"_corpse", self.owner.own)
				self.owner.own.endObject()
			
		elif self.HP >= self.maxHP:	self.HP = self.maxHP
		if self.owner.Name == 'Player':
			value = self.HP / self.maxHP
			logic.sendMessage('update_player_hp', str(value))
		print("{}/{} HP remaining for {}".format(self.HP, self.maxHP, self.owner.Name))
			

	def attack(self):
		d = self.attack_range
		ray = self.owner.ai.sight_ray(d)

		if ray and 'ent' in ray:
			ray['ent'].get_hit(self.owner, self.power)
			brush = self.owner.own.scene.objects['System']
			brush.worldPosition = ray.worldPosition
			brush.worldPosition.z += 1.0
			emitter = self.owner.own.scene.addObject('Blood Spray', brush, 2)
			emitter['impact'] = self.power
		else:
			print("{} swings at the air!".format(self.owner.Name))





class Thing:
	def __init__(self, own, Name, 
					sprite=None, fighter=None, ai=None,
					item=None):
					
		self.own = own
		self.sys = own.scene.objects['System']
		self.Name = Name
		
		self.state = 'alive'
		
		self.sprite = sprite
		
		self.fighter = fighter
		self.ai = ai
		
		self.item = item
		
		if self.sprite:
			self.sprite.owner = self
			
		if self.fighter:	
			self.fighter.owner = self
		
		if self.ai:
			self.ai.owner = self
		
		if self.item:
			self.item.owner = self
			
	def __repr__(self):
		return "THING {} @ x{} y{}".format(self.Name, self.x, self.y)
	
	@property
	def facing(self):
		D = 8	#number of directions desired
		z = self.own.worldOrientation.to_euler().z * (180/pi)
		if z < 0:	z += 360
		facing = round(z / (360/D))
		if facing == D:	facing = 0
		return facing
	
	@property
	def x(self):
		return round(self.own.worldPosition.x/4)
	
	@property
	def y(self):
		return round(self.own.worldPosition.y/4)
	
		
	def get_hit(self, origin, damage):
		print("{} is hit by {} for {} damage!".format(self.Name, origin.Name, damage))
		self.own['sfx_hit'] = True
		#self.own.applyMovement([0,-(damage),damage*0.5], True)
		if self.fighter:
			self.fighter.hurt(damage, origin)
			if self.ai and self.Name != 'Player':	#specials for non-player AI
				self.state = 'hurt'	
				self.ai.last_attacker = origin	#become hostile toward our damage source
			#extra stuff for player hurting
			elif self.Name == 'Player':
				head = self.own.children['Head']
				impact = damage / self.fighter.HP
				head_kick(head,impact)