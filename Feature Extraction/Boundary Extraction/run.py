import MooreBoundaryFollowing as mbf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
'''
Details: Test run for the Moore Border Following Algorithm for border feature extraction

'''
#runner function
if __name__=="__main__":
    fpath=input("Enter the path of the image : ")
    try:
        if len(fpath)<1:
            raise ValueError()
        file_path=os.path.join(fpath)
        image=cv2.cvtColor(cv2.imread(file_path),cv2.COLOR_BGR2GRAY)
        
        #binarizing the image
        _,image=cv2.threshold(image,0,255,type=cv2.THRESH_BINARY)
        
        #create a new MooreBoundry Objects
        mbfObj=mbf.MooreBoundary(image)

        #create a new image with border separated and return it
        borderCoords=mbfObj.findBoundary()

        #create a border image from the coordinates
        border_image=mbfObj.constructImage(image.shape,borderCoords)

        plt.imshow(border_image,cmap='gray')
        plt.show()

    

    except:
        raise ValueError()



    