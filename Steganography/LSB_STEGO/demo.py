from lsb import LSB

if __name__=='__main__':
    inst=LSB()
    path=input("Enter image path : ")

    #for demonstration we use this hard coded picture
    #read image
    inst.getImage(path)
    #convert to rgb
    inst.bgr2rgb()
    #encode
    text=""
    print()
    filename=input('Enter path to file containing text to be encrypted: ')
    with open(filename,encoding='utf-8-sig') as fh:
        text=fh.read()
    print()
    imagePath=input('Enter the path to save image along with imagename : ')
    keyPath=input('Enter the path to save the keys along with keyfile name : ') 
    encoded=inst.encode(text,imagePath,keyPath)
    
    #lets see the image
    if encoded:
        print('Image and keys saved')
    else:
        print('Image and keys cannot be saved')


    #check for decryption
    print()
    choice=input('Decrypt some image y(Yes) n(No) ?  ')
    if choice.lower()=='y':
        imagePath=input('Enter the path to encrypted image : ')
        print()
        keyPath=input('Enter the path to key files for the image : ')
        result=LSB.decryptImage(imagePath,keyPath)
        print()
        choice=input('Message decrypted. Enter path to txt file for dumping the messsage : ')
        print()
        try:
            with open(choice,'w') as fh:
                fh.write(result)
        except:
            print('Unable to write to the file')
    else:
        exit()