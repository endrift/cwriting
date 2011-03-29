import cwriting.core as core
import cwriting.node as node

def generateButton(doc, text):
	text.setVisibility(False)

	tl_pre = core.Timeline(text.name + '_pre', True)
	doc.registerTimeline(tl_pre)
	
	tl_post = core.Timeline(text.name + '_post')
	doc.registerTimeline(tl_post)
	
	text.link = node.Link()
	text.link.addAction(node.TimerChange(tl_post, 'start'))
	doc.registerObject(text)
	
	text.keyVisibility(tl_pre)
	text.keyPlacement(tl_pre)
	tl_pre.advance(0.5)
	
	text.setVisibility(True)
	text.getPlacement().move(node.Placement(start=(0, 0.2, 0)))
	
	text.keyVisibility(tl_pre)
	text.keyPlacement(tl_pre)
	text.keyVisibility(tl_post)
	text.keyPlacement(tl_post)
	tl_post.advance(0.5)
	
	text.setVisibility(False)
	text.getPlacement().move(node.Placement(start=(0, -0.2, 0)))
	text.keyVisibility(tl_post)
	text.keyPlacement(tl_post)

if __name__ == '__main__':
	d = core.Document()
	t = core.Text('nihilo', "In the beginning,\nthere was nothing")
	
	generateButton(d, t)

	d.save('button.xml')
