import os, sys
import pyglet
from pyglet.gl import *
'''
import pymunkoptions
pymunkoptions.options["debug"] = False
'''
import pymunk
from pymunk import Vec2d
import math
from math import sin,cos,tan,degrees,sqrt,atan2,radians

import pyglet_util
import camera
import vehicle
from heightmap import Contour

import entities
import utils
import meshpy

import obj_batch
import ctypes

def angle_between_lines(line1, line2):
	dx1 = line1[1][0] - line1[0][0]
	dy1 = line1[1][1] - line1[0][1]

	dx2 = line2[1][0] - line2[0][0]
	dy2 = line2[1][1] - line2[0][1]

	d = dx1*dx2 + dy1*dy2
	l2 = (dx1*dx1+dy1*dy1)*(dx2*dx2+dy2*dy2)

	return math.acos(d/math.sqrt(l2))

def clear_space(space):
	for c in space.constraints:
		space.remove(c)
	for s in space.shapes:
		space.remove(s)
	for b in space.bodies:
		space.remove(b)
		
class GameLevel1(object):
	def __init__(self):
		pass
	def define_level(self, space):
		segments = (pymunk.Segment(space.static_body, (-200,0), 	(500,0), 	4),
					pymunk.Segment(space.static_body, (-200,0), 	(-200,100), 4),
					pymunk.Segment(space.static_body, (500,-80),  	(800,-80), 	4),
					pymunk.Segment(space.static_body, (800,-180),  	(1200,-180),4),
					pymunk.Segment(space.static_body, (1200,-240), 	(1800,-240),4),
					pymunk.Segment(space.static_body, (-180,100),	(-160,100), 4),
					pymunk.Segment(space.static_body, (-160,100),	(-100,50),  4),)
		for seg in segments:
			seg.friction 	= .8
			seg.elasticity 	= 1
		space.add(segments)


		self.car = vehicle.Car(space, (-140,350))
		
		'''
		size = (60,20)
		mass = .0075
		box_moment = pymunk.moment_for_box(mass, size[0], size[1])
		for i in range(5):
			box_body = pymunk.Body(mass, box_moment)
			box_body.position = 300,(18+(size[1]*i))
			
			box_shape = pymunk.Poly.create_box(box_body, size=size)
			box_shape.friction = .7
			box_shape.elasticity = .5

			space.add(box_body, box_shape)

			box_body.sleep()
		entities.SoftBody(space, (700,100), 70, poly=6, friction=.2)
		'''


	def update_controls(self, keys):
		self.car.control(keys)
	def draw(self):
		pass

def round_trip_connect(start, end):
	result = []
	for i in range(start, end):
	  result.append((i, i+1))
	result.append((end, start))
	return result

class GameLevel2(object):
	def __init__(self):
		pass
	def define_level(self, scene):
		self.scene = scene
		heightmap = Contour('resources/test3.bmp', scene.space, 
							tolerance = 400, segment_radius = .5)

		glShadeModel(GL_SMOOTH) # (GL_SMOOTH/GL_FLAT)
		#glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # wireframe

		intensity = .2
		intensity2 = .2
		r = .1
		g = .1
		b = .1

		spread = .2, .2, .2

		fourfv = ctypes.c_float * 4

		glLightfv(GL_LIGHT0, GL_POSITION, fourfv(100, 5000, 200, 1))
		glLightfv(GL_LIGHT0, GL_AMBIENT, fourfv(spread[0], spread[1], spread[2], intensity))
		glLightfv(GL_LIGHT0, GL_DIFFUSE, fourfv(r, g, b, intensity))
		glLightfv(GL_LIGHT0, GL_SPECULAR, fourfv(r, g, b, intensity))
		

		r2, g2, b2 = .3, .3, .3

		glLightfv(GL_LIGHT1, GL_POSITION, fourfv(0, 0, 0, 1))
		glLightfv(GL_LIGHT1, GL_AMBIENT, fourfv(r2, g2, b2, intensity2))
		glLightfv(GL_LIGHT1, GL_DIFFUSE, fourfv(r2, g2, b2, intensity2))
		glLightfv(GL_LIGHT1, GL_SPECULAR, fourfv(r2, g2, b2, intensity2))

		glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
		glEnable(GL_LIGHT0)
		#glEnable(GL_LIGHT1)
		# http://geoffrey.googlecode.com/svn-history/r1/trunk/geoffrey.py

		self.land_batch = pyglet.graphics.Batch()

		o = obj_batch.OBJ.from_resource('testmodel1.obj')
		o.load_identity()
		o.scale(100, 100, 100)
		o.add_to(self.land_batch)
		'''
		t = obj_batch.OBJ.from_resource('tree.obj')
		t.load_identity()
		t.scale(100, 100, 100)
		t.add_to(self.land_batch)
		'''

		'''
		size = (60,20)
		mass = .0001
		box_moment = pymunk.moment_for_box(mass, size[0], size[1])
		for i in range(5):
			box_body = pymunk.Body(mass, box_moment)
			box_body.position = 300,(400+(size[1]*i))
			
			box_shape = pymunk.Poly.create_box(box_body, size=size)
			box_shape.friction = .7
			box_shape.elasticity = .5

			scene.space.add(box_body, box_shape)

			#box_body.sleep()
		entities.SoftBody(scene.space, (700,100), 70, poly=6, friction=.2)
		'''

		self.player = vehicle.Jeep(scene, (100,250))

	def update_controls(self, keys):
		self.player.control(keys)

	def draw(self):
		self.player.draw()

		fourfv = ctypes.c_float * 4
		glLightfv(GL_LIGHT1, GL_POSITION, fourfv(self.player.body.position[0], self.player.body.position[1]+10, 1, 1))
		##
		glEnable(GL_COLOR_MATERIAL)
		glEnable(GL_LIGHTING)

		self.land_batch.draw()

		glDisable(GL_LIGHTING)
		##

		
