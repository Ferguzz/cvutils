import cv

def check(im):
	"""Checks whether we have an IplImage of a cvMat by attempting 
	to access im.depth.  If im is a cvMat this raises an AttributeError."""
	try:
		im.depth
		return 'ipl'
	except AttributeError:
		return 'mat'

def zoom(im, level):
	pass

def rotate(im, angle):
	"""Rotates image by angle degrees clockwise."""
	centre = ((im.width-1)/2.0, (im.height-1)/2.0)
	rot = cv.CreateMat(2, 3, cv.CV_32FC1)
	cv.GetRotationMatrix2D(centre, -angle, 1.0, rot)
	if check(im) == 'mat':
		dst = cv.CloneMat(im)
	else:
		dst = cv.CloneImage(im)
	cv.WarpAffine(im, dst, rot)
	return dst
	
def contrast(im, value):
	pass

def normalise(im):
	pass

def resize(im, size):
	pass

def blackandwhite(im):
	pass

def saltandpepper(im, level):
	pass

def gaussiannoise(im, level):
	pass

numbered_title = 1
def show(im, title = 'none'):
	if title == 'none':
		global numbered_title
		title = numbered_title
		numbered_title += 1
	cv.NamedWindow(str(title))
	cv.ShowImage(str(title), im)

def wait():
	print 'Press any key to quit...'
	cv.WaitKey(0)
