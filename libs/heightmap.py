import pyglet
import pymunk
from pymunk import Vec2d

import re

from math import sin,cos,tan,degrees,radians,sqrt
import contours

class Contour(object):
	def __init__(self, image_path, space, segment_radius = 3, segment_friction = 1, tolerance = 150):
		remove_base_points = False
		make_loop = False
		order_verts = False

		''' # not reduced
		layers = contours.find_contours(image_path)
		'''
		# reduced
		tmp = contours.find_contours(image_path)
		layers = []
		for layer in tmp:
			if remove_base_points:
				for pos in layer[:]:
					if pos[1] <= 2:
						layer.remove(pos)
				
			layer = pymunk.util.reduce_poly(layer, tolerance=tolerance)
			layers.append(layer)

		radius = segment_radius
		friction = segment_friction
		elasticity = 1

		self.points = []
		'''
		if order_verts:
			new_layers = []
			for layer in layers:
				new_layers.append(sorted(layer, key=lambda a: a[0]))
		else:
			new_layers = layers
		'''
		self.points = []

		for layer in layers:
			i = 0
			for point in layer:
				if point == layer[0]:
					self.points.append(point)

					seg = pymunk.Segment(space.static_body, point, layer[-1], radius)
					seg.group = 2
					seg.elasticity = elasticity
					seg.friction = friction
					space.add(seg)

				else:
					seg = pymunk.Segment(space.static_body, point, layer[i-1], radius)
					seg.group = 2
					seg.elasticity = elasticity
					seg.friction = friction
					space.add(seg)
	
					self.points.append(point)
				i += 1

## old dirty code

'''
		for layer in layers:
			i = 0
			for point in layer:
				if point == layer[0]:
					seg = pymunk.Segment(space.static_body, point, layer[-1], radius)
					seg.group = 2
					seg.elasticity = elasticity
					seg.friction = friction
					space.add(seg)

					self.heightmap_points.append(point)

				else:
					if make_loop:
						seg = pymunk.Segment(space.static_body, point, layer[i-1], radius)
						seg.group = 2
						seg.elasticity = elasticity
						seg.friction = friction
						space.add(seg)

						self.heightmap_points.append(point)
					else:
						if point != layer[1]:
							seg = pymunk.Segment(space.static_body, point, layer[i-1], radius)
							seg.group = 2
							seg.elasticity = elasticity
							seg.friction = friction
							space.add(seg)

							self.heightmap_points.append(point)

				if point == layer[1]:
					self.heightmap_points.append(point)
				i += 1
		'''

if __name__ == '__main__':
	pass