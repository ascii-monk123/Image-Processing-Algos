from typing import Tuple
import numpy as np
import math
'''

Note: This algorithm only works for binary image. So be sure to convert the image into a binary format before applying the algorithm
Author: Aahan Singh
Department: CSE
Institution: Manipal University Jaipur
License: M.I.T
Extra: Why would I copyright something which hasn't even been developed by me :)


'''


class MooreBoundary:

    #initialize self.image as  a copy of the original image
    def __init__(self,imageRef)->bool:
        self.image=imageRef.copy()
    
    #move up
    def moveUp(self,row,col)->Tuple:
        return (row-1,col)
    #move down

    def moveDown(self,row,col)->Tuple:
        return (row+1,col)
    #move left
    def moveLeft(self,row,col)->Tuple:
        return (row,col-1)
    #move right
    def moveRight(self,row,col)->Tuple:
        return (row,col+1)

    #the main method to calculate the boundaries
    def findBoundary(self)->list:
        
        #applypadding from all the sides to the image
        row,cols=self.image.shape
        
        colPad=np.zeros((1,cols),dtype=np.uint8)
        rowPad=np.zeros((row+2,1),dtype=np.uint8)

        self.image=np.hstack((rowPad,np.hstack((np.vstack((colPad,np.vstack((self.image,colPad)))),rowPad))))
        hCoordinates=[]
        c=[]
        i,j=0,0
        for r in self.image:
            if len(hCoordinates)>0:
                break
            for col in r:
                if col==255:
                    hCoordinates.append((i,j))
                    c.append((i,j-1))
                    break
                if j==len(r)-1:
                    j=0
                    break
                    
                else:
                    j+=1
            i+=1
        
        #main algorithm start
        cR,cC=c[len(c)-1]
        hR,hC=hCoordinates[len(hCoordinates)-1]
        hnewR,hnewC=hR,hC
        times=0
        while( hnewC!=hC or hnewR !=hR or times==0):
            cArr=[(cR,cC)]
            #loop through all the neighboring pixels
            for i in range(0,8):
                if self.image[cR][cC]==np.uint8(255):
                    hnewC,hnewR=cC,cR
                    hCoordinates.append((hnewR,hnewC))
                    cArr.pop()
                    cR,cC=cArr.pop()
                    break
                sumC,sumR=cC-hnewC,cR-hnewR
                if sumC==-1 and sumR==0:
                    cR,cC=self.moveUp(cR,cC)
                elif sumC==1 and sumR==0:
                    cR,cC=self.moveDown(cR,cC)
                elif sumC==-1 and sumR==-1:
                    cR,cC=self.moveRight(cR,cC)
                elif sumC==0 and sumR==-1:
                    cR,cC=self.moveRight(cR,cC)
                elif sumC==1 and sumR==-1:
                    cR,cC=self.moveDown(cR,cC)
                elif sumC==1 and sumR==1:
                    cR,cC=self.moveLeft(cR,cC)
                elif sumC==0 and sumR==1:
                    cR,cC=self.moveLeft(cR,cC)
                elif sumC==-1 and sumR==1:
                    cR,cC=self.moveUp(cR,cC)
                cArr.append((cR,cC))
            times+=1
        return hCoordinates

    
    #define construct image from co-ordinates
    def constructImage(self,shp,coordinates)->np.ndarray:
        img=np.zeros(shape=shp,dtype=np.uint8)
        
        for ele in coordinates:
            x,y=ele[0],ele[1]
            img[x][y]=np.uint8(255)
        return img

        



