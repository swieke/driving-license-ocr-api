# Python 2/3 compatibility
from __future__ import print_function
from kraken import binarization
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import imutils
import pytesseract
import re
import json
import hashlib
# built-in modules
import os
import sys

def SimExtract(input, filename):
    # src = input
    img = Image.open(input)


    result = binarization.nlbin(img)
    rgb_im = result.convert('RGB')
    #rgb_im = rgb_im.rotate(270)
    

    open_cv_image = np.array(rgb_im) 
    # cv.imwrite('converted.jpg',open_cv_image)
    # Convert RGB to BGR 

    
    #cv.imwrite('new2.jpg', frame) ##CROPPED

    kernel = np.ones((2,2), np.uint8)

    img = open_cv_image 

    img = cv.dilate(img, kernel, iterations=2) 

    #img -> eroded

    image = cv.resize(img, (800,480))

    namaAlamat = image[143:192,0:660]
    tipe = image[0:109,609:780]
    kelamin = image[142:180,610:765]
    block = image[220:343,397:649]
    rt = image[190:228, 244:646]

    kernel = np.ones((2,2), np.uint8)
    tipe = cv.dilate(tipe, kernel, iterations=4)

    # cv.imwrite('block.jpg', block)
    # cv.imwrite('tipe.jpg', tipe)
    # cv.imwrite('kelamin.jpg', kelamin)
    # cv.imwrite('namaAlamat.jpg', namaAlamat)
    # cv.imwrite('rt.jpg', rt)

    #Cropped for each part

    text1 = pytesseract.image_to_string(namaAlamat, lang="ind", config='--psm 6 --oem 3')
    print(text1)
    text1 = text1.split("\n")
    text1[0] = text1[0].replace('1', 'I')
    nama = re.sub(r'[^a-zA-Z .:]',r'',text1[0])
    alamat = re.sub(r'[^a-zA-Z0-9 .:]',r'',text1[1])
    if 'NAMA' in nama:
        nama = nama.split('NAMA')[1]
        return
    elif 'nama' in nama:
        nama = nama.replace('nama', '')
    if 'ALAMAT' in alamat:
        alamat = alamat.split('ALAMAT')[1]
        return
    elif 'alamat' in alamat:
        alamat = alamat.replace('alamat','')
   
    
    if ':' in alamat:
        alamat = alamat.split(':')[1]

    
    
    
    
  
    

    text4 = pytesseract.image_to_string(rt, lang="ind", config='--psm 6 --oem 3')
    text4 = text4.split("\n")
    newText4 =''
    for i in text4:
        newText4 += ' ' + i
    if ':' in newText4:
        rt = newText4.split(':')[1]
    else:
        rt = newText4
   
    
    

    text5 = pytesseract.image_to_string(block, lang="ind", config='--oem 3')
    print(text5)
    if 'om' in text5:
        text5 = text5.replace('om','cm')
    if 'mm' in text5:
        text5 = text5.replace('mm','cm')
    text5 = text5.split('\n')
    print('oiiiiiii')
    print(text5)
    newText5 = [i for i in text5 if i!='']
    print(newText5)
    if 'cm' in newText5:
        newText5.remove('cm')
        newText5[2] += ' cm'
    print(newText5)
    datas = []
    datas.extend(newText5)
    if len(datas) != 6:
        datas.append('')
    print(datas)

    text3 = pytesseract.image_to_string(kelamin, lang="ind")
    print(text3)
    if 'PRI' or 'PRIA' in text3:
        text3 = 'PRIA'
        print('Jenis Kelamin :'+ text3)
    elif 'W' or 'WANITA' or 'WAN' in text3:
        text3 = 'WANITA'
        print('Jenis Kelamin :'+ text3)
    kelamin = text3

   
   


    # from datas
    teL = datas[0].strip().upper()
    taL = datas[1].strip().upper()
    tinggi = datas[2].strip()
    pekerjaan = datas[3].strip().upper()
    noSIM = datas[4]
    noSIM = re.sub(r'[^0-9]',r'', noSIM).strip()
    mb    = datas[5].strip()

    text2 = pytesseract.image_to_string(tipe, lang ="ind", config='-c tessedit_char_whitelist=AaBbCc --psm 6 --oem 3')
    print(text2)
   
    jenisSim = text2.strip().upper()
    
    
    
    # Cleaning data for JSON

    nama = re.sub(r'[^a-zA-Z .]',r'',nama).strip().upper()
    if 'NAMA' in nama:
        nama = nama.replace('NAMA','').strip()
    
    alamat = alamat.upper()
    if 'ALAMAT' in alamat:
        alamat = alamat.replace('ALAMAT','')
    rt = rt.upper()
    alamat = alamat + ' ' + rt
    alamat = alamat.strip()
    
    kelamin = text3.strip().upper()
    
    
    if tinggi[0]!='1':
        tinggi = '1'+tinggi
    pekerjaan = text5[3].strip().upper()
    if 'ARYAWAN SW' or 'SWASTA' or 'AWAN' in pekerjaan:
        pekerjaan = 'KARYAWAN SWASTA'

    



    x = {
        "message"       : "OCR Success",
        "success"       : True,
        "documentType"  : "SIMprocessed",
        "data"          : {
            "Nama" : nama,
            "Alamat": alamat,
            "JenisKelamin": kelamin,
            "TempatLahir" : teL,
            "TanggalLahir": taL,
            "Tinggi": tinggi,
            "Pekerjaan": pekerjaan,
            "NoSIM": noSIM,
            "JenisSIM": jenisSim,
            "mb":mb
        },
        "img"           : {
            "sim": filename,
        }
    }

    # convert into JSON:
    return x, filename

