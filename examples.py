import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('baboon.jpg')

rot = rotate(im, 45)
# rot = zoom(rot, 2)
show(overlay(rot, sample(mat, size=(100,100)), pos = (250,30), blend = 0.5))

# show(sample(mat, (100,300), pos = (100,1000)))
bw = blackandwhite(mat)
zoom = zoom(bw, 2, (1000,20))
# show(zoom)

im = saltandpepper(im, 0.05)
im = contrast(im, 0.7)

im = brightness(im, 100)
# show(im, 'optional title')

noise = cv.LoadImage('kitten.jpg')
n = gaussiannoise(blackandwhite(noise), std = 30)
show(n)

s, pos = sample(mat, return_pos = True)
print pos

cam = webcam()
s = cam.get()
print 'Cam resolution: %d, %d' %(s.width, s.height)

print 'Press Esc to stop...'
while(cv.WaitKey(1) != 0x1b):
	cam.show()
	
# wait()



