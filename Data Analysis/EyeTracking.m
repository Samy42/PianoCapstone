if count(py.sys.path,'') == 0
    insert(py.sys.path,int32(0),'');
end

fprintf('start')
commandStr = 'python "ScalesArpeggios.py"';
 [status, commandOut] = system(commandStr);
 if status==0
     fprintf('it worked!');
 end
 if status ~= 0
     fprintf('you suck')
 end
 name='01';
 nmat = readmidi(strcat('Subject', name , 'Scales.mid'));
 notes = transpose(nmat(:,4));
 a = py.ScalesArpeggios.scales(py.list(notes))
 
 
 listing = dir('./MIDIfiles/Scales/MIDI')
 