import matplotlib.pylab as p 
#image display
def imdisp(image):
   data,x,y,graylevel=image
   p.gray()
   p.imshow(p.array(data).reshape((y,x)),vmin=0,vmax=25)

def histogramme(data,graylevel):
   his = [0]*graylevel
   for val in data:
      his[val] += 1
   return his

def histogramme_cumule(data,graylevel):
    his = histogramme(data,graylevel)
    his_c = [0]*graylevel
    his_c[0]=his[0]
    for i in range(1,len(his)):
        his_c[i]=his[i]+his_c[i-1]
    return his_c

def histogramme_egalise(data,graylevel):
    
    his_c= histogramme_cumule(data,graylevel)
    p_c=[his_c[i]/len(data) for i in range(graylevel)]
    n1=[int(p_c[k]*(graylevel-1)) for k in range(graylevel)]
    new_data=data.copy()
    for j in range(len(data)):
        new_data[j]=n1[new_data[j]]
    return histogramme(new_data,graylevel)