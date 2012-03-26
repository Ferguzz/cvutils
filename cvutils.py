"""
Some handy helper functions for writing OpenCV programs in no time!

The idea with this module is that most functions can be used with very few or zero additional arguments.  e.g. if you call :func:`sample()` with just the image as an argument it takes a 16x16 pixel sample from a random point in the image.  However if you want a bit more control you can specify a rectangluar size and a coordinate, as well as tell it to place a white rectangle around the sample on the original image.  Similarly, calling :func:`show()` with just the image creates a :class:`cv.NamedWindow` with the variable name of the image and calles :func:`cv.ShowImage()`.  Again, an optional window title can be passed if required.  I know that is pretty lazy, but it can really speed up your workflow if you are regularly just checking the outputs of CV functions.  
"""

# Note:  I could do with using Numpy for a couple of functions but I didn't want to include external dependancies in this module.  However I think Numpy might be an OpenCV prerequisite anyway for Python, so if this is the case then why not!

import cv, warnings, inspect, re, random, array, math

def sample(im, size = (16,16), pos = 'random', show_on_original = False, return_pos = False):
	"""
	Gets a rectangluar sample from an image.  If pos is too close to an edge it is moved just far enough inside so the full sample size is always returned.
	
	**Parameters:** 
		* im (cvArr) - The source image.
		* size (tuple) - The width and height of the sample rectange (width, height).
		* pos (tuple) - The coordinates of the top-left corner of the sample (x, y).
		* show_on_original (bool) - Place a white rectangle around the sample on the original image.
		* return_pos (bool) - Return the randomly generated position coordinate as well.
		
	**Returns:**
		The image sample, top-left coordinate of the sample (optional).
	
	.. warning::
		Think I spotted a problem here that when the sample is really large, the position can become negative.  This maybe applies to :func:`crop()` too.
	
	.. seealso::
		:func:`crop()`
	"""	
	if pos == 'random':
		random.seed()
		pos = (random.randint(0, im.width-1-size[0]), random.randint(0, im.height-1-size[1]))
	else:
		# Think I spotted a problem here when the sample is really large, the position can become negative.  This probably applies to crop() too.
		if pos[0] + size[0] > im.width:
			pos = (im.width-1-size[0], pos[1])
		if pos[1] + size[1] > im.height:
			pos = (pos[0], im.height-1-size[1])
	sample = cv.GetSubRect(im, pos + size)
	if show_on_original == True:
		if im.channels == 3:
			colour = (255,255,255)
		else:
			colour = 255
		cv.Rectangle(im, (pos[0]-1, pos[1]-1), (pos[0]+size[0], pos[1]+size[1]), colour, 1)
	if return_pos == True:
		return sample, pos
	return sample


def crop(im, size, pos = (0,0)):
	"""
	This function is very similar to :func:`sample()` in that it returns a specified subsection of the image.  The main difference here is that if the region is too big to fit, the returned image is made smaller.  There is no size default here and pos defaults to the top-left corner of the image.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* size (tuple) - The cropped image size (w, h).
		* pos (tuple) - The position of the top-left corner of the cropped image.
	
	**Returns:**
		The cropped image.
	
	.. seealso::
		:func:`sample()`
	"""
	warn = False
	if pos[0] + size[0] > im.width:
		size = (im.width-1-pos[0], size[1])
		warn = True
	if pos[1] + size[1] > im.height:
		size = (size[0], im.height-1-pos[1])
		warn = True
	if warn:
		warnings.warn("Cropped region went off the edge of the image.  The cropped size has been reduced to %dx%d." %(size[0], size[1]), stacklevel=2)

	rect = (pos[0], pos[1], size[0], size[1])
	cropped = create(im, size = size)
	dst = cv.GetSubRect(im, rect)
	cv.Resize(dst, cropped)
	return cropped

