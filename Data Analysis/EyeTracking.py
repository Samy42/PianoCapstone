
# coding: utf-8

# In[1]:

from glob import glob
import csv
import re
import numpy as np


# In[2]:

def readOgamaTsv(i):
    data = []
    with open(files[i]) as f:
        for line in f:
            if line[0] is not '#':
                temp = line.strip().split('\t')
                data.append(temp)
    delete = []
    
    if files[i][-13:] == 'Fixations.txt':
        todelete = ['ID','SubjectName','TrialSequence',
                    'PosX','PosY','Trial Name','Trial Category',
                    'SlideNr','AOI Group']
        for j in range(len(data[0])):
            if data[0][j] in todelete:
                delete.append(j)
        

    if files[i][-12:] == 'Saccades.txt':
        delete = [0,2,4,8,9,10,11,12,13,14,15,16,18]
        todelete = ['ID','SubjectName','TrialSequence','CountInTrial',
                    'StartTime','Validity','SubjectCategory','Age','Sex',
                    'Handedness','Comments','Trial Name', 'Trial Category',
                    'SlideNr','Saccade Target AOI Group']
        for j in range(len(data[0])):
            if data[0][j] in todelete:
                delete.append(j)
    
    for r in range(len(data)):
                data[r] = np.delete(data[r],delete)
                data[r]= data[r].tolist()
            
    return data


# In[3]:

def flipRowsCols(data):
    flipped = []
    
    for i in range(len(data[0])):
        flipped.append([data[v][i] for v in range(len(data))])
        
        
    return flipped


# In[4]:

def splitBySong(data,headers):
    
    
    slides = []
    for i in range(6):
        temp = []
        for r in range(len(data[0])):
            if data[headers.index('TrialID')][r] == str(i):
                temp.append(r)
        slides.append(temp)
        
    split = []
    for s in range(6):
        if len(slides[s]) == 0:
            split.append([])
            continue
        temp = []
        for c in range(len(data)):
            temp.append(data[c][min(slides[s]):max(slides[s])+1])
        split.append(temp)
        
    return split


# In[5]:

def findGreenDot( data ):
    bestMaxAvg = 0
    bestEndIndex = 0
    
    if data.count('GreenDot'):
    
        for i in range(int(len(data)*.8)):

            zone = int(len(data)*.8)-i


            currentMaxAvg = 0
            currentEndIndex = 0

            for z in range(len(data)-zone-5):

                if (z+zone) > int(len(data)*0.8):
                    continue

                currentAvg = (data[z:z+zone].count('GreenDot'))/zone

                if currentAvg >= currentMaxAvg:
                    currentMaxAvg = currentAvg
                    currentEndIndex = z + zone
            if currentMaxAvg > bestMaxAvg:
                bestMaxAvg = currentMaxAvg
                bestEndIndex = currentEndIndex

    
    return bestEndIndex


# In[6]:

def removeReading(data):
    for s in range(len(data)):
        if len(data[s]):
            for c in range(len(data[0])):
                data[s][c] = np.delete(data[s][c],range(findGreenDot(data[s][-2])))
                data[s][c]= data[s][c].tolist()
    return data


# In[7]:

files = glob("./EyeTracking/*.txt")


# In[8]:

exceloutput = []
exceloutput.append(['Subject ID', 'Song ID', "Playing Time", 
                    'Fixation Count','Fixation Duration','Saccade Length',
                    'Saccade Duration','Path Velocity']) 
row = 0
for person in range(int(len(files)/2)): #starting with one person
    subjectID = files[0+(person*2)][-15:-13]
    #Fixation data preprocessing
    
    Fdata = readOgamaTsv(0+(person*2))
    Fheaders = Fdata[0]
    Fdata = flipRowsCols(Fdata)
    Fdata = splitBySong(Fdata,Fheaders)
    Fdata = removeReading(Fdata)
    
    #Saccade data preprocessing
    
    Sdata = readOgamaTsv(1+(person*2))
    Sheaders = Sdata[0]
    Sdata = flipRowsCols(Sdata)
    Sdata = splitBySong(Sdata,Sheaders)
    Sdata = removeReading(Sdata)

    for s in range(6):
        
        if not len(Fdata[s]): #don't write blank rows
            continue
            
        exceloutput.append([0]*8)
        row = row + 1


        if len(Fdata[s]) and len(Fdata[s][0]) and len(Fdata[s][0][0]):

            playingtime = int(Fdata[s][Fheaders.index('StartTime')][-1])- int(Fdata[s][Fheaders.index('StartTime')][0])

            fixationcount = len(Fdata[s][0])

            fixationduration = np.average([int(x) for x in Fdata[s][Fheaders.index('Length')]])

            exceloutput[row][exceloutput[0].index('Subject ID')] = subjectID
            exceloutput[row][exceloutput[0].index('Song ID')] = s
            exceloutput[row][exceloutput[0].index('Playing Time')] = playingtime
            exceloutput[row][exceloutput[0].index('Fixation Count')] = fixationcount
            exceloutput[row][exceloutput[0].index('Fixation Duration')] = fixationduration

        if len(Sdata[s]) and len(Sdata[s][0]) and len(Sdata[s][0][0]):

            saccadelength = np.average([float(x) for x in Sdata[s][Sheaders.index('Distance')]])
            saccadeduration = np.average([float(x) for x in Sdata[s][Sheaders.index('Duration')]])
            pathvelocity = np.average([float(x) for x in Sdata[s][Sheaders.index('Velocity')]])
            
            exceloutput[row][exceloutput[0].index('Saccade Length')] = saccadelength
            exceloutput[row][exceloutput[0].index('Saccade Duration')] = saccadeduration
            exceloutput[row][exceloutput[0].index('Path Velocity')] = pathvelocity


# In[9]:

with open('eyeTrackingData.csv','w+') as f:
    for row in range(len(exceloutput)):
        for col in range(len(exceloutput[0])):
            f.write(str(exceloutput[row][col])+',')
        f.write('\n')

