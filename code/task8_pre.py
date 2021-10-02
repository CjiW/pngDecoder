import cv2

videoFile = './before/before.mp4'
outputFile = './images/image_'
vc = cv2.VideoCapture(videoFile)
c = 1
if vc.isOpened():
    rval, frame = vc.read()
else:
    print('openerror!')
    rval = False
while rval:
    rval, frame = vc.read()
    cv2.imwrite(outputFile + str(c) + '.png', frame)
    c += 1
    cv2.waitKey(1)
vc.release()
