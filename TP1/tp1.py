
import numpy as n
import scipy as s
import matplotlib.pylab as p 
import math

def readPGM(file): 
    fp = open(file,'rb')
    if fp.readline() == b'P5\n':
        while True:
            line = fp.readline().decode()
            if line[0] != '#': break      
        dimx,dimy=line.split()
        dimx,dimy=int(dimx),int(dimy)
        graylevel=fp.readline()
        data = list(fp.read(dimx*dimy))
        if len(data) != dimx*dimy:
            print ('readPGM: error with ' + file + ': has wrong size')
        fp.close()
        return (data,dimx,dimy,graylevel)
    else:
        print( 'readPGM: error with '+ file + ': unsupported format')
    fp.close()
    return None

def writePGM(image,file):
   data,dimx,dimy,graylevel = image
   fp = open(file,'wb')
   fp.writelines([bytes('P5\n'+'"#CREATOR: Souha Ben Hassine \n'+str(dimx)+' '+str(dimy)+'\n'+ str(graylevel)+'\n','utf8')])
   fp.write(bytearray(data))
   fp.close()

def moyenne(image):
    data,dimx,dimy,graylevel =image
    somme=0
    for i in range(len(data)):
        somme+= data[i]
    return somme/(dimx*dimy)
        
def ecart_type(image):
    moy=moyenne(image)
    ecart_type=0
    data,dimx,dimy,graylevel =image
    for i in range(len(data)):
        ecart_type+=(data[i]-moy)**2
    return math.sqrt(ecart_type/(dimx*dimy))

#image display
def imdisp(image):
   data,x,y,graylevel=image
   p.gray()
   p.imshow(p.array(data).reshape((y,x)),vmin=0,vmax=25)

def histogramme(data,n):
   his = [0]*n
   for val in data:
      his[val] += 1
   return his

def histogramme_cumule(data,n):
    his = histogramme(data,n)
    his_c = [0]*n
    his_c[0]=his[0]
    for i in range(1,len(his)):
        his_c[i]=his[i]+his_c[i-1]
    return his_c

def main():

    #read a pgm image
    img=readPGM("mona_lisa.pgm")
    olena,dimx,dimy, graylevel= img
    #calculate avg and variation
    moy=moyenne(img)
    print("La moyenne de cette image est : ",moy)
    ecart=ecart_type(img)
    print("L'écart type de cette image est : ",ecart)
    #display pgm image
    p.subplot(1,2,1)
    imdisp(img)
    his_c = histogramme_cumule(olena,256)
    p.subplot(1,2,2)
    p.plot(his_c)
    p.show()

    #display histogram
    his = histogramme(olena,256)
    p.subplot(1,2,2)
    p.plot(his)
    p.show()


if __name__ == "__main__":
    main()