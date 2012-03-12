import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('baboon.jpg')

rot = rotate(im, 20)
rot = zoom(rot, 2)
# show(rot)

# show(sample(mat, (100,300), pos = (100,1000)))
bw = blackandwhite(mat)
zoom = zoom(bw, 2, (1000,20))
# show(zoom)

im = saltandpepper(im, 0.05)
im = contrast(im, 0.7)

im = brightness(im, 100)
show(im, 'optional title')

noise = cv.LoadImage('kitten.jpg')
n = gaussiannoise(blackandwhite(noise), std = 30)
show(n)

s, pos = sample(mat, return_pos = True)
print pos

wait()



