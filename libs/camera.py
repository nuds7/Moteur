from __future__ import division
import pyglet
from pyglet.gl import *
from math import sin,cos,tan
import pymunk
from pymunk import Vec2d

import utils
import ctypes

def world_mouse(mX, mY, camera_pos_x, camera_pos_y, camera_scale, screen_resolution):
	aspect = screen_resolution[0]/screen_resolution[1]
	wmX = (camera_pos_x - (camera_scale*aspect)) + mX*((camera_scale*aspect)/screen_resolution[0])*2
	wmY = (camera_pos_x - (camera_scale)) + mY*((camera_scale)/screen_resolution[1])*2
	wmPos = wmX, wmY
	print(wmPos)
	return wmPos

class Camera(object):
	def __init__ (self, screen_size, map_size, position,
						rate = [10,10], scale_rate = 30):
		self.position 			= position
		self.screen_size 		= screen_size
		self.width, self.height = screen_size
		self.aspect 			= screen_size[0] / screen_size[1]
		self.map_size 			= map_size
		self.newPositionX 		= 0
		self.newPositionY 		= 0
		self.newAngle 			= 0
		self.newWeightedScale 	= 180
		self.newTarget 			= [0,0]
		self.scale 				= 60

		self.taret 				= (0,0)

		self.scaleRate 			= scale_rate
		self.rate 				= rate
		self.vel_zoom 			= 0
		self.new_vel_zoom 		= 0
		
	def update(self, target, angle):
		#self.target = target
		
		self.newPositionX 		= utils.weighted_average(self.newPositionX,target[0],self.rate[0])
		self.newPositionY 		= utils.weighted_average(self.newPositionY,target[1],self.rate[1])
		self.newWeightedScale 	= utils.weighted_average(self.newWeightedScale,self.scale,self.scaleRate)
		
		self.new_vel_zoom 	= utils.weighted_average(self.new_vel_zoom,self.vel_zoom,20)
		
		glViewport(0, 0, self.screen_size[0], self.screen_size[1])

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

		# fov (120), aspect, near, far clipping planes
		gluPerspective(self.newWeightedScale, self.aspect, 10.0, -10.)
		#self.newAngle = ((self.newAngle*(30-1))+angle) / 30

		#glRotatef(self.newAngle,0.0,0.0,1.0)
		
		# position of the camera
		gluLookAt(self.newPositionX-self.new_vel_zoom, self.newPositionY+(self.new_vel_zoom*.5), +370,
				  self.newPositionX, self.newPositionY, 0,
				  sin(0),1,0.0)

		#glRotatef(0, 0., 1., 0.)

		#glScalef(2.0, 2.0, 2.0)
		#glTranslatef(self.newPositionX*-1, self.newPositionY*-1, 100)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()


	def edge_bounce(self, dx, dy, cameraPos):
		if (self.scale*self.aspect)*2 < self.map_size[0]:
			if cameraPos[0] < self.newWeightedScale*self.aspect:
				self.newPositionX -= dx*((self.newWeightedScale*self.aspect)/(self.screen_size[0]/2))
				cameraPos[0] = self.newWeightedScale*self.aspect
			if cameraPos[0] > self.map_size[0] - self.newWeightedScale*self.aspect:
				self.newPositionX -= dx*((self.newWeightedScale*self.aspect)/(self.screen_size[0]/2))
				cameraPos[0] = self.map_size[0] - self.newWeightedScale*self.aspect

		if self.scale*2 < self.map_size[1]:
			if cameraPos[1] < self.newWeightedScale:
				self.newPositionY -= dy*((self.newWeightedScale)/(self.screen_size[1]/2))
				cameraPos[1] = (self.newWeightedScale)
			if cameraPos[1] > self.map_size[1] - self.newWeightedScale:
				self.newPositionY -= dy*((self.newWeightedScale)/(self.screen_size[1]/2))
				cameraPos[1] = self.map_size[1] - self.newWeightedScale
		return cameraPos

	def zoom(self, scroll_y):
		self.scale -= scroll_y*5

	def ui_mode(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluOrtho2D(0, self.screen_size[0], 0, self.screen_size[1])
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_3d(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glEnable(GL_DEPTH_TEST)         # enable depth testing
		# reset modelview matrix
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_2d(self):
		glDisable(GL_DEPTH_TEST)
		# store the projection matrix to restore later
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()

		# load orthographic projection matrix
		glLoadIdentity()
		#glOrtho(0, float(self.width),0, float(self.height), 0, 1)
		far = 8192
		glOrtho(-self.width / 2., self.width / 2., -self.height / 2., self.height / 2., -10, far)

		# reset modelview
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		#glClear(GL_COLOR_BUFFER_BIT)
	def draw_2d(self):
		glTranslatef(self.newPositionX*-1, self.newPositionY*-1, 100)

	def unset_2d(self):
		# load back the projection matrix saved before
		glMatrixMode(GL_PROJECTION)
		glPopMatrix() 