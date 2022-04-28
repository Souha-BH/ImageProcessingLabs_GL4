
def readPGM(file): 
    fp = open(file,'rb')
    if fp.readline() == b'P5\n':
        while True:
            line = fp.readline().decode()
            if line[0] != '#': break      
        dimx,dimy=line.split()
        dimx,dimy=int(dimx),int(dimy)
        graylevel=int(fp.readline().decode())
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
   fp.writelines([bytes('P5\n'+'"#CREATOR: Souha Ben Hassine & Cyrine Zaouali\n'+str(dimx)+' '+str(dimy)+'\n'+ str(graylevel)+'\n','utf8')])
   fp.write(bytearray(data))
   fp.close()
