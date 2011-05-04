import cwriting.core as core
import cwriting.node as node
import cwriting.curve as curve

import math

def makeRiseTween(d, obj, duration, real, diff=node.Placement(start=(0, -0.2, 0))):
	tl = core.Timeline(d.next())
	d.registerTimeline(tl)
	obj.setPlacement(real.moved(diff))
	obj.setVisibility(False)
	obj.keyPlacement(tl)
	obj.keyVisibility(tl)
	objTweenIn = core.CurveTweener()
	objTweenIn.setObject(obj, 'Placement', real)
	objTweenIn.setCurve(curve.quadOut3) 
	objTweenIn.tween(duration)
	d.registerTimeline(objTweenIn.getTimeline())
	tl.changeTimeline(objTweenIn.getTimeline())
	tl.advance(duration)
	obj.setVisibility(True)
	obj.keyVisibility(tl)
	return tl

def makeFallTween(d, obj, duration, real, diff=node.Placement(start=(0, -0.2, 0))):
	tl = core.Timeline(d.next())
	d.registerTimeline(tl)
	obj.setPlacement(real)
	obj.setVisibility(True)
	obj.keyPlacement(tl)
	obj.keyVisibility(tl)
	objTweenIn = core.CurveTweener()
	objTweenIn.setObject(obj, 'Placement', real.moved(diff))
	objTweenIn.setCurve(curve.quadIn3) 
	objTweenIn.tween(duration)
	d.registerTimeline(objTweenIn.getTimeline())
	tl.changeTimeline(objTweenIn.getTimeline())
	tl.advance(duration)
	obj.setVisibility(False)
	obj.keyVisibility(tl)
	return tl

def genScene0(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)
	
	tlBegin = core.Timeline('begin')
	d.registerTimeline(tlBegin)
	
	exnihilo = core.Text(d.next(), 'Ex Nihilo')
	exnihilo.setScale(3)
	exnihilo.setVisibility(False)
	exnihilo.setPlacement(node.Placement(start=(0, -2, -2)))
	d.registerObject(exnihilo)
	
	begin = core.Text(d.next(), 'begin')
	begin.setVisibility(False)
	begin.setPlacement(node.Placement(start=(0, -2, -3)))
	begin.link = node.Link()
	begin.link.addAction(node.TimerChange(tlBegin, 'start'))
	d.registerObject(begin)
	
	exnihilo.keyVisibility(tl0)
	exnihiloTweenIn = core.CurveTweener()
	exnihiloTweenIn.setObject(exnihilo, 'Placement', node.Placement(start=(0, 1, -2)))
	exnihiloTweenIn.setCurve(curve.quadOut3)
	exnihiloTweenIn.tween(3)
	d.registerTimeline(exnihiloTweenIn.getTimeline())
	tl0.changeTimeline(exnihiloTweenIn.getTimeline())
	
	tl0.advance(0.5)
	begin.keyVisibility(tl0)
	beginTweenIn = core.CurveTweener()
	beginTweenIn.setObject(begin, 'Placement', node.Placement(start=(0, 0, -2)))
	beginTweenIn.setCurve(curve.quadOut3)
	beginTweenIn.tween(2.5)
	d.registerTimeline(beginTweenIn.getTimeline())
	tl0.changeTimeline(beginTweenIn.getTimeline())
	
	tl0.advance(2.5)
	exnihilo.setVisibility(True)
	exnihilo.keyVisibility(tl0)
	exnihilo.keyVisibility(tlBegin)
	tl0.advance(0.5)
	begin.setVisibility(True)
	begin.keyVisibility(tl0)
	
	exnihilo.keyVisibility(tlBegin)
	exnihiloTweenOut = core.CurveTweener()
	exnihiloTweenOut.setObject(exnihilo, 'Placement', node.Placement(start=(0, 4, -2)))
	exnihiloTweenOut.setCurve(curve.quadIn3)
	exnihiloTweenOut.tween(2)
	d.registerTimeline(exnihiloTweenOut.getTimeline())
	tlBegin.changeTimeline(exnihiloTweenOut.getTimeline())
	
	
	tlBegin.advance(1)
	begin.keyVisibility(tlBegin)
	tlBegin.advance(1)
	exnihilo.setVisibility(False)
	exnihilo.keyVisibility(tlBegin)
	tlBegin.advance(1)
	begin.setVisibility(False)
	begin.keyVisibility(tlBegin)
	tlBegin.startScene('inTheBeginning')

	return 'begin', tl0

