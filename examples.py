import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('kitten.jpg')

im = rotate(im, 20)
im = zoom(im, 0.1)
mat = blackandwhite(mat)
mat = zoom(mat, 2, (100,4000))

saltandpepper(im, 0.05)

show(im)
show(mat, 'mat version')

wait()





