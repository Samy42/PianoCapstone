if count(py.sys.path,'') == 0
    insert(py.sys.path,int32(0),'');
end

fprintf('start')
commandStr = 'python "EyeTracking.py"';
 [status, commandOut] = system(commandStr);
 if status==0
     fprintf('it worked!');
 end
 if status ~= 0
     fprintf('you suck')
 end

 