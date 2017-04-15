
# coding: utf-8

# In[1]:

#import required python modules
from glob import glob
import csv
import numpy as np


# In[2]:

#this function reads in the ith file in the EyeTracking folder
def readOgamaTsv(i):
    data = []
    with open(files[i]) as f:
        for line in f:
            if line[0] is not '#':
                temp = line.strip().split('\t')
                data.append(temp)
    delete = []
    
    #if the file name ends with "Fixations", then it has the fixations data and this will read it in as such
    if files[i][-13:] == 'Fixations.txt':
        #flag the unneeded columns for deletion
        todelete = ['ID','SubjectName','TrialSequence',
                    'PosX','PosY','Trial Name','Trial Category',
                    'SlideNr','AOI Group']
        #identify the locations of the falgged columns
        for j in range(len(data[0])):
            if data[0][j] in todelete:
                delete.append(j)
        
    #if the file name ends with "Saccades", then it has the fixations data and this will read it in as such
    if files[i][-12:] == 'Saccades.txt':
        #flag the unneeded columns for deletion
        todelete = ['ID','SubjectName','TrialSequence','CountInTrial',
                    'StartTime','Validity','SubjectCategory','Age','Sex',
                    'Handedness','Comments','Trial Name', 'Trial Category',
                    'SlideNr','Saccade Target AOI Group']
        #identify the locations of the falgged columns
        for j in range(len(data[0])):
            if data[0][j] in todelete:
                delete.append(j)
    
    #delete the unnecessary columns to speed processing later
    for r in range(len(data)):
                data[r] = np.delete(data[r],delete)
                data[r]= data[r].tolist()
                del data[r][-1]
            
    return data


# In[3]:

def flipRowsCols(data):
    flipped = []
    
    #data is origionally read in row-by-row, this seperates it into columns.
    for i in range(len(data[0])):
        flipped.append([data[v][i] for v in range(len(data))])
        
        
    return flipped


# In[4]:

#all songs are recorded in the same file, this seperates each song
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

#This function identifies the point when the pianist switches from reading the piece to playing it
#it does this by finding the largest section of the data with the highest concentration of fixations within the "greenDot"
#location which is what we asked players to look at before playing the pieces
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

#This deletes all data before the subject started playing the piece
def removeReading(data):
    for s in range(len(data)):
        if len(data[s])and data[s][-2].count('GreenDot'):
            for c in range(len(data[0])):
                data[s][c] = np.delete(data[s][c],range(findGreenDot(data[s][-2])))
                data[s][c]= data[s][c].tolist()
    return data


# In[7]:

files = glob("./EyeTracking/*.txt") # creates a list of all files in the EyeTracking folder


# In[8]:

exceloutput = []
#print headers for the csv
exceloutput.append(['Subject ID', 'Song ID', "Playing Time", 
                    'Fixation Count','Fixation Duration','Saccade Length',
                    'Saccade Duration','Path Velocity']) 

#this calculates the eye tracking measures for each person and song
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

#print calculated data to csv file
with open('eyeTrackingData.csv','w+') as f:
    for row in range(len(exceloutput)):
        for col in range(len(exceloutput[0])):
            f.write(str(exceloutput[row][col])+',')
        f.write('\n')

