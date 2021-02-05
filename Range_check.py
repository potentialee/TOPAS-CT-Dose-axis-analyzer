# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 14:18:54 2021

@author: Chanil
"""

### Proton range checker ###

import matplotlib.pyplot as plt
import pydicom
import csv
import numpy as np

#####

# RT dose image show

#####

def doseImageShow (dosemap, slicenumber, title, colormap) :

    fig, ax = plt.subplots()
    zplane = dosemap.pixel_array[slicenumber] * dosemap.DoseGridScaling
    ax.set_title(title)
    ax.imshow(zplane, cmap = colormap)
    plt.show()
    
## Load DICOM image

Dosemap_170MeV_Atom = pydicom.dcmread('./Result_Dicom_Data/Dosemap_170MeV_Atom.dcm')
Dosemap_190MeV_Atom = pydicom.dcmread('./Result_Dicom_Data/Dosemap_190MeV_Atom.dcm')
Dosemap_170MeV_G4WATER = pydicom.dcmread('./Result_Dicom_Data/Dosemap_170MeV_G4WATER.dcm')
Dosemap_190MeV_G4WATER = pydicom.dcmread('./Result_Dicom_Data/Dosemap_190MeV_G4WATER.dcm')

## Plot RT dose image

doseImageShow(Dosemap_170MeV_Atom, 11, 'Dosemap 170MeV (Atom Phantom)' , 'gist_ncar')
doseImageShow(Dosemap_190MeV_Atom, 11, 'Dosemap 190MeV (Atom Phantom)' , 'gist_ncar')
doseImageShow(Dosemap_170MeV_G4WATER, 100, 'Dosemap 170MeV (G4-WATER)' , 'gist_ncar')
doseImageShow(Dosemap_190MeV_G4WATER, 100, 'Dosemap 190MeV (G4-WATER)' , 'gist_ncar')

#####

# TOPAS CT CSV outpuit data analyze by each axis

#####

## CT X,Y,Z pixel specification
XPixel = 512
YPixel = 512
ZPixel = 184

def CSVAxisDataSortX(CSVData) :
    print('Start to sort X axis of the file. Please wait..')
    RawLineData = csv.reader(CSVData)
    SortData_x = [[0 for col in range(2)] for row in range(XPixel)]
    XValue = 0
    YValue = 0
    ZValue = 0
    for line in RawLineData:
        
        if (YValue > YPixel - 1) :
            YValue = 0
            XValue = XValue + 1
        if (YValue <= YPixel - 1) :
            if (ZValue <= ZPixel-1) :
                ZValue = ZValue + 1
            if (ZValue > ZPixel -1):
                YValue =  YValue + 1
                ZValue = 0
        
        SortData_x[XValue][0] = XValue
        SortData_x[XValue][1] = SortData_x[XValue][1] + float(line[3])
        
    print('######################################## Sorted X Data ########################################')        
    print(SortData_x)
    
    return SortData_x
          
def CSVAxisDataSortY(CSVData) :
    print('Start to sort Y axis of the file. Please wait..')
    RawLineData = csv.reader(CSVData)
    SortData_y = [[0 for col in range(2)] for row in range(YPixel)]
    YValue = 0
    ZValue = 0
    for line in RawLineData:
        SortData_y[YValue][0] = YValue
        if (ZValue <= ZPixel-1) :
            SortData_y[YValue][1] = SortData_y[YValue][1] + float(line[3])
            ZValue = ZValue + 1
            if (ZValue > ZPixel-1) :
                ZValue = 0
                YValue = YValue + 1
                if (YValue > YPixel-1) :
                    YValue = 0
                
            
    print('######################################## Sorted Y Data ########################################')        
    print(SortData_y)
    
    return SortData_y

def CSVAxisDataSortZ(CSVData) :
    print('Start to sort Y axis of the file. Please wait..')
    ZValue = 0
    RawLineData = csv.reader(CSVData)
    SortData_z = [[0 for col in range(2)] for row in range(ZPixel)]
    for line in RawLineData :
        SortData_z[ZValue][0] = ZValue
        SortData_z[ZValue][1] = SortData_z[ZValue][1] + float(line[3])
        ZValue = ZValue + 1
        if (ZValue > ZPixel-1) :
            ZValue = 0
    
    print('######################################## Sorted Z Data ########################################')        
    print(SortData_z)
    
    return SortData_z
        
CT_CSV_Data = open('Dosemap.csv')
Sorted_data_X = CSVAxisDataSortX(CT_CSV_Data)
CT_CSV_Data.close()

print('### Start to write CSV file of X axis. Please wait.. ###')
f_x = open('Sorted_Dosemap_x.csv', 'w', encoding='utf-8', newline='')
writer_x = csv.writer(f_x)
for Data in Sorted_data_X :
    writer_x.writerow(Data)
f_x.close()
print('### Write result CSV file of X axis complete! ###')

CT_CSV_Data = open('Dosemap.csv')
Sorted_data_Y = CSVAxisDataSortY(CT_CSV_Data)
CT_CSV_Data.close()

print('### Start to write CSV file of Y axis. Please wait.. ###')
f_y = open('Sorted_Dosemap_y.csv', 'w', encoding='utf-8', newline='')
writer_y = csv.writer(f_y)
for Data in Sorted_data_Y :
    writer_y.writerow(Data)
f_y.close()
print('### Write result CSV file of Y axis complete! ###')

CT_CSV_Data = open('Dosemap.csv')
Sorted_data_Z = CSVAxisDataSortZ(CT_CSV_Data)
CT_CSV_Data.close()

print('### Start to write CSV file of Z axis. Please wait.. ###')
f_z = open('Sorted_Dosemap_z.csv', 'w', encoding='utf-8', newline='')
writer_z = csv.writer(f_z)
for Data in Sorted_data_Z :
    writer_z.writerow(Data)
f_z.close()
print('### Write result CSV file of Z axis complete! ###')
    
