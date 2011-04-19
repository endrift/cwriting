import xml.dom.minidom
import time
import copy

class Document(object):
	def __init__(self):
		self._doc = xml.dom.minidom.Document()
		p = self._doc.createProcessingInstruction('jaxfront', 'version=2.1;time=%s;xui=jar:http://cavewriting.sourceforge.net/2006/CWEditor/cavewriting.jar!/schema/caveschema.xui;xsd=caveschema.xsd' % time.strftime('%Y-%m-%d %H:%M:%S.000'))
		self._doc.appendChild(p)
		self._root = None

	def setRoot(self, node):
		if self._root:
			self._doc.replaceChild(self._root, node)
		else:
			self._doc.appendChild(node)
		self._root = node

	def getNode(self):
		return self._doc

	def save(self, filename):
		f = open(filename, 'w')
		self._doc.writexml(f, encoding="UTF-8")
		f.close()

class Node(object):
	def __init__(self, name):
		self._attrs = {}
		self._props = PropertySet()
		self._children = []
		self._name = name
		self._text = None

	def __repr__(self):
		return '<node.%s: %s>' % (self.__class__.__name__, self._name)

	def genNode(self, doc):
		elt = doc.createElement(self._name)
		for (k, v) in self._attrs.iteritems():
			elt.setAttribute(k, str(v))

		for n in self._props.genNodes(doc):
			elt.appendChild(n)

		for c in self._children:
			#print repr(c)
			elt.appendChild(c.genNode(doc))

		if self._text:
			t = doc.createTextNode(self._text)
			elt.appendChild(t)

		return elt

	def setAttr(self, name, value):
		self._attrs[name] = value

	def setAttrFromNode(self, node):
		self._attrs[node._name] = node

	def addChild(self, child):
		self._children.append(child)

	def clearChildren(self):
		self._children = []

	def setText(self, text):
		self._text = str(text)

	def getText(self):
		return self._text

class Story(Node):
	def __init__(self, version=8, last_xpath="/"):
		super(Story, self).__init__('Story')
		self._roots = {
			'objects': Node('ObjectRoot'),
			'groups': Node('GroupRoot'),
			'timelines': Node('TimelineRoot'),
			'placements': Node('PlacementRoot'),
			'particleactions': Node('ParticleActionRoot')
		}
		self.setAttr('version', version)
		self.setAttr('last_xpath', last_xpath)
		self._global = Global()

		for child in self._roots.values():
			self.addChild(child)
		self.addChild(self._global)

		# Set up the default placements
		center = Placement('Center')
		self._add('placements', center)

	def _add(self, root, node):
		self._roots[root].addChild(node)

	def addObject(self, obj):
		self._add('objects', obj)

	def addGroup(self, group):
		self._add('groups', group)

	def addTimeline(self, timeline):
		self._add('timelines', timeline)

	def addParticleActions(self, pa):
		self._add('particleactions', pa)

class Object(Node):
	def __init__(self, name, obj):
		super(Object, self).__init__('Object')
		self.name = name
		self.setAttr('name', name)
		self._obj = obj
		self._props.copy(obj._props)
		self._content = Node('Content')
		self._link = obj.link

	def genNode(self, doc):
		self.addChild(self._content)
		if self._link:
			self.addChild(self._link)
		return super(Object, self).genNode(doc)

class Property(Node):
	def genDiff(self, current, next):
		return self._genDiff(current, next['time'] - current['time'], next)

class PropertySet(object):
	def __init__(self):
		self._props = {}

	def clear(self):
		self._props.clear()

	def copy(self, other):
		self._props.update(copy.deepcopy(other._props))

	def setProperty(self, name, p):
		self._props[name] = p

	def getProperty(self, name):
		return self._props[name]

	def setBool(self, name, v):
		self._props[name] = Boolean(name, v)

	def setColor(self, name, r, g, b):
		self._props[name] = Color(name, (r, g, b))

	def setScalar(self, name, v):
		self._props[name] = Scalar(name, v)

	def setCoord(self, name, (x, y, z)):
		self._props[name] = Coord(name, (x, y, z))

	def genNodes(self, doc):
		props = []
		for p in self._props.itervalues():
			props.append(p.genNode(doc))

		return props

	def genAttrs(self, parent):
		for p in self._props.itervalues():
			parent.setAttrFromNode(p)