def clone(im):
	"""
	Clones the image.  The function checks whether we have an IplImage 
	or a cvMat and returns the same type.
	
	**Parameters:**
	 	* im (cvArr) - The source image.
	
	**Returns:**
		The cloned image.
	
	.. seealso::
		:func:`create()`
	"""
	try:
		im.depth
		return cv.CloneImage(im)
	except AttributeError:
		return cv.CloneMat(im)
		
def create(im, onechannel = False, size = 'same'):
	"""
	Creates an empty image the same type and size as the input image.  A single channel version is produced if ``onechannel = True``.  Size can also be specified with size parameter.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* onechannel (bool) - Create a single channel image.
		* size (tuple) - Size of the image (w, h).
	
	**Returns:**
		An empty image.
		
	.. seealso::
		:func:`clone()`
	"""
	try:
		im.depth
		if size == 'same':
			width = im.width
			height = im.height
		else:
			width = size[0]
			height = size[1]
		if onechannel:
			channels = 1
		else:
			channels = im.channels
		return cv.CreateImage((width, height), im.depth, channels)
	except AttributeError:
		if size == 'same':
			width = im.width
			height = im.height
		else:
			width = size[0]
			height = size[1]
		if onechannel:
			mask = 24
		else: 
			mask = 0
		return cv.CreateMat(height, width, im.type & ~mask)
		
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
		
	if centre[0] + width > im.width:
		centre = (im.width-1-width, centre[1])
	elif centre[0] - width < 0:
		centre = (width, centre[1])
	if centre[1] + height > im.height:
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
	
	.. todo::
		* Arguments to specifcy background colour and clockwise/anti-clockwise.
		* Enclosed rectangle formula.
	"""
	centre = ((im.width-1)/2, (im.height-1)/2)
	rot = cv.CreateMat(2, 3, cv.CV_32FC1)
	cv.GetRotationMatrix2D(centre, -angle, 1.0, rot)
	dst = create(im)
	cv.WarpAffine(im, dst, rot)
	
	# Code in progress to return the new rectangle contained in the rotated image
	
	# w = float(im.width)
	# 	h = float(im.height)
	# 	angle = (angle/360.0)*2*math.pi
	# 	width = w/(math.sin(angle)*(h/w + (math.cos(angle)/math.sin(angle))))
	# 	height = (w/h)*width
	# pt1 = (centre[0]-int(width/2), centre[1]-int(height/2))
	# pt2 = (centre[0]+int(width/2)-1, centre[1]+int(height/2)-1)
	# cv.Rectangle(dst, pt1, pt2, 255)
	return dst
	
def contrast(im, value):
	"""
	Changes the contrast of the image.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* value (float) - The contrast level.
	
	**Returns:**
		The image with changed contrast.
	
	.. todo::
		Should this function be merged with :func:`brightness()`?		
	
	.. seealso::
		:func:`brightness()`
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
	
	.. todo::
		Should this function be merged with :func:`contrast()`?
	
	.. seealso::
		:func:`contrast()`
	"""	
	dst = create(im)
	cv.ConvertScale(im, dst, shift = value)
	return dst

def normalise(im):
	"""
	Normalise image histogram.
	"""
	pass

def resize(im, size):
	"""
	Resizes the image.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* size (tuple) - The size of the new image.
	
	**Returns:**
		The resized image.
	"""
	dst = create(im, size = size)
	cv.Resize(im, dst)
	return dst

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
	"""Applies salt and pepper noise to the image.  If the amount of noise if above 10\% a warning is raised.  This can be turned off by setting ``nowarning = True``.
	
	**Parameters:**
		* im (cvArr) - The source image.
		* level (float) - The amount of noise between 0 and 1.  e.g. 0.05 = 5\%
		* nowarning (bool) - Suppress warning message.
	
	**Returns:**
		The noisy image.

	.. seealso::
		:func:`gaussiannoise()`

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
	Applies Gaussian noise to the image.  This models sensor noise found in cheap cameras in low light etc.
	
	**Parameters:**
		* im - (cvArr) - The source image.
		* mean (float) - The mean value of the Gaussian distribution.
		* std (float) - The standard deviation of the Gaussian distribution.  Larger standard deviation means more noise.
		
	**Returns:**
		The noisy image.
		
	.. note::
		This function takes a while to run on large images.
		
	.. todo::
		* Argument for blue amplification to model bad sensors?
		* Use numpy to speed things up?
	
	.. seealso::
		:func:`saltandpepper()`
	"""
	# The first version below takes around 0.4s less time to run on my computer than the version beneath it on a colour image that is about 600x800.
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

def wait(key = None):
	"""
	Causes the program to wait at this point until a key is pressed.
	"""
	print 'Press any key to continue...'
	cv.WaitKey(0)
	
def overlay(im, overlay, pos = (0,0), blend = 1, nowarning = False):
	"""
	Overlays an image with a specified blend ratio.  If the overlay image is too big to fit at the specified position, it is cropped down to size and a warning is raised.  This can be turned off by setting ``nowarning = True``.
	
	**Parameters:**
		* im (cvArr) - The source image,
		* overlay (cvArr) - The image to be overlayed.
		* pos (tuple) - The position in the image to place the top-left corner of the overlay image.
		* blend (float)/(string) - The blend ratio.  If blend is 1, the overlay image is fully opaque, if blend is 0, the overlay image is invisible.  Between 1 and 0 is transparent.  If blend = 'both', both images are added as they are, this turns any black in the overlay region to become fully transparent.
		* nowarning (bool) - Suppress warning message.
	
	**Returns:**
		* The source image with overlay image added.
	"""
	size = (overlay.width, overlay.height)
	# Should I move the coordinate inside as with zoom() and sample() or crop the overlay image?  I think cropping might be the best way to go here.
	warn = False
	if pos[0] + size[0] > im.width:
		size = (im.width-1-pos[0], size[1])
		warn = True
	if pos[1] + size[1] > im.height:
		size = (size[1], im.height-1-pos[1])
		warn = True
	if warn:
		overlay = crop(overlay, size)
		if nowarning == False:
			warnings.warn("The overlay image was too big to fit at the position specified.  It has been cropped to %dx%d.  Use 'nowarning = True' to suppress this warning." %(size[0], size[1]), stacklevel=2)

	cv.SetImageROI(im, pos + size)
	if blend == 'both':
		alpha = 1
		blend = 1
	else:
		alpha = 1-blend
	cv.AddWeighted(im, alpha, overlay, blend, 0, im)
	cv.ResetImageROI(im)
	return im
		
class webcam:
	"""
	Initialises an OpenCV capture object.
	
	**Parameters:**
		* index (int) - The device ID of the camera.  If there is just one camera, this should be 0.
	
	**Returns:**
		A webcam instance.
		
	**Raises:**
		* NameError:  The device ID of the camera is invalid.
	
	.. todo::
		* Stereo capture mode?
	"""
	def __init__(self, index = 0):
		self.cap = cv.CaptureFromCAM(index)
		if not cv.QueryFrame(self.cap): # Not sure why I can't just check self.cap here, it seems to return a capture oject even if initialisation fails.  Weird.
			raise NameError("Camera initialisation didn't work, maybe the wrong camera index?")
	def show(self, flip = True):
		"""
		Grab an image from the webcam and show it in a :func:`cv.NamedWindow` called 'webcam'.
		
		**Parameters:**
			* flip (bool) - Used to rectify the image if using a webcam which is facing you.  
		"""
		frame = cv.QueryFrame(self.cap)
		if flip:
			cv.Flip(frame, flipMode = 1)
		show(frame, 'webcam')
	def get(self, flip = True):
		"""
		Grab an image from the webcam.
		
		**Parameters:**
			* flip (bool) - Used to rectify the image if using a webcam which is facing you.  
		
		**Returns:**
			The webcam image.
		"""
		frame = cv.QueryFrame(self.cap)
		if flip:
			cv.Flip(frame, flipMode =1)
		return frame
