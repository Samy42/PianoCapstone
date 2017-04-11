function [ technicalDifficultyScore ] = ScalesArpeggios( name )
%This function reads in the midi file named "Subject##Scales.mid" where the
%## is the string input for the subject's ID number. It outputs a number
%which is the number of incorrect or missing notes. 
%If a scale is skipped, 15 points are added to the score, one per note
%played.
%A scale is considered to have been played if the first, middle, and last
%notes are correct. These notes are all the same key as the name of the
%scale, with the middle note being an octave up. For example, the C Major
%Scale starts at middle C, goes up to the next C, then back down to middle
%C. If those 3 notes are played with the correct number of notes between
%them, the scale is correct.
%Similarly, for arpeggios, the first, middle, and last notes are the same
%as the name of the arpreggio and therefore it is considered played if
%those are played in the correct place.



nmat = readmidi(strcat('Subject', name , 'Scales.mid'));

% Define custom data type for storing the info on scales
%scaleType.name = 'CmajorScale';
%scaleType.numnotes = 15;
%scaleType.startnote = 60;
%scaletype.sequence = [60,62,64,65,67,69,71,72,71,69,67,65,64,62,60];


% assuming a c scale starts at middle c, goes to next c up, back to C, and
% does it in 15 keys total.

[correctnotes,titles] = xlsread('NoteToNum.xlsx','Scales&Arpeggios');
scaleslength = 15;
arpeggioslength = 7;

c = 1;


score = zeros(18);

while c < 12 %for the 12 scales
    for n = 1:length(nmat)-14
        if(nmat(n,4) == correctnotes(1,c)) 
            if (nmat(n+7,4) == correctnotes(8,c)) 
                if (nmat(n+14,4) == correctnotes(15,c))
                    for k = 1:scaleslength
                        if nmat(n+k-1,4) ~= correctnotes(k,c)
                            score(c) = score(c) + 1;
                        end
                    end
                    c = c + 1;
                    
                    
                    if c > 12
                        break
                    end
                end
            end
        end
    end 
    c = c + 1; %this fixes issues where a scale was skipped
    score(c) = scaleslength;
end


while c < 18 %for the 6 arpeggios
    for n = 1:length(nmat)-6
        if(nmat(n,4) == correctnotes(1,c)) 
            if (nmat(n+3,4) == correctnotes(4,c)) 
                if (nmat(n+6,4) == correctnotes(7,c))
                    for k = 1:arpeggioslength
                        if nmat(n+k-1,4) ~= correctnotes(k,c)
                            score(c) = score(c) + 1;
                        end
                    end
                    c = c + 1;
                    if c > 18
                        break
                    end

                end
            end
        end
    end 
    c = c + 1; %this fixes issues where a chord was skipped
    score(c) = arpeggioslength;
end


technicalDifficultyScore = sum(sum(score));

end