def genSceneInTheBeginning(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)

	tl0.advance(1)
	inTheBeginning = core.Text(d.next(), 'In the beginning')
	inTheBeginning.setPlacement(node.Placement(start=(0, 1, -2)))
	d.registerObject(inTheBeginning)

	inTheBeginningSound = node.Sound(d.next(), './res/01_l00.mp3')
	d.registerSound(inTheBeginningSound)

	tl0.playSound(inTheBeginningSound)
	inTheBeginning.keyVisibility(tl0)
	tl0.advance(0.05)
	inTheBeginning.setVisibility(True)
	inTheBeginning.keyVisibility(tl0)
	tl0.advance(1)

	thereWasNothing = core.Text(d.next(), 'there was nothing.')
	thereWasNothing.setPlacement(node.Placement(start=(0, 0.8, -2)))
	d.registerObject(thereWasNothing)
	thereWasNothing.keyVisibility(tl0)

	inTheBeginningTweenUp = core.CurveTweener()
	inTheBeginningTweenUp.setObject(inTheBeginning, 'Placement', node.Placement(start=(0, 1.2, -2)))
	inTheBeginningTweenUp.setCurve(curve.quadOut3) 
	inTheBeginningTweenUp.tween(1)
	d.registerTimeline(inTheBeginningTweenUp.getTimeline())
	tl0.changeTimeline(inTheBeginningTweenUp.getTimeline())

	tl0.advance(1)
	thereWasNothing.setVisibility(True)
	thereWasNothing.keyVisibility(tl0)

	tl0.advance(2)
	inTheBeginning.setVisibility(True)
	inTheBeginning.keyVisibility(tl0)
	thereWasNothing.setVisibility(True)
	thereWasNothing.keyVisibility(tl0)

	inTheBeginningTweenOut = core.CurveTweener()
	inTheBeginningTweenOut.setObject(inTheBeginning, 'Placement', node.Placement(start=(0, 1.2, -6)))
	inTheBeginningTweenOut.setCurve(curve.quadIn3) 
	inTheBeginningTweenOut.tween(2)
	d.registerTimeline(inTheBeginningTweenOut.getTimeline())
	tl0.changeTimeline(inTheBeginningTweenOut.getTimeline())

	thereWasNothingTweenOut = core.CurveTweener()
	thereWasNothingTweenOut.setObject(thereWasNothing, 'Placement', node.Placement(start=(0, 0.8, -6)))
	thereWasNothingTweenOut.setCurve(curve.quadIn3) 
	thereWasNothingTweenOut.tween(2)
	d.registerTimeline(thereWasNothingTweenOut.getTimeline())
	tl0.changeTimeline(thereWasNothingTweenOut.getTimeline())

	tl0.advance(2)
	inTheBeginning.setVisibility(False)
	inTheBeginning.keyVisibility(tl0)
	thereWasNothing.setVisibility(False)
	thereWasNothing.keyVisibility(tl0)
	
	fromNothing = core.Text(d.next(), "From nothing,\nthe world began")
	fromNothing.setPlacement(node.Placement(start=(0, 1.2, -2)))
	fromNothing.breakApart()
	d.registerObject(fromNothing)

	fromNothingSound = node.Sound(d.next(), './res/01_l01.mp3')
	d.registerSound(fromNothingSound)

	fromNothingTweensIn = fromNothing.createTweenSet('Visibility', (lambda t: node.Boolean('Visibility', True)), (lambda t: curve.floor1))
	fromNothingTweensIn.register(d)
	fromNothingTweensIn.setLazyKeying(True)
	tlFromNothingIn = fromNothingTweensIn.tweenAcross(0.1, 1.5)
	d.registerTimeline(tlFromNothingIn)
	tl0.changeTimeline(tlFromNothingIn)
	tl0.playSound(fromNothingSound)

	tl0.advance(5)
	fromNothingTweensOut1 = fromNothing.createTweenSetBackwards('Visibility', (lambda t: node.Boolean('Visibility', False)), (lambda t: curve.floor1))
	fromNothingTweensOut1.register(d)
	fromNothingTweensOut1.setLazyKeying(True)
	tlFromNothingOut1 = fromNothingTweensOut1.tweenAcross(0.1, 1)
	d.registerTimeline(tlFromNothingOut1)
	tl0.changeTimeline(tlFromNothingOut1)
	fromNothingTweensOut2 = fromNothing.createTweenSetBackwards('Placement', (lambda t: t.getPlacement().moved(node.Placement(start=(0, -2, 0)))), (lambda t: curve.quadIn3))
	fromNothingTweensOut2.register(d)
	tlFromNothingOut2 = fromNothingTweensOut2.tweenAcross(0.1, 2)
	d.registerTimeline(tlFromNothingOut2)
	tl0.changeTimeline(tlFromNothingOut2)
	tl0.advance(4)
	tl0.startScene('rain')

	return 'inTheBeginning', tl0

