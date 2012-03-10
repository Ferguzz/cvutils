import cv, warnings, inspect, re, random, array

def sample(im, size = (16,16), pos = 'random'):
	"""
	Gets a rectangluar sample from an image.  If pos is too close to an edge it is moved just far enough inside to get the full sample size.
	
	**Parameters:** 
		* im (cvArr) - The source image.
		* size (tuple) - The width and height of the sample rectange (width, height).
		* pos (tuple) - The coordinates of the top-left corner of the sample (x, y).
	**Returns:**
		The image sample.
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
	"""
	Clones the image.  The function checks whether we have an IplImage 
	or a cvMat and returns the same type.
	
	**Parameters:**
	 	* im (cvArr) - The source image.
	
	**Returns:**
		The cloned image.
	"""
	try:
		im.depth
		return cv.CloneImage(im)
	except AttributeError:
		return cv.CloneMat(im)
		
def create(im, onechannel = False):
	"""
	Creates an empty image the same type and size as the input image.  A single channel version is produced is onechannel = True
	
	**Parameters:**
		* im (cvArr) - The source image.
		* onechannel (bool) - Create a single channel image.
	
	**Returns:**
		An empty image.
	"""
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
	Returns a zoomed version of the image.  If centre point is too close to an edge it is moved just far enough inside to get the required zoom level.  A warning is raised if level is below 1 and no zoom occurs.  
	
	**Parameters:**
		* im (cvArr) - The source image.
		* level (float) - Zoom level.
		* centre (tuple) - Zoom centre (x, y).
	
	**Returns:**
		The zoomed image.
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
	"""
	Rotates image by angle degrees clockwise.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* angle (float) - Angle in degrees.
	
	**Returns:**
		The rotated image.
	"""
	# TODO: arguments to specifcy background colour and clockwise/anti-clockwise.
	centre = ((im.width-1)/2.0, (im.height-1)/2.0)
	rot = cv.CreateMat(2, 3, cv.CV_32FC1)
	cv.GetRotationMatrix2D(centre, -angle, 1.0, rot)
	dst = create(im)
	cv.WarpAffine(im, dst, rot)
	return dst
	
# Should these functions be merged?
def contrast(im, value):
	"""
	Changes the contrast of the image.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* value (float) - The contrast level.
	
	**Returns:**
		The image with changed contrast.
	"""
	dst = create(im)
	cv.ConvertScale(im, dst, value)
	return dst

def brightness(im, value):
	"""
	Changes the brightness of the image.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* value (float) - The brightness level.
		
	**Returns:**
		The image with changed brightness.
	"""	
	dst = create(im)
	cv.ConvertScale(im, dst, shift = value)
	return dst

def normalise(im):
	"""Need to write docstring"""
	pass

def resize(im, size):
	"""Need to write docstring"""
	pass

def blackandwhite(im):
	"""
	Converts RGB input to black and white.
	
	**Parameters:**
		* im (cvArr) - The source image.
	
	**Returns:**
		The black and white image.
	"""
	dst = create(im, onechannel = True)		
	cv.CvtColor(im, dst, cv.CV_BGR2GRAY)
	return dst

def saltandpepper(im, level, nowarning = False):
	"""Applies salt and pepper to the image.  If the amount of noise if above 10\% a warning is raised.  This can be turned off by setting nowarning = True.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* level (float) - The amount of noise between 0 and 1.  e.g. 0.05 = 5\%
		* nowarning (bool) - Suppress warning message.
	
	**Returns:**
		The noisy image.
	"""
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
		
def gaussiannoise(im, mean = 0.0, std = 15.0):
	"""
	Applies Gaussian noise to the image.  This models sensor noise found in cheap cameras in low light etc.  **Note:** This function takes a while to run (>1s).
	
	**Parameters:**
		* im - (cvArr) - The source image.
		* mean (float) - The mean value of the Gaussian distribution.
		* std (float) - The standard deviation of the Gaussian distribution.  Larger standard deviation means more noise.
		
	**Returns:**
		The noisy image.
	"""
	# The first version below takes around 0.4s less time to run on my computer than the version beneath it.
	# But I still don't like it...
	# Want to change this to make it quicker still and nicer to read.
	# Numpy would make this really quick but don't want it be a dependancy.
	# Also it's tricky to add the blue amplification using this method.
	dst = create(im)
	if im.channels == 3:
		data = array.array('d', [random.gauss(mean, std) for i in xrange(im.width*im.height*3)])
		noise = cv.CreateMatHeader(im.height, im.width, cv.CV_64FC3)
		cv.SetData(noise, data, cv.CV_AUTOSTEP)
	else:
		data = array.array('d', [random.gauss(mean, std) for i in xrange(im.width*im.height)])
		noise = cv.CreateMatHeader(im.height, im.width, cv.CV_64FC1)
		cv.SetData(noise, data, cv.CV_AUTOSTEP)
	cv.Add(im, noise, dst)
	return dst
	
	# # TODO: argument for blue amplification?
	# blue_amplification_value = 1.0
	# dst = create(im)
	# random.seed()	
	# for row in range(im.height):
	# 	for col in range(im.width):
	# 		pix = im[row, col]
	# 		if im.channels == 3:
	# 			dst[row, col] = (pix[0]+random.gauss(mean, std), pix[1]+random.gauss(mean, std), pix[2]+(blue_amplification_value*random.gauss(mean, std)))
	# 		else:
	# 			dst[row, col] = pix+random.gauss(mean, std)
	# return dst

def show(im, title = 'none'):
	"""
	Opens a window and displays the image.  If no title is provided the title of the window will default to the first argument.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* title (string) - The title of the window.
	"""
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
	"""
	Causes the program to wait at this point until a key is pressed.
	"""
	print 'Press any key to continue...'
	cv.WaitKey(0)
