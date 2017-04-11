files = dir('./MIDIfiles/Scales/MIDI/*.mid');

for i = 1:length(files)
    nmat = readmidi(strcat('./MIDIfiles/Scales/MIDI/',files(i).name));
    csvwrite(strcat('./MIDIfiles/Scales/csv/',files(i).name(1:15),'.csv'),nmat)
end