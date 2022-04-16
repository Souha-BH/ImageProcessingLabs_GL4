
import numpy as n
import scipy as s
import matplotlib.pylab as p 

def readPGM(file): 

    fp = open(file,'rb')
    if fp.readline() == b'P5\n':
        while True:
            line = fp.readline().decode()
            if line[0] != '#': break      
        dimx,dimy=line.split()
        dimx,dimy=int(dimx),int(dimy)
        l=fp.readline()
        data = list(fp.read(dimx*dimy))
        if len(data) != dimx*dimy:
            print ('readPGM: error with ' + file + ': has wrong size')
        fp.close()
        return (data,dimx,dimy)
    else:
        print( 'readPGM: error with '+ file + ': unsupported format')
    fp.close()
    return None

def writePGM(filepath, image):
    # image is a tuple of (data,width,height,graylevel)
    file = open(filepath, "w")
    file.write("P2\n")
    file.write(str(s.width) + " " + str(s.height) + "\n")
    file.write(str(s.graylevel) + "\n")
    for num in range(0, len(image)):
        file.write(str(image[num]) + " ")
        if ((num + 1) % s.width == 0):
            file.write("\n")
    file.close()


def imdisp(img):
   data,x,y=img
   p.gray()
   p.imshow(p.array(data).reshape((y,x)),vmin=0,vmax=25)

def histogram(data,n):
   his = [0]*n
   for val in data:
      his[val] += 1
   return his
olena,dimx,dimy = readPGM('mona_lisa.pgm')

p.subplot(1,2,1)
imdisp((olena,dimx,dimy))
his = histogram(olena,256)
p.subplot(1,2,2)
p.plot(his)
p.show()
img=readPGM("mona_lisa.pgm")
imdisp(img)
p.show()
test = 'test.pgm'

