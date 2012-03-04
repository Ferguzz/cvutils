import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('kitten.jpg')
t = cv.LoadImageM('kitten.jpg')

im = rotate(im, 20)
mat = rotate(mat, -20)

show(im, title='im')
show(mat)
show(im, title = 'im2')
show(t)

wait()



