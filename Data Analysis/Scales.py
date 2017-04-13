
# coding: utf-8

# In[1]:

import pandas
from glob import glob


# In[2]:

files = glob('./MIDIfiles/Scales/csv/*.csv')


# In[3]:

octave = 12


# In[4]:

noteNum = {'C': 60, 'C#':61, 'D':62,'D#':63,'E':64,'F':65,'F#':66,'G':67,'G#':68,'A':69,'A#':70,'B':71}


# In[5]:

def extractNotes(file):
    df = pandas.read_csv(files[file], header = None , names=['Onset (Beats)','Duration (Beats)','MIDI Channel','MIDI Pitch','Velocity','Onset (Sec)','Duration (sec)'])
    return df['MIDI Pitch'].tolist()


# In[6]:

correctNotes = pandas.read_csv('correctScales.csv')


# In[7]:

def checkScale(notes, letter):
    score = 0
    
    deleteOctave(notes, letter)
    
    for n in range(len(notes)-14):
        if (notes[n] == noteNum[letter]) and (notes[n+7] ==noteNum[letter]+octave) and (notes[n+14] == noteNum[letter]):
            for p in range(15):
                if notes[n + p] != correctNotes[letter + ' Major Scale'][p]:
                    score = score + 1
                return [letter, score]
            
    return [letter, 15]


# In[8]:

def checkArpeggio(notes, letter):
    score = 0
    
    for n in range(len(notes)-14):
        if (notes[n] == noteNum[letter]) and (notes[n+3] ==noteNum[letter]+octave) and (notes[n+6] == noteNum[letter]):
            for p in range(7):
                if notes[n + p] != correctNotes[letter + ' Major Arpeggio'][p]:
                    score = score + 1
                return score
            
    return 7


# In[9]:

# 1 octave: n1-6-n2-6-n1

#2 octaves: n1 - 6 - n2 - 6 - n3 - 6 - n2 - 6 - n1 
#          = n1 - 6 - n2 - 13 - n2 - 6 - n1

#3 octaves: n1-6-n2-6-n3-6-n4-6-n3-6-n2-6-n1
#         = n1-6-n2-6-n3-13-n3-6-n2-6-n1
#         = n1-6-n2-6-15-6-n2-6-n1
#         = n1-6-n2-27-n2-n1
#each octive = ney num + 12*octaves

def deleteOctave(notes, letter):
    for n in range(len(notes)-14):
        if (notes[n] == noteNum[letter]+octave) and (notes[n+7] ==noteNum[letter]+(octave*2)) and (notes[n+14] == noteNum[letter]+octave):
            for p in range(14):
                del notes[n + p]
                break
    for n in range(len(notes)-14):
        if (notes[n] == noteNum[letter]+(octave*2)) and (notes[n+7] ==noteNum[letter]+(octave*3)) and (notes[n+14] == noteNum[letter]+(octave*2)):
            for p in range(14):
                del notes[n + p]
                break


# In[10]:

def getScore(notes):
    score = []
    for key in noteNum:
        score.append(checkScale(notes,key))
    return score


# In[11]:

scoreOutput = []
arpeggioOutput=[]

for f in range(len(files)):
    #get notes
    notes = extractNotes(f)
    
    subject = files[f][-12:-10]
    
    #score scales
    score = getScore(notes)
    errors = sum(s[1] for s in score)
    scoreOutput.append([subject,errors])
    
    #score arpeggios
    score = 0
    for a in ['A','E','B','C','D','G']:
        score = score + checkArpeggio(notes,a)
    arpeggioOutput.append([subject,score])


# In[12]:

with open('scales.csv', 'w+') as f:
    for line in scoreOutput:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[13]:

with open('arpeggio.csv', 'w+') as f:
    for line in arpeggioOutput:
        f.write(str(line[0])+', '+str(line[1])+'\n')

