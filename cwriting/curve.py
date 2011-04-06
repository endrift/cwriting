import cwriting.node as node

import math

const1 = (lambda x: (lambda t: x))
zero1 = const1(0)
one1 = const1(1)
floor1 = (lambda t: math.floor(t))
linear1 = (lambda t: t)
quadIn1 = (lambda t: t*t)
quadOut1 = (lambda t: (2 - t)*t)

class Curve2D(object):
	def __init__(self, x, y):
		self._x = x
		self._y = y

	def __call__(self, t):
		return self._x(t), self._y(t)

const2 = (lambda x, y: (lambda t: (x, y)))
zero2 = const2(0, 0)
one2 = const2(1, 1)
floor2 = (lambda t: (math.floor(t), math.floor(t)))
linear2 = (lambda t: (t, t))
quadIn2 = (lambda t: (t*t, t*t))
quadOut2 = (lambda t: ((2 - t)*t, (2 - t)*t))

class Curve3D(object):
	def __init__(self, x, y, z):
		self._x = x
		self._y = y
		self._z = z

	def __call__(self, t):
		return self._x(t), self._y(t), self._z(t)

const3 = (lambda x, y, z: (lambda t: (x, y, z)))
zero3 = const3(0, 0, 0)
one3 = const3(1, 1, 1)
floor3 = (lambda t: (math.floor(t), math.floor(t), math.floor(t)))
linear3 = (lambda t: (t, t, t))
quadIn3 = (lambda t: (t*t, t*t, t*t))
quadOut3 = (lambda t: ((2 - t)*t, (2 - t)*t, (2 - t)*t))

class Map(object):
	pass

class PlanarMap(Map):
	def __init__(self, prop, rot, d):
		self._rotation = rot
		self._displacement = d
		self.prop = 'Placement'

	def __call__(self, x, y, z):
		# TODO project x, y, z onto s, t
		s, t = x, z
		return self.value(s, t)

class HeightMap(PlanarMap):
	def __init__(self, rot, d, z, n=None):
		super(HeightMap, self).__init__('Placement', rot, d)
		self._z = z
		self._n = n

	def value(self, s, t):
		p = node.Placement(start=(s, self.height(s, t), t))
		# TODO rotation
		return p

	def height(self, s, t):
		return self._z(s, t) - self._displacement

	def normal(self, s, t):
		if self._n:
			return self._n(s, t)
		else:
			return node.AxisRotation()
