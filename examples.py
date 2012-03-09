import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('kitten.jpg')

im = rotate(im, 20)
im = zoom(im, 1)
show(sample(mat, (100,300), pos = (100,1000)))

mat = blackandwhite(mat)
mat = zoom(mat, 2, (1000,20))

saltandpepper(im, 0.05)

show(im)
show(mat, 'mat version')

wait()