class Placement(Property):
	def __init__(self, name=None, start=(0, 0, 0), rotation=None):
		super(Placement, self).__init__('Placement')
		self.position = list(start)
		self.relativeTo = 'Center'
		self.rotation = rotation or AxisRotation()
		self.name = name

	def __eq__(self, rhs):
		return self.position == rhs.position and self.relativeTo == rhs.relativeTo and self.rotation == rhs.rotation

	def _genDiff(self, current, delta, next):
		if current['value'] == next['value']:
			return None
		return Movement(next['time'] - current['time'], next['value'])

	def move(self, rhs):
		self.position = [l + r for (l, r) in zip(self.position, rhs.position)]
		self.rotation.rotate(rhs.rotation)

	def moved(self, rhs):
		lhs = copy.deepcopy(self)
		lhs.move(rhs)
		return lhs

	def genCurve(self, end, curve):
		diffPos = [r - l for (l, r) in zip(self.position, end.position)]
		# TODO diff rotation
		diffRot = None
		def move(t):
			tAfter = curve(t)
			pos = [(1 - c)*s + c*e for (s, e, c) in zip([0, 0, 0], diffPos, tAfter)]
			placement = copy.deepcopy(self)
			placement.move(Placement(start=pos))
			return placement

		return move

	def genNode(self, doc):
		self.clearChildren()
		if self.name:
			self.setAttr('name', self.name)

		n = Node('RelativeTo')
		n.setText(self.relativeTo)
		self.addChild(n)
		n = Coord('Position', self.position)
		self.addChild(n)
		self.addChild(self.rotation)
		return super(Placement, self).genNode(doc)

class Group(Node):
	def __init__(self, name):
		super(Group, self).__init__('Group')
		self.name = name
		self.setAttr('name', name)

	def addObject(self, obj):
		self.clearChildren()
		n = Node('Objects')
		n.setAttr('name', obj.name)
		self.addChild(n)

class Timeline(Node):
	def __init__(self, name, autostart=False):
		super(Timeline, self).__init__('Timeline')
		self.name = name
		self.setAttr('name', name)
		self.setAttrFromNode(Boolean('start-immediately', autostart))

	def addAction(self, start, action):
		ta = TimedActions(start)
		ta.addAction(action)
		self.addChild(ta)

	def addTimedAction(self, ta):
		self.addChild(ta)

class TimedActions(Node):
	def __init__(self, start):
		super(TimedActions, self).__init__('TimedActions')
		self.start = start
		self.setAttr('seconds-time', start)

	def addAction(self, action):
		self.addChild(action)

class Link(Node):
	def __init__(self):
		super(Link, self).__init__('LinkRoot')
		self._root = Node('Link')
		self._root._props.setBool('Enabled', True)
		self._root._props.setBool('RemainEnabled', True)
		self._root._props.setColor('EnabledColor', 0, 128, 255)
		self._root._props.setColor('SelectedColor', 255, 0, 0)
		self.addChild(self._root)

	def addAction(self, action):
		n = Node('Actions')
		clicks = Node('Clicks')
		a = Node('any')
		clicks.addChild(a)
		n.addChild(clicks)
		n.addChild(action)
		self._root.addChild(n)

class Global(Node):
	def __init__(self):
		super(Global, self).__init__('Global')

		# Set some defaults
		self._camera = (100, Placement(start=(0, 0, 6)))
		self._caveCam = (100, Placement(start=(0, 0, 0)))
		self._bg = Color('color', (0, 0, 0))

		self._wandRot = Boolean('allow-rotation', False)
		self._wandMov = Boolean('allow-movement', False)

		self._bgNode = Node('Background')
		self.addChild(self._bgNode)

		self._wand = Node('WandNavigation')
		self.addChild(self._wand)

		cam = Node('CameraPos')
		cam.setAttr('far-clip', self._camera[0])
		cam.addChild(self._camera[1])
		self.addChild(cam)

		cam = Node('CaveCameraPos')
		cam.setAttr('far-clip', self._caveCam[0])
		cam.addChild(self._caveCam[1])
		self.addChild(cam)

	def genNode(self, doc):
		self._bgNode.setAttrFromNode(self._bg)
		self._wand.setAttrFromNode(self._wandRot)
		self._wand.setAttrFromNode(self._wandMov)
		return super(Global, self).genNode(doc)

# Objects

