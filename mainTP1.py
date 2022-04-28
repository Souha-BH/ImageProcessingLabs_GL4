import matplotlib.pylab as p 
from ReadWriteBinaryPGM import readPGM
from Histograms import imdisp, histogramme,histogramme_cumule, histogramme_egalise
from ImageStats import moyenne, ecart_type

def main():

    #read a pgm image
    img=readPGM("./images/mona_lisa.pgm")
    data,dimx,dimy, graylevel= img
    #calculate avg and variation
    moy=moyenne(img)
    print("La moyenne de cette image est : ",moy)
    ecart=ecart_type(img)
    print("L'écart type de cette image est : ",ecart)
    #display pgm image
    p.subplot(1,2,1)
    imdisp(img)
    his_c = histogramme_cumule(data,256)
    p.subplot(1,2,2)
    p.plot(his_c)
    p.show()

    #display histogram
    his = histogramme_egalise(data,256)
    p.subplot(1,2,2)
    p.plot(his)
    p.show()


if __name__ == "__main__":
    main()