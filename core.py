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
	def __init__(self, name):
		self._time = 0.0
		self.name = name
		self._loop = False

		self._first = {}
		self._current = {}
		self._previous = []

		self._changes = []

	def _genDiff(self, current, next):
			key = (next['object'], next['property'])
			if key in current:
				diff = current[key]['value'].genDiff(current[key], next)
				if diff:
					self._changes.append(diff)

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

		topNode = node.Timeline(self.name)

		for change in self._changes:
			topNode.addTimedAction(change)

		return topNode

class Object(object):
	def __init__(self, name):
		self.name = name
		self._placement = node.Placement()
		self._visibility = node.Boolean('Visible', True)

	def copyAttributes(self, other):
		self._placement = copy.deepcopy(other._placement)

	def setPlacement(self, placement):
		self._placement = copy.deepcopy(placement)

	def getPlacement(self):
		return self._placement

	def setVisibility(self, v):
		self._visibility.setValue(v)

	def keyPlacement(self, timeline):
		timeline.key('placement', self, self._placement)

	def keyVisibility(self, timeline):
		timeline.key('visibility', self, self._visibility)

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
				nodes.extend(l.distill())
		else:
			nodes = [node.Text(self.name, self)]

		return nodes