def genSceneRain(d):
	def waves(n):
		return (lambda s, t: 0.2*math.sin(n)*(math.sin(2.5*s+n) + math.sin(2.5*t+n)) + (t-1)*(t-1)*0.1 + n/3.5 - 3.0)

	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)

	sceneText = core.Text(d.next(), 'First, the rains rained and the\n'
	                                'seas filled. An almost endless\n'
	                                'deluge filled the yawning void\n'
	                                'that had preceded the oceans.')

	sceneText2 = core.Text(d.next(), 'Slowly, the rains ceased and\n'
	                                 'the water stopped rising.\n'
	                                 '\n'
	                                 'The rain was done.')

	sceneText.setPlacement(node.Placement(start=(0, 2.0, -2)))
	d.registerObject(sceneText)
	sceneText.keyPlacement(tl0)
	sceneText.keyVisibility(tl0)
	sceneText2.setPlacement(node.Placement(start=(0, 0.5, -2)))
	d.registerObject(sceneText2)
	sceneText2.keyPlacement(tl0)
	sceneText2.keyVisibility(tl0)

	sceneSound = node.Sound(d.next(), './res/02_l00.mp3')
	sceneSound2 = node.Sound(d.next(), './res/02_l01.mp3')
	d.registerSound(sceneSound)
	d.registerSound(sceneSound2)

	s = []
	text = 'the rains fell, the seas filled, '
	for y in range(12):
		for x in range(20):
			s.append(text[(x + 4*y) % len(text)])
		s.append('\n')
	s = ''.join(s)
	theRains = core.Text(d.next(), s)
	theRains.setScale(2.1)
	# XXX HACK ATTACK
	theRains.breakApart(lambda s, t: node.Placement(start=(s*.4, 0, t*.7 - 5)))
	theRainsG = theRains.getGroup()
	theRainsG.applyMap(curve.HeightMap(None, 2, waves(0)))
	d.registerObject(theRains)

	theRainsP = core.Text(d.next(), 'the rains')
	theRainsPGroup = core.Group('rains')
	theRainsPGroup.addObject(theRainsP)
	theRainsPSystem = core.ParticleSystem(d.next())
	theRainsPSystem.speed = 0.3
	theRainsPActions = node.ParticleActionList(d.next())
	theRainsPSystem.actions = theRainsPActions
	theRainsPActions.setRate(2)
	theRainsPGravity = node.Gravity()
	theRainsPGravity.setDirection((-0.2, -0.5, 0))
	theRainsPActions.addAction(theRainsPGravity)
	theRainsPSystem.particles = theRainsPGroup
	theRainsPSource = node.Disc()
	theRainsPSource.setCenter((0, 8, 0))
	theRainsPSource.setNormal((0.2, -1.0, 0))
	theRainsPVel = node.Box()
	theRainsPVel.setP1((-1, -4, 0))
	theRainsPVel.setP2((2, -2, -2))
	theRainsPActions.setSource(theRainsPSource)
	theRainsPActions.setVel(theRainsPVel)
	theRainsPActions.setRemoveCondition(node.Age(6))
	d.registerObject(theRainsP)
	d.registerObject(theRainsPSystem)
	d.registerGroup(theRainsPGroup)
	d.registerParticleActions(theRainsPSystem.actions)

	tlWaves = core.Timeline('waves')
	d.registerTimeline(tlWaves)
	for t in range(72):
		if t:
			tlWaves.advance(1/4.0)
		theRainsG.applyMap(curve.HeightMap(None, 2, waves(t*2.0/15.0*math.pi)))
		theRainsG.key('Placement', tlWaves)
		if t == 64:
			theRainsG.set('Visibility', True)
			theRainsG.key('Visibility', tlWaves)
	theRainsG.set('Visibility', False)
	theRainsG.key('Visibility', tlWaves)
	tlWaves.advance(0.01)
	#tlWaves.freeze(True)

	tl0.changeTimeline(tlWaves)
	theRainsG.key('Visibility', tl0)
	theRainsPSystem.key('Visibility', tl0)

	sceneTextTweenIn = core.CurveTweener()
	sceneTextTweenIn.setObject(sceneText, 'Placement', node.Placement(start=(0, 2.2, -2)))
	sceneTextTweenIn.setCurve(curve.quadOut3) 
	sceneTextTweenIn.tween(1)
	d.registerTimeline(sceneTextTweenIn.getTimeline())
	tl0.changeTimeline(sceneTextTweenIn.getTimeline())
	tl0.playSound(sceneSound)

	tl0.advance(1)
	theRainsG.set('Visibility', True)
	theRainsG.key('Visibility', tl0)
	theRainsPSystem.set('Visibility', True)
	theRainsPSystem.key('Visibility', tl0)
	sceneText.setVisibility(True)
	sceneText.keyVisibility(tl0)

	tl0.advance(15)
	tl0.playSound(sceneSound2)
	sceneText2.keyPlacement(tl0)
	sceneText2.keyVisibility(tl0)
	sceneText2TweenIn = core.CurveTweener()
	sceneText2TweenIn.setObject(sceneText2, 'Placement', node.Placement(start=(0, 0.7, -2)))
	sceneText2TweenIn.setCurve(curve.quadOut3) 
	sceneText2TweenIn.tween(1)
	d.registerTimeline(sceneText2TweenIn.getTimeline())
	tl0.changeTimeline(sceneText2TweenIn.getTimeline())
	theRainsPSystem.key('Visibility', tl0)
	tl0.advance(1)
	sceneText2.setVisibility(True)
	sceneText2.keyVisibility(tl0)
	tl0.advance(2)
	theRainsPSystem.set('Visibility', False)
	theRainsPSystem.key('Visibility', tl0)

	tl0.advance(5)
	tl0.changeTimeline(makeFallTween(d, sceneText, 1, node.Placement(start=(0, 2.2, -2))))
	tl0.changeTimeline(makeFallTween(d, sceneText2, 1, node.Placement(start=(0, 0.7, -2))))
	tl0.advance(1)
	tl0.startScene('lands')

	return 'rain', tl0