class Scene(object):
	def __init__(self, window, level):
		pass
	def update(self, dt):
		raise NotImplementedError
	def update_half(self, dt):
		raise NotImplementedError
	def update_third(self, dt):
		raise NotImplementedError
	def world_pos(self, x, y):
		raise NotImplementedError
	def keyboard_input(self, dt):
		raise NotImplementedError
	def on_key_press(self, symbol, modifiers):
		raise NotImplementedError
	def on_key_release(self, symbol, modifiers):
		raise NotImplementedError
	def on_mouse_press(self, x, y, button, modifierse):
		raise NotImplementedError
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		raise NotImplementedError
	def on_mouse_release(self, x, y, button, modifiers):
		raise NotImplementedError
	def on_mouse_motion(self, x, y, dx, dy):
		raise NotImplementedError
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		raise NotImplementedError

class Pymunk_Scene(Scene):
	def __init__(self, window, level):
		super(Pymunk_Scene, self).__init__(window, level)
		self.screen_resolution 	= window.width,window.height
		self.window 			= window

		self.debug_batch 		= pyglet.graphics.Batch()
		self.normal_batch 		= pyglet.graphics.Batch()
		self.ui_batch 			= pyglet.graphics.Batch()

		# The common_group parent keeps groups from 
		# overlapping on accident. Silly Pyglet!
		common_group 			= pyglet.graphics.OrderedGroup(1) 
		self.ordered_group10	= pyglet.graphics.OrderedGroup(10, 	parent = common_group)
		self.ordered_group9 	= pyglet.graphics.OrderedGroup(9, 	parent = common_group)
		self.ordered_group8 	= pyglet.graphics.OrderedGroup(8, 	parent = common_group)
		self.ordered_group7		= pyglet.graphics.OrderedGroup(7, 	parent = common_group)
		self.ordered_group6		= pyglet.graphics.OrderedGroup(6, 	parent = common_group)
		self.ordered_group5		= pyglet.graphics.OrderedGroup(5, 	parent = common_group)
		self.ordered_group4		= pyglet.graphics.OrderedGroup(4, 	parent = common_group)
		self.ordered_group3 	= pyglet.graphics.OrderedGroup(3,	parent = common_group)
		self.ordered_group2		= pyglet.graphics.OrderedGroup(2, 	parent = common_group)
		self.ordered_group1		= pyglet.graphics.OrderedGroup(1, 	parent = common_group)

		self.space 						= pymunk.Space()
		self.space.sleep_time_threshold = 1
		self.space.gravity 				= (0,-800)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		#glEnable(GL_LINE_SMOOTH)
		glPointSize(3)
		glLineWidth(1) #(1.25)

		self.map_size = [1920,1080]
		self.camera = camera.Camera(self.screen_resolution, 
									self.map_size, [0,0],
									rate = [8,5])

		#### Level ####
		self.level = level
		self.level.define_level(self)
		
		self.camera.newPositionX,self.camera.newPositionY = self.level.player.body.position
		#### Level ####

		self.pymunk_util = pyglet_util.PymunkUtil2(self)
		self.pymunk_util.setup()

		self.keys_held = []

		self.mouse_interact = pyglet_util.MouseInteraction(self)

	def update(self, dt):
		self.level.update_controls(self.keys_held)

	def update_half(self, dt):
		pass
		
	def update_third(self, dt):
		pass

	def draw(self):
		self.space.step(.015)
		self.pymunk_util.update()
		self.camera.update([self.level.player.body.position[0], self.level.player.body.position[1]], 0)

		glClearColor(0,0,0,1)

		self.camera.set_3d()

		self.level.draw()

		self.debug_batch.draw()
		self.normal_batch.draw()

		self.level.draw()

		self.camera.ui_mode()
		self.ui_batch.draw()

	def world_pos(self, x, y):
		# Depends on the position of the camera.
		pass
	def keyboard_input(self, dt):
		pass
	def on_key_press(self, symbol, modifiers):
		pass
	def on_key_release(self, symbol, modifiers):
		if symbol == pyglet.window.key.R:
			self.manager.go_to(Pymunk_Scene(self.window, self.level))
		if symbol == pyglet.window.key.ESCAPE:
			self.manager.go_to(Menu_Scene(self.window, self.level))
		if symbol == pyglet.window.key.C:
			self.camera.scale = 120
		if symbol == pyglet.window.key.X:
			self.camera.scale = 90
	def on_mouse_press(self, x, y, button, modifiers):
		self.mouse_interact.on_mouse_press((x,y), button)
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.mouse_interact.on_mouse_drag((x,y), buttons)
	def on_mouse_release(self, x, y, button, modifiers):
		self.mouse_interact.on_mouse_release((x,y), button)
	def on_mouse_motion(self, x, y, dx, dy):
		self.mouse_interact.on_mouse_motion((x,y))
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.camera.zoom(scroll_y)


