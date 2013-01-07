import SimpleCV
import cv
import serial
import time
    
cam = SimpleCV.Camera(1)
width = 320
height = 240

center = (width/2, height/2)
margin = (width * 0.1, height * 0.1)

def move_servos(xdistance, ydistance):
    #position = '%da%db' % (xdistance, ydistance)
    #position = "%d%d" % (xdistance, ydistance)
    if abs(xdistance) > 3:
    	xdistance = 0
    if abs(ydistance) > 3:
    	ydistance = 0
    position = 'x%dy%d\n' % (xdistance, ydistance)
    #position = '%d' % (xdistance)
    ser.write(position)
    print "moveservo serial is ", position
    #print ser.readline()

if __name__ == '__main__':
	ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=0)
	ser.write('r')
	move_servos(90, 90)
	while True:
	    img = cam.getImage().scale(width, height)
	    #faces = img.findHaarFeatures('/home/pgao/Desktop/OpenCV-2.4.0/data/haarcascades/haarcascade_frontalface_alt.xml')
	    faces = img.findHaarFeatures('/home/pgao/Dropbox/Private Files/School and Work/Programming/Hal/haarcascade_frontalface_alt.xml')
	    if faces:
	    	#print dir(faces[0])
	        for face in faces:
		    	face.draw()
		    	print face.coordinates()
		    	print face.corners()
		    	if face.coordinates()[0] > center[0] - margin[0] and face.coordinates()[0] < center[0] + margin[0] and \
		    	face.coordinates()[1] > center[1] - margin[1] and face.coordinates()[1] < center[1] + margin[1]:
		    		print "centered"
		    	else:
		    		xdistance = 0
		    		ydistance = 0

			    	xdistance = face.coordinates()[0] - (center[0] - margin[0])
			    	ydistance = face.coordinates()[1] - (center[1] - margin[1])

			   #  	if xdistance >= 0:
			   #  		xdistance = -1
			   #  	elif xdistance <= 0:
			   #  		xdistance = 1
			   #  	else:
			   #  		xdistance = 0

			   #  	if ydistance >= 0:
						# ydistance = -1
			   #  	elif ydistance <= 0:
			   #  		ydistance = 1
			   #  	else:
			   #  		ydistance = 0

			    	if xdistance < 25 and xdistance >= 0:
			    		xdistance = -1
			    	elif xdistance > 25:
			    		xdistance = -3
			    	elif xdistance > -25 and xdistance <= 0:
			    		xdistance = 1
			    	elif xdistance < -25:
			    		xdistance = 3
			    	else:
			    		xdistance = 0

			    	if ydistance < 25 and ydistance >= 0:
			    		ydistance = -1
			    	elif ydistance > 25:
			    		ydistance = -3
			    	elif ydistance > -25 and ydistance <= 0:
			    		ydistance = 1
			    	elif ydistance < -25:
			    		ydistance = 3
			    	else:
			    		ydistance = 0

			    	if face.coordinates()[0] < center[0] - margin[0]:
			    		print "too far to the left"
			    	elif face.coordinates()[0] > center[0] + margin[0]:
			    		print "too far to the right"
			    	else:
			    		print "left-right is centered"
			    		xdistance = 0

			    	if face.coordinates()[1] < center[1] - margin[1]:
			    		print "too far up"
			    	elif face.coordinates()[1] > center[1] + margin[1]:
			    		print "too far down"
			    	else:
			    		print "up-down is centered"
			    		ydistance = 0

			    	move_servos(xdistance, ydistance)
	    img.show()