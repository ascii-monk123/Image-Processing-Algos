import cv2
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import png

class LSB:

    #image will be stored as a property of the instance object if getImage called
    image=None
    keys=""
    '''

    This method reads and stores the image as a property of the instance object.
    return type -> None

    '''
    def getImage(self,path:str)->None:
        try:
            self.image=cv2.imread(path)
        except Exception as E:
            print(E)
            print('Please enter valid image path')

    '''

    This method converts the image from bgr2rgb for the instance object.
    return type -> None

    ''' 
    def bgr2rgb(self):
        if self.image is not None:
            try:
                self.image=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            except Exception as E:
                print(E)
                print('Unable to convert the image')


    '''
    This method will count the number of bits that can be encoded into the image.
    return type -> int
    '''
    def countBits(self)->int:
        if self.image is not None:
            shape=self.image.shape
            totalEle=shape[0]*shape[1]*shape[2]
            return totalEle
        else:
            return -1

    '''
    This method will encode the image using least significant bit steganography.
    return type -> bool 
    '''
    def encode(self,text,imagePath,keyPath)->bool:
        if self.image is not None:
            #this will store key
            key=""
            totalPix=self.countBits()
            #text to bits
            byte_text=[ele for ele in''.join(format(ord(char),'08b')for char in text)]
            print(byte_text)
            #check whether image can be stored
            if totalPix==-1 or len(byte_text)>totalPix:
                return False
            #r,g and b channels
            r,g,b=self.image[:,:,0].reshape(-1),self.image[:,:,1].reshape(-1),self.image[:,:,2].reshape(-1)

            rindex,gindex,bindex=(0,0,0)
            #logic to encrypt the original image
            for i in range(0,len(byte_text)):
                if i%3==0:
                    rval=[ele for ele in np.binary_repr(r[rindex],width=8)]
                    rval.pop()
                    rval.append(byte_text[i])
                    rval=''.join(rval)
                    r[rindex]=int(rval,2)
                    key+="r:{} ".format(rindex)
                    rindex+=1
                elif i%3==1:
                    gval=[ele for ele in np.binary_repr(g[gindex],width=8)]
                    gval.pop()
                    gval.append(byte_text[i])
                    gval=''.join(gval)
                    g[gindex]=int(gval,2)
                    key+="g:{} ".format(gindex)
                    gindex+=1
                elif i%3==2:
                    bval=[ele for ele in np.binary_repr(b[bindex],width=8)]
                    bval.pop()
                    bval.append(byte_text[i])
                    bval=''.join(bval)
                    b[bindex]=int(bval,2)
                    key+="b:{} ".format(bindex)
                    bindex+=1
       
            self.keys=key
            #convert into numpy array
            rgb=np.dstack((r,g,b)).reshape(self.image.shape)
            self.image=rgb.copy()
            #save keys
            saved=self.saveKeys(keyPath)
            try:
                #save image
                with open(imagePath,"wb") as fh:
                    pngWriter=png.Writer(width=self.image.shape[1],height=self.image.shape[0],bitdepth=8,greyscale=False,compression=0)
                    image=self.image.copy().reshape(-1,self.image.shape[1]*self.image.shape[2]).tolist()
                    pngWriter.write(fh,image)
            except Exception as e:
                print(e)
                
                return False
            if not saved:
                print('Cannot generate keys. Try again')
                return False
            return True

        else:
            print('First read an image')
            return False

    '''
    This method will show the image using matplotlib.
    return type -> none
    '''
    def showImage(self):
        if self.image is not None:
            plt.imshow(self.image)

    '''
    Save the keys to txt file
    return type->bool
    '''
    def saveKeys(self,keyPath):
        try:
            with open(keyPath,"w") as fh:
                fh.write(self.keys)
            return True
        except:
            return False
    
    '''
    This method will read the encrypted image using keys and then return the text value
    return type -> String or boolean
    boolean if not able to decrypt
    '''
    @staticmethod
    def decryptImage(imagePath,keyPath)->str or bool:
        try:
            with open(keyPath,'r') as fh:
                key=fh.read().strip()
            image=cv2.cvtColor(cv2.imread(imagePath),cv2.COLOR_BGR2RGB)
            r,g,b=image[:,:,0].reshape(-1),image[:,:,1].reshape(-1),image[:,:,2].reshape(-1)

            
            #convert key to array
            temp=key.split(' ')
            bitArr=[]
            for ele in temp:
                type,index=tuple(ele.split(':'))
                index=int(index)
                if type=='r':
                    ele=np.binary_repr(r[index],8)  
                elif type=='g':
                    ele=np.binary_repr(g[index],8)
                elif type=='b':
                    ele=np.binary_repr(b[index],8)
                bitArr.append(ele[len(ele)-1])
            text=LSB.bitArr2Str(bitArr)
            return text
        
        except Exception as E:
            print(E)
            return False
    
    '''
    This method converts bitstring to corresponding characters
    returns -> str
    '''
    @staticmethod
    def bitArr2Str(bitArr):
        collecStr=''
        retStr=""
        for index,bit in enumerate(bitArr):
            collecStr+=bit
            if index%8==7:
                retStr+=chr(int(collecStr,2))
                collecStr=""
        return retStr
        
            