from simplui import *

class Menu_Scene(Scene):
	def __init__(self, window, level):
		super(Menu_Scene, self).__init__(window, level)
		self.screen_resolution 	= window.width,window.height
		self.window = window

		self.debug_batch 		= pyglet.graphics.Batch()
		self.normal_batch 		= pyglet.graphics.Batch()
		self.ui_batch 			= pyglet.graphics.Batch()

		# The common_group parent keeps groups from 
		# overlapping on accident. Silly Pyglet!
		common_group 			= pyglet.graphics.OrderedGroup(1) 
		self.ordered_group10	= pyglet.graphics.OrderedGroup(10, 	parent = common_group)
		self.ordered_group9 	= pyglet.graphics.OrderedGroup(9, 	parent = common_group)
		self.ordered_group8 	= pyglet.graphics.OrderedGroup(8, 	parent = common_group)
		self.ordered_group7		= pyglet.graphics.OrderedGroup(7, 	parent = common_group)
		self.ordered_group6		= pyglet.graphics.OrderedGroup(6, 	parent = common_group)
		self.ordered_group5		= pyglet.graphics.OrderedGroup(5, 	parent = common_group)
		self.ordered_group4		= pyglet.graphics.OrderedGroup(4, 	parent = common_group)
		self.ordered_group3 	= pyglet.graphics.OrderedGroup(3,	parent = common_group)
		self.ordered_group2		= pyglet.graphics.OrderedGroup(2, 	parent = common_group)
		self.ordered_group1		= pyglet.graphics.OrderedGroup(1, 	parent = common_group)

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		themes = [Theme('themes/game'), Theme('themes/pywidget')]
		theme = 0
		self.frame = Frame(themes[theme], w=window.width, h=window.height)
		# let the frame recieve events from the window
		window.push_handlers(self.frame)
		# create and add a second window

		buttons = []
		for i in range(6):
			if i == 0:
				buttons.append(Label('Select a level to play!'))
				#buttons.append(Checkbox('Game?', h=100))
			buttons.append(Button('Level '+str(i), action=self.load_level))

		self.dialogue = Dialogue('Level Select', x=(window.width//2) - 60, y=(self.window.height//2), 
			content = VLayout(w=50,children=buttons))

		self.frame.add( self.dialogue )

	def update(self, dt):
		pass
	def update_half(self, dt):
		pass
	def update_third(self, dt):
		pass
	def draw(self):
		glClearColor(.1,.1,.12,1)
		self.normal_batch.draw()
		self.debug_batch.draw()
		self.ui_batch.draw()
		self.frame.draw()
	def world_pos(self, x, y):
		pass
	def keyboard_input(self, dt):
		pass
	def on_key_press(self, symbol, modifiers):
		pass
	def on_key_release(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			pyglet.app.exit()
	def on_mouse_press(self, x, y, button, modifiers):
		pass
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass
	def on_mouse_release(self, x, y, button, modifiers):
		pass
	def on_mouse_motion(self, x, y, dx, dy):
		pass
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		pass

	def load_level(self, button):
		print('-----\nLoading: "'+button._get_text()+'"')

		self.window.pop_handlers()
		self.manager.go_to(Pymunk_Scene(self.window, GameLevel2()))


class SceneManager(object):
	def __init__(self, window, level):
		self.go_to(Menu_Scene(window, level))
	def go_to(self, scene):
		self.scene = scene
		self.scene.manager = self