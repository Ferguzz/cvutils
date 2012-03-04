import cv, warnings, inspect, re

def clone(im):
	"""Modified clone function which checks whether we have an IplImage 
	or a cvMat by attempting to access im.depth.  If im is a cvMat this 
	raises an AttributeError and cv.CloneMat is called instead of cv.CloneImage"""
	try:
		im.depth
		return cv.CloneImage(im)
	except AttributeError:
		return cv.CloneMat(im)
		
def create(im):
	"""Function which creates an empty IplImage or CvMat the same size
	and type as the input image."""
	try:
		return cv.CreateImage(cv.GetSize(im), im.depth, im.channels)
	except AttributeError:
		return cv.CreateMat(im.height, im.width, im.type)
		
def zoom(im, level, centre = 'middle'):
	"""Simple zoom function.  Issues warning if zoom level is less than 1.
	If centre point is too close to an edge it is moved just far enough inside."""
	if level < 1:
		warnings.warn('Cannot have zoom level less than 1.')
		return im	
	if centre == 'middle':
		centre = ((im.width-1)/2, (im.height-1)/2)
	width = int(im.width/(2.0*level))
	height = int(im.height/(2.0*level))	
	
	if centre[0] + width >= im.width:
		centre = (im.width-1-width, centre[1])
	elif centre[0] - width < 0:
		centre = (width, centre[1])		
	if centre[1] + height >= im.height:
		centre = (centre[0], im.height-1-height)		
	elif centre[1] - height < 0:
		centre = (centre[0], height)
	
	rect = (centre[0]-width, centre[1]-height, width*2, height*2)
	dst = cv.GetSubRect(im, rect)
	size = create(im)
	cv.Resize(dst, size)
	return size

def rotate(im, angle):
	"""Rotates image by 'angle' degrees clockwise."""
	centre = ((im.width-1)/2.0, (im.height-1)/2.0)
	rot = cv.CreateMat(2, 3, cv.CV_32FC1)
	cv.GetRotationMatrix2D(centre, -angle, 1.0, rot)
	dst = create(im)
	cv.WarpAffine(im, dst, rot)
	return dst
	
def contrast(im, value):
	pass

def normalise(im):
	pass

def resize(im, size):
	pass

def blackandwhite(im):
	"""Converts RGB input to black and white."""
	try:
		dst = cv.CreateImage(cv.GetSize(im), im.depth, 1)
	except AttributeError:
		dst = cv.CreateMat(im.height, im.width, im.type & 7)
		
	cv.CvtColor(im, dst, cv.CV_BGR2GRAY)
	return dst

def saltandpepper(im, level):
	pass

def gaussiannoise(im, level):
	pass

def show(im, title = 'none'):
	if title == 'none':
		frame = inspect.currentframe()
		try:
			context = inspect.getframeinfo(frame.f_back).code_context
			caller_lines = ''.join([line.strip() for line in context])
			m = re.search(r'show\s*\((.+?)\)$', caller_lines)
			if m:
				title = m.group(1)
		finally:
			del frame
		
	cv.NamedWindow(title)
	cv.ShowImage(title, im)

def wait():
	print 'Press any key to quit...'
	cv.WaitKey(0)
