
from Tkinter import*
from PIL import Image,ImageTk
import tkFileDialog
import cv2
import numpy as np
import glob
import imutils
import Tkinter       


def select_image():
    # referensi image panel
    global panelA,panelB
    template_data=[]
    files1= glob.glob('Latih/*.jpg')
    #buka file dan pilih input image
    path=tkFileDialog.askopenfilename()
    lbl.configure(text="Tidak ada Template yang sama")
    lbl.pack()
    #memastikan file path telah dipilih
          #load image dari disk, konversikan ke grayscale dan deteksi tepi
          
    if len(path)>0:
        for myfile in files1:
            image = cv2.imread(myfile)
            print "Nilai Citra Asli"
            print image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print "Nilai Citra Grayscale"
            print image
            image = cv2.Canny(image, 50, 100)
            template_data.append(image)
                
        #Perulangan untuk template matching
        for tmp in template_data:
            (tH, tW) = tmp.shape[:2]
                #cv2.imshow("Template", tmp)
            
        # Melakukan perulangan untuk meload data gambar dan melakukan template matching
        
        #x = kolom.get()
        
            
            for imageP in glob.glob(path):
               
        	# Convert kegrayscale
        	 imageS = cv2.imread(imageP)
        	 gray = cv2.cvtColor(imageS, cv2.COLOR_BGR2GRAY)
        	 found = None
        	# melakukan perulangan untuk melakukan scaling pada gambar
        	 for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        		# Merescale gambar sesuai dengan skala dan rasio yang diberikan
        	  	resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        		r = gray.shape[1] / float(resized.shape[1])
        
        		# Jika gambar yang di rescale lebih kecil dari template
        		# break loop
        		if resized.shape[0] < tH or resized.shape[1] < tW:
        			break
        
        		# Deteksi tepi untuk gambar yang telah discale
        		# Melakukan Template Matching
        		edged = cv2.Canny(resized, 50, 100)
        		result = cv2.matchTemplate(edged, tmp, cv2.TM_CCOEFF_NORMED)
        		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        		# jika ketemu dengan variable berskala baru, maka simpan
        		if found is None or maxVal > found[0]:
                            found = (maxVal, maxLoc, r)
                         
                                
            	# keluarkan variable gambar yang telah di skala dan kembalikan ke skala asli
        	# berikan kotakan pada gambar asli jika ditemukan kecocokan template
                	(maxVal, maxLoc, r) = found
                	(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
                	(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
                        if maxVal >= 0.4:
                            cv2.rectangle(imageS, (startX, startY), (endX, endY), (0, 0, 255), 5)
                       # cv2.imshow("Image", imageS)
                       # cv2.waitKey(0)
                       #konversi image dan edge dari OpenCV ke format PIL
                            imageS=Image.fromarray(imageS)
                            tmp=Image.fromarray(tmp)
                    
                            #konversikan image dan edge PIL ke format ImageTk
                            imageS=ImageTk.PhotoImage(imageS)
                            tmp=ImageTk.PhotoImage(tmp)
                            
                        # lakukan inisialisasi panel
                            if panelA is None or  panelB is None:
                                #panel petama akan menyimpan original image
                                panelA=Label(image=imageS)
                                panelA.image=imageS
                                panelA.pack(side="left", padx=10, pady=10)
                    
                                #panel kedua menyimpan hasil deteksi
                                panelB=Label(image=tmp)
                                panelB.image=tmp
                                panelB.pack(side="right",padx=10,pady=10)
                                lbl.configure(text="Match")
                                lbl.pack()
                    
                                #jika tidak, update image panel
                            else:
                                panelA.configure(image=imageS)
                                panelB.configure(image=tmp)
                                panelA.image=imageS
                                panelB.image=tmp
                                
                        #else:
         
#inisialisasi window 
root=Tk()
panelA=None
panelB=None
lbl=Tkinter.Label(root,text="Match")

#create button
btn=Button(root,text="Select an Image",command=select_image)
btn.pack(side="bottom",fill="both",expand="yes",padx="10",pady="10")

root.mainloop()
