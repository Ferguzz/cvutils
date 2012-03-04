import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('kitten.jpg')

im = rotate(im, 20)
im = zoom(im, 3)
mat = blackandwhite(mat)
mat = zoom(mat, 2, (100,4000))

show(im)
show(mat, 'mat version')

wait()





