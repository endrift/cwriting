import node
import copy

class Document(object):
	def __init__(self):
		self._objs = []
		self._groups = []
		self._times = []

	def registerObject(self, obj):
		self._objs.append(copy.copy(obj)) # TODO should this be a deep copy?

	def registerTimeline(self, obj):
		self._times.append(obj)

	def distill(self):
		doc = node.Document()
		story = node.Story()
		for obj in self._objs:
			for o in obj.distill():
				story.addObject(o)

		for group in self._groups:
			story.addGroup(group.distill())

		for timeline in self._times:
			story.addTimeline(timeline.distill())

		doc.setRoot(story.genNode(doc.getNode()))
		return doc

	def save(self, filename):
		xml = self.distill()
		xml.save(filename)

class Timeline(object):
	def __init__(self, name, autostart=False):
		self._time = 0.0
		self.name = name
		self._loop = False
		self._autostart = autostart

		self._first = {}
		self._current = {}
		self._previous = []

		self._changes = []

	def _genDiff(self, current, next):
			key = (next['object'], next['property'])
			if key in current:
				diff = current[key]['value'].genDiff(current[key], next)
				if diff:
					ta = node.TimedActions(current[key]['time'])
					ta.addAction(diff)
					self._changes.append(ta)

			current[key] = next

	def advance(self, n):
		self._time += n

	def current(self):
		return self._time

	def key(self, prop, obj, value):
		key = (prop, obj)
		data = {
			'time': self._time,
			'object': obj,
			'property': prop,
			'value': copy.deepcopy(value) }

		if key not in self._first:
			self._first[key] = data

		if key in self._current:
			self._previous.append(self._current[key])

		self._current[key] = data

	def freeze(self, loop=False):
		self._changes = []
		self._loop = loop
		current = {}

		for next in self._previous:
			self._genDiff(current, next)

		for next in self._current.itervalues():
			self._genDiff(current, next)

		# TODO looping
		if loop:
			ta = node.TimedActions(self._time)
			ta.addAction(node.TimerChange(self))
			self._changes.append(ta)

	def distill(self):
		if not self._changes:
			self.freeze()

		topNode = node.Timeline(self.name, self._autostart)

		for change in self._changes:
			topNode.addTimedAction(change)

		return topNode

class Object(object):
	def __init__(self, name):
		self.name = name
		self._props = node.PropertySet()
		self._props.setProperty('Placement', node.Placement())
		self._props.setBool('Visible', True)
		self._props.setColor('Color', 255, 255, 255)
		self._props.setBool('Lighting', False)
		self._props.setBool('ClickThrough', True)
		self._props.setBool('AroundSelfAxis', False)
		self._props.setScalar('Scale', 1.0)
		self.link = None

	def copyAttributes(self, other):
		self._props.clear()
		self._props.copy(other._props)

	def setPlacement(self, placement):
		self._props.setProperty('Placement', copy.deepcopy(placement))

	def getPlacement(self):
		return self._props.getProperty('Placement')

	def setVisibility(self, v):
		self._props.getProperty('Visible').setValue(v)

	def keyPlacement(self, timeline):
		timeline.key('Placement', self, self._props.getProperty('Placement'))

	def keyVisibility(self, timeline):
		timeline.key('Visible', self, self._props.getProperty('Visible'))

class Text(Object):
	def __init__(self, name, text):
		super(Text, self).__init__(name)
		self._text = text
		self.halign = 'center'
		self.valign = 'center'
		self.depth = 0
		self._letters = []

	def breakApart(self, curve=None):
		self._letters = []
		i, j = (0, 0)
		for c in self._text:
			if c == '\n':
				i = 0
				j += 1
				l = None
			elif c == ' ':
				l = None
			else:
				l = Text('%s_%05d' % (self.name, i), c)
				l.copyAttributes(self)
				if curve:
					offset = curve.get(i, j)
					l.move(offset)
			self._letters.append(l)
			i += 1

		return self._letters

	def getText(self):
		return self._text

	def distill(self):
		nodes = []
		if self._letters:
			for l in self._letters:
				if l:
					nodes.extend(l.distill())
		else:
			nodes = [node.Text(self.name, self)]

		return nodes
