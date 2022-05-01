def change_contrast(data,graylevel):
    #look for min and max values
    min=0
    max=0
    for i in range(len(data)):
        if data[i]<=min:
            min=data[i]
        if data[i]>=max:
            max=data[i]   
    new_data=data.copy()
    for j in range(len(data)):
        new_data[j]=(graylevel*(data[j]-min))/(max-min)
    return new_data
    