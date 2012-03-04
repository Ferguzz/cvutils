import cv
from cvutils import *

im = cv.LoadImage('kitten.jpg')
mat = cv.LoadImageM('kitten.jpg')
t = cv.LoadImageM('kitten.jpg')

im = rotate(im, 20)
# mat = rotate(mat, -20)
t = zoom(t, 2, (100,4000))
# im = zoom(im, 10, (130,30))

# show(im, title='im')
# show(mat)
# show(im, title = 'im2')
# show(t, 'test')
show(t)
show(mat)

wait()



