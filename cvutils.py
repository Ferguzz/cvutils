import cv, warnings, inspect, re, random

def sample(im, size = (16,16), pos = 'random'):
	"""
	Returns a rectangluar sample from an image.
	
	**Parameters:** 
		* im (cvArr) - The source image.
		* size (tuple) - The width and height of the sample rectange (width, height).
		* pos (tuple) - The coordinates of the top-left corner of the sample (x, y).  If corner is too close to an edge it is moved just far enough inside.
	"""
	if pos == 'random':
		random.seed()
		pos = (random.randint(0, im.width-1-size[0]), random.randint(0, im.height-1-size[1]))
	else:
		if pos[0] + size[0] >= im.width:
			pos = (im.width-1-size[0], pos[1])
		if pos[1] + size[1] >= im.height:
			pos = (pos[0], im.height-1-size[1])
	return cv.GetSubRect(im, pos + size)

def clone(im):
	"""Modified clone function which checks whether we have an IplImage 
	or a cvMat by attempting to access im.depth.  If im is a cvMat this 
	raises an AttributeError and cv.CloneMat is called instead of cv.CloneImage"""
	try:
		im.depth
		return cv.CloneImage(im)
	except AttributeError:
		return cv.CloneMat(im)
		
def create(im, onechannel = False):
	"""Function which creates an empty IplImage or CvMat the same size
	and type as the input image.  A single channel version is produced is onechannel is True"""
	try:
		im.depth
		if onechannel:
			channels = 1
		else:
			channels = im.channels
		return cv.CreateImage(cv.GetSize(im), im.depth, channels)
	except AttributeError:
		if onechannel:
			mask = 24
		else: 
			mask = 0
		return cv.CreateMat(im.height, im.width, im.type & ~mask)
		
def zoom(im, level, centre = 'middle'):
	"""
	Returns a zoomed version of the image.
	Parameters: im (cvArr) - The source image.
				level (float) - Zoom level (warning is raised if this is below one and no zoom occurs).
				centre (tuple) - Zoom centre (x, y).  If centre point is too close to an edge it is moved just far enough inside.
	"""
	if level < 1:
		warnings.warn('Cannot have zoom level less than 1.', stacklevel=2)
		return im
		
	width = int(im.width/(2.0*level))
	height = int(im.height/(2.0*level))	
	
	if centre == 'middle':
		centre = ((im.width-1)/2, (im.height-1)/2)
		
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
	dst = create(im)
	cv.ConvertScale(im, dst, value)
	return dst

def brightness(im, value):
	dst = create(im)
	cv.ConvertScale(im, dst, shift = value)
	return dst

def normalise(im):
	pass

def resize(im, size):
	pass

def blackandwhite(im):
	"""Converts RGB input to black and white."""
	dst = create(im, onechannel = True)		
	cv.CvtColor(im, dst, cv.CV_BGR2GRAY)
	return dst

def saltandpepper(im, level, nowarning = False):
	if not (0 < level <= 0.1) and nowarning == False:
		warnings.warn("This is a lot of salt and pepper noise.  I would suggest somewhere up to 0.1.  Use 'nowarning = True' to suppress this warning.", stacklevel=2)
		
	if im.channels == 3:
		white = (255,255,255)
		black = (0,0,0)
	else:
		white = 255
		black = 0
		
	random.seed()
	size = im.width*im.height
	r = range(size)
	random.shuffle(r)
	noise_pixels = r[:min(int(level*size), size)]
	dst = clone(im)
	for pix in noise_pixels:
		x = (pix/im.width) - 1
		y = pix%(im.width) - 1
		if random.random() > 0.5:
			dst[x,y] = white
		else:
			dst[x,y] = black
	return dst
		
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