class Text(Object):
	def __init__(self, name, text):
		super(Text, self).__init__(name, text)

	def genNode(self, doc):
		self.clearChildren()
		tnode = Node('Text')
		tnode.setAttr('horiz-align', self._obj.halign)
		tnode.setAttr('vert-align', self._obj.valign)
		tnode.setAttr('depth', self._obj.depth)

		tsubnode = Node('text')
		tsubnode.setText(self._obj.getText())

		tnode.addChild(tsubnode)
		self._content.addChild(tnode)

		return super(Text, self).genNode(doc)

class ParticleSystem(Object):
	def __init__(self, name, ps):
		super(ParticleSystem, self).__init__(name, ps)

	def genNode(self, doc):
		self.clearChildren()
		pnode = Node('ParticleSystem')
		pnode.setAttr('max-particles', self._obj.maxParticles)
		pnode.setAttr('actions-name', self._obj.actions.name)
		pnode.setAttr('particle-group', self._obj.particles.name)
		pnode.setAttrFromNode(Boolean('look-at-camera', self._obj.lookAtCamera))
		pnode.setAttrFromNode(Boolean('sequential', self._obj.sequential))
		pnode.setAttr('speed', self._obj.speed)
		self._content.addChild(pnode)

		return super(ParticleSystem, self).genNode(doc)

# Actions

class ObjectChange(Node):
	def __init__(self, obj):
		super(ObjectChange, self).__init__('ObjectChange')
		self.setAttr('name', obj.name)

class GroupRef(Node):
	def __init__(self, obj):
		super(GroupRef, self).__init__('GroupRef')
		self.setAttr('name', obj.name)

class Transition(Node):
	def __init__(self, duration):
		super(Transition, self).__init__('Transition')
		self.setAttr('duration', duration)
		
class MoveRel(Transition):
	def __init__(self, duration, delta):
		super(MoveRel, self).__init__(duration)
		move = Node('MoveRel')
		move.addChild(delta)

class Movement(Transition):
	def __init__(self, duration, newloc):
		super(Movement, self).__init__(duration)
		move = Node('Movement')
		move.addChild(newloc)
		self.addChild(move)

class TimerChange(Node):
	def __init__(self, timer, kind='start'):
		super(TimerChange, self).__init__('TimerChange')
		self.setAttr('name', timer.name)
		action = Node(kind)
		self.addChild(action)

# Values

class Value(Property):
	def __str__(self):
		return self.getText()

	def __repr__(self):
		return '<node.%s: %s (%s)>' % (self.__class__.__name__, self._name, str(self))

	def __eq__(self, rhs):
		return self._v == rhs._v

	def _genDiff(self, current, delta, next):
		if current['value'] == next['value']:
			return None

		d = Transition(delta)
		d.addChild(copy.deepcopy(next['value']))
		return d

	def getValue(self):
		return self._v

class Color(Value):
	def __init__(self, name, (r, g, b)):
		super(Color, self).__init__(name)
		self.setValue((r, g, b))

	def setValue(self, (r, g, b)):
		self._v = (r, g, b)
		self.setText('%i,%i,%i' % (r, g, b))

class Boolean(Value):
	def __init__(self, name, value=False):
		super(Boolean, self).__init__(name)
		self.setValue(value)

	def setValue(self, value):
		assert(value is not self)
		self._v = value
		self.setText('true' if value else 'false')

	def genCurve(self, end, curve):
		return (lambda t: end.getValue() if curve(t) > 0 else self.getValue())

class Scalar(Value):
	def __init__(self, name, value=False):
		super(Scalar, self).__init__(name)
		self.setValue(value)

	def setValue(self, value):
		self._v = value
		self.setText(value)

class Coord(Value):
	def __init__(self, name, (x, y, z)):
		super(Coord, self).__init__(name)
		self.setValue((x, y, z))

	def setValue(self, (x, y, z)):
		self._v = (x, y, z)
		self.setText('(%f, %f, %f)' % (x, y, z))

# Rotations

class AxisRotation(Node):
	def __init__(self, axis=(0, 1, 0), rotation=0):
		super(AxisRotation, self).__init__('Axis')
		self.axis = Coord('rotation', axis)
		self.angle = Scalar('angle', rotation)
		self.setAttrFromNode(self.axis)
		self.setAttrFromNode(self.angle)

	def __eq__(self, rhs):
		return self.axis == rhs.axis and self.angle == rhs.angle

	def rotate(self, other):
		pass

	def project(self, (x, y, z)):
		pass

