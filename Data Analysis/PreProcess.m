% Eye Tracking

if count(py.sys.path,'') == 0
    insert(py.sys.path,int32(0),'');
end

fprintf('start Eye Tracking')
commandStr = 'python "EyeTracking.py"';
 [status, commandOut] = system(commandStr);
 if status==0
     fprintf('it worked!');
 end
 if status ~= 0
     fprintf('you suck')
 end

 
 %Scales
 
 fprintf(' start Scales')

 
 files = dir('./MIDIfiles/Scales/MIDI/*.mid');
i = 0;
for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Scales/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Scales/csv/',files(i).name(1:15),'.csv'),nmat)
end

commandStr = 'python "Scales.py"';
 [status, commandOut] = system(commandStr);
 if status==0
     fprintf('it worked!');
 end
 if status ~= 0
     fprintf('you suck')
 end
 
 
 %Pieces
 
 fprintf(' start Pieces')

 i = 0;
 files = dir('./MIDIfiles/AmazingGrace/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/AmazingGrace/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/AmazingGrace/csv/',files(i).name(1:21),'.csv'),nmat)
end


i = 0;
files = dir('./MIDIfiles/Clavier/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Clavier/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Clavier/csv/',files(i).name(1:16),'.csv'),nmat)
end


i = 0;
files = dir('./MIDIfiles/Nocturne/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Nocturne/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Nocturne/csv/',files(i).name(1:17),'.csv'),nmat)
end


i = 0;
files = dir('./MIDIfiles/Opus/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Opus/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Opus/csv/',files(i).name(1:13),'.csv'),nmat)
end


i = 0;
files = dir('./MIDIfiles/Sonata/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Sonata/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Sonata/csv/',files(i).name(1:15),'.csv'),nmat)
end


i = 0;
files = dir('./MIDIfiles/Traumerei/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Traumerei/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Traumerei/csv/',files(i).name(1:18),'.csv'),nmat)
end



if count(py.sys.path,'') == 0
    insert(py.sys.path,int32(0),'');
end

fprintf('start')
commandStr = 'python "Pieces.py"';
 [status, commandOut] = system(commandStr);
 if status==0
     fprintf('it worked!');
 end
 if status ~= 0
     fprintf('you suck')
 end
 
 fprintf(' All Done!!!')