def genSceneLands(d):
	tl0 = core.Timeline(d.next())
	d.registerTimeline(tl0)

	sceneText = core.Text(d.next(), 'But the oceans were unending.')
	sceneText2 = core.Text(d.next(), 'From beneath the infinite oceans\n'
	                                 'rose the lands. Solid stone jutted\n'
	                                 'out. The mountains towered, and\n'
	                                 'slowly the land emerged from the\n'
	                                 'ocean. There was a terminus\n'
	                                 'setting apart the seas.')

	sceneText.setPlacement(node.Placement(start=(0, 2.4, -2)))
	sceneText2.setPlacement(node.Placement(start=(0, 1.1, -2)))
	d.registerObject(sceneText)
	d.registerObject(sceneText2)

	sceneSound = node.Sound(d.next(), './res/03_l00.mp3')
	sceneSound2 = node.Sound(d.next(), './res/03_l01.mp3')
	d.registerSound(sceneSound)
	d.registerSound(sceneSound2)

	waterText = core.Text(d.next(), 'Into the horizon, into the eternity, the\n'
	                                'waters spread forever. North, south, east,\n'
	                                'and west: in all directions, the waters\n'
	                                'were all that could be seen, for the waters\n'
	                                'were all there was. Above the waters, the\n'
	                                'skies looked down upon her brother and saw\n'
	                                'the loneliness of his expanse. She knew\n'
	                                'something was missing, and she knew that\n'
	                                'there was more to come. There must be no\n'
	                                'infinite; there must be bounds, they must\n'
	                                'just be found. After the rains, the waters\n'
	                                'were calm. But this too must not last, for\n'
	                                'the bleak emptiness of the unending filled\n'
	                                'the waters. This pure boredom of the waters,\n'
	                                'with no waves and no motion, must be ended\n'
	                                'somehow. The end has yet to be seen, but\n'
	                                'there must be an end. There must be an end.\n'
	                                'Where is the end? The end must be found. The\n'
	                                'skies and the seas must make this end. There\n'
	                                'will be a terminus. There must be an end.')
	waterText.setScale(2)
	waterText.valign = 'bottom'
	waterText.setPlacement(node.Placement(start=(0, -3, 0), rotation=node.AxisRotation(axis=(1, 0, 0), rotation=-90)))
	d.registerObject(waterText)
	waterText.keyVisibility(tl0)

	tl0.changeTimeline(makeRiseTween(d, sceneText, 1, node.Placement(start=(0, 2.6, -2))))
	tl0.playSound(sceneSound)
	tl0.advance(1)

	waterText.setVisibility(True)
	waterText.keyVisibility(tl0)
	tl0.advance(2)

	mountain01 = core.Text(d.next(), 'The mountains rose from beneath the seas, filling the space around them. And here did the oceans part.'.replace(' ', '\n'))
	mountain01.halign = 'right'
	mountain01.setScale(2)
	mountain01.setPlacement(node.Placement(start=(-5, -4, -5), rotation=node.LookAt(target=(-2, -2.8, -4.5), up=(0, 0, -1))))
	d.registerObject(mountain01)
	mountain01.keyVisibility(tl0)
	mountain01.keyPlacement(tl0)


	mountain02 = core.Text(d.next(), 'No longer whole, the seas were sundered by cliffs and beaches. And beyond these shores lay more still.'.replace(' ', '\n'))
	mountain02.halign = 'left'
	mountain02.setScale(2)
	mountain02.setPlacement(node.Placement(start=(5, -4, -5), rotation=node.LookAt(target=(2, -2.8, -4.5), up=(0, 0, -1))))
	d.registerObject(mountain02)
	mountain02.keyVisibility(tl0)
	mountain02.keyPlacement(tl0)

	mountain01TweenIn = core.CurveTweener()
	mountain01TweenIn.setObject(mountain01, 'Placement', mountain01.getPlacement().moved(node.Placement(start=(-0.2, 1, 0), rotation=node.LookAt(up=(0, 0, -1)))))
	mountain01TweenIn.setCurve(curve.quadOut3)
	mountain01TweenIn.tween(2)
	d.registerTimeline(mountain01TweenIn.getTimeline())
	tl0.changeTimeline(mountain01TweenIn.getTimeline())

	mountain02TweenIn = core.CurveTweener()
	mountain02TweenIn.setObject(mountain02, 'Placement', mountain02.getPlacement().moved(node.Placement(start=(0.2, 1, 0), rotation=node.LookAt(up=(0, 0, -1)))))
	mountain02TweenIn.setCurve(curve.quadOut3)
	mountain02TweenIn.tween(2)
	d.registerTimeline(mountain02TweenIn.getTimeline())
	tl0.changeTimeline(mountain02TweenIn.getTimeline())

	tl0.advance(1)

	mountain01.setVisibility(True)
	mountain01.keyVisibility(tl0)
	mountain02.setVisibility(True)
	mountain02.keyVisibility(tl0)

	tl0.playSound(sceneSound2)
	tl0.changeTimeline(makeRiseTween(d, sceneText2, 1, node.Placement(start=(0, 1.3, -2))))
	tl0.advance(2)

	return 'lands', tl0

d = core.Document()

d.addScene(genScene0(d), True)
d.addScene(genSceneInTheBeginning(d))
d.addScene(genSceneRain(d))
d.addScene(genSceneLands(d))

d.save('exnihilo.xml')
