
# coding: utf-8

# In[1]:

import pandas
from glob import glob


# In[2]:

def extractNotes(file):
    df = pandas.read_csv(files[file], header = None , names=['Onset (Beats)','Duration (Beats)','MIDI Channel','MIDI Pitch','Velocity','Onset (Sec)','Duration (sec)'])
    
    
    notes = df['MIDI Pitch'].tolist()
    beats = df['Duration (Beats)'].tolist()
    roundedBeats = []
    
    if file > 0:
        for i in range(len(beats)):
            roundedBeats.append(min(enumerate(set(correctNotes[1])), key=lambda x: abs(x[1]-beats[i]))[1])
    else:
        roundedBeats = beats.copy()
    
    return [notes, roundedBeats]


# In[3]:

def roundBeats(beats):
    roundedBeats = []
    
    if type(beats) is list:
        for i in range(len(beats)):
            roundedBeats.append(min(enumerate(set(correctNotes[1])), key=lambda x: abs(x[1]-beats[i]))[1])
    else:
        roundedBeats = (min(enumerate(set(correctNotes[1])), key=lambda x: abs(x[1]-beats))[1])
        
    return roundedBeats


# In[4]:

def checkPiece(correct, notes):
    

    iterlist = correct.copy()

    same = 0
    for i in iterlist:
        if i in notes:
            notes.remove(i)
            correct.remove(i)
            same = same + 1


    return [[same, len(notes), len(correct)],notes,correct]


# In[5]:

def mushNotes(notes):
    new = []
    for i in range(len(notes[0])):
        new.append([notes[0][i],notes[1][i]])
        
    return new


# In[6]:

def scoreSubject(subject):
    correct = mushNotes(correctNotes)
    notes = mushNotes(extractNotes(subject))

    output = []
    output.append(checkPiece(correct,notes))

    beatCounts = set(correctNotes[1])

    for i in range(len(beatCounts)):

        if output[i][0][1] == 0:
            break

        for n in range(len(output[i][1])):
            output[i][1][n][1]= roundBeats(output[i][1][n][1] + (min(beatCounts)*pow(2,i)))

        output.append(checkPiece(output[i][1],output[i][2]))



    #calculate overall score, taking off half credit recursively for every adjustment to get all notes
    score = 0

    for i in range(len(output)):
        score = score + (output[i][0][0]*pow(2,(-1*i)))
    
    
    return score


# In[7]:

#Amazing Grace

files = glob('./MIDIfiles/AmazingGrace/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('amazingGrace.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[ ]:

#Clavier

files = glob('./MIDIfiles/Clavier/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('clavier.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[ ]:

#Nocturne

files = glob('./MIDIfiles/Nocturne/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('nocturne.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[ ]:

#Opus

files = glob('./MIDIfiles/Opus/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('opus.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[ ]:

#Sonata

files = glob('./MIDIfiles/Sonata/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('sonata.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')


# In[ ]:

#Traumerei

files = glob('./MIDIfiles/Traumerei/csv/*.csv')

correctNotes = extractNotes(0)

output = []
for f in range(len(files)-1):
    subject = files[f+1][-18:-16]
    output.append([subject, scoreSubject(f+1)])

with open('traumerei.csv', 'w+') as f:
    for line in output:
        f.write(str(line[0])+', '+str(line[1])+'\n')