# Particle-related classes

class ParticleActionList(Node):
	def __init__(self, name):
		super(ParticleActionList, self).__init__('ParticleActionList')
		self.name = name
		self.setAttr('name', name)
		self._source = Node('Source')
		self._sourceDomain = None
		self._rate = Scalar('rate', 1)
		self._vel = Node('Vel')
		self._velDomain = None
		self._actions = []
		self._remove = None

	def setSource(self, source):
		self._sourceDomain = source
		self._source.clearChildren()
		self._source.addChild(self._sourceDomain)

	def setVel(self, vel):
		self._velDomain = vel
		self._vel.clearChildren()
		self._vel.addChild(self._velDomain)

	def setRate(self, rate):
		self._rate.setValue(rate)

	def setRemoveCondition(self, remove):
		self._remove = remove

	def addAction(self, action):
		self._actions.append(action)

	def genNode(self, doc):
		self.clearChildren()
		self.setAttr('name', self.name)
		self.addChild(self._source)
		self._source.setAttrFromNode(self._rate)
		self.addChild(self._vel)
		for pa in self._actions:
			self.addChild(pa)
		self.addChild(self._remove)

		return super(ParticleActionList, self).genNode(doc)

# ParticleDomains

# TODO: cleanup these sorts of classes

class ParticleDomain(Node):
	def __init__(self):
		super(ParticleDomain, self).__init__('ParticleDomain')
		self._domProps = PropertySet()
		self._dom = None

	def genNode(self, doc):
		self.clearChildren()
		self.addChild(self._dom)
		self._domProps.genAttrs(self._dom)

		return super(ParticleDomain, self).genNode(doc)

class Disc(ParticleDomain):
	def __init__(self):
		super(Disc, self).__init__()
		self._dom = Node('Disc')
		self._domProps.setCoord('center', (0, 0, 0))
		self._domProps.setCoord('normal', (0, -1, 0))
		self._domProps.setScalar('radius', 4.0)
		self._domProps.setScalar('radius-inner', 0.0)

	def setCenter(self, (x, y, z)):
		self._domProps.getProperty('center').setValue((x, y, z))

	def setNormal(self, (x, y, z)):
		self._domProps.getProperty('normal').setValue((x, y, z))

	def setRadius(self, r):
		self._domProps.getProperty('radius').setValue(r)

	def setRadiusInner(self, r):
		self._domProps.getProperty('radius-inner').setValue(r)

class Box(ParticleDomain):
	def __init__(self):
		super(Box, self).__init__()
		self._dom = Node('Box')
		self._domProps.setCoord('p1', (0, 0, 0))
		self._domProps.setCoord('p2', (0, 0, 0))

	def setP1(self, (x, y, z)):
		self._domProps.getProperty('p1').setValue((x, y, z))

	def setP2(self, (x, y, z)):
		self._domProps.getProperty('p2').setValue((x, y, z))

# ParticleActions

class ParticleAction(Node):
	def __init__(self):
		super(ParticleAction, self).__init__('ParticleAction')
		self._paProps = PropertySet()
		self._pa = None

	def genNode(self, doc):
		self.clearChildren()
		self.addChild(self._pa)
		self._paProps.genAttrs(self._pa)

		return super(ParticleAction, self).genNode(doc)

class Gravity(ParticleAction):
	def __init__(self):
		super(Gravity, self).__init__()
		self._pa = Node('Gravity')
		self._paProps.setCoord('direction', (0, 1, 0))

	def setDirection(self, (x, y, z)):
		self._paProps.getProperty('direction').setValue((x, y, z))

# RemoveConditions

class RemoveCondition(Node):
	def __init__(self):
		super(RemoveCondition, self).__init__('RemoveCondition')
		self._rcProps = PropertySet()
		self._rc = None

	def genNode(self, doc):
		self.clearChildren()
		self.addChild(self._rc)
		self._rcProps.genAttrs(self._rc)

		return super(RemoveCondition, self).genNode(doc)

class Age(RemoveCondition):
	def __init__(self, age, youngerThan=False):
		super(Age, self).__init__()
		self._rc = Node('Age')
		self._rcProps.setScalar('age', age)
		self._rcProps.setBool('younger-than', youngerThan)
