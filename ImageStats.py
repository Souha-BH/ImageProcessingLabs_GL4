import math
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
