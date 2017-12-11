% create_gallery - generate a gallery based on the specified fpath.
% can be used to generate a gallery of enrolled users,
% or to a 'gallery' of probes
% fpath should be one of:
% - '2008-03-11_13'
% - 'LG2200-2010-04-27_29'
% - 'LG4000-2010-04-27_29'
%
% Author: Shiyu Luo

function gallery_entry = create_gallery(fpath)
% disable warnings
warning('off','all')

% dummy gallery entry
gallery_entry = struct('id', 00000, 'eye', 'Right', 'image', 'default', 'template', zeros(10), 'mask', ones(10));
counter = 1;

% add directory containing iris recognition funtions to research path
% If 'undefined function createiristemplate' is thrown
% change this to its absolute directory
addpath('irisrecog_functions');

cd(fpath);
gallery_image_dir = dir;

% error messages stored here
errorfilename = strcat('../error-messages-', fpath, '.txt');
fid = fopen(errorfilename, 'w');
fclose(fid);
% log
logfilename = strcat('../log-', fpath, '.txt');
fid = fopen(logfilename, 'w');
fclose(fid);


% For Linux, uncomment line 39, and comment out line 40
% For OS X, if there is no .DS_Store file in the folder, uncomment line 39, and comment out line 40
%for i = 3:(length(gallery_image_dir))
for i = 4:(length(gallery_image_dir)) 
    current_subject_path = gallery_image_dir(i).name; 
    fid = fopen(logfilename, 'at');
    fprintf(fid, 'subfolder %s\n', current_subject_path);
    fclose(fid);
    cd(current_subject_path); 
    current_subject_files = dir;
    mkdir('diagnostics');
    
    
    % find .txt
    for j = 3:length(current_subject_files)
        if isempty(strfind(current_subject_files(j).name, 'log'))...
                && isempty(strfind(current_subject_files(j).name, 'error'))...
                && ~isempty(strfind(current_subject_files(j).name, '.txt'))
            current_txt_file_path = current_subject_files(j).name;
            break;
        end
    end
    
    txt = fopen(current_txt_file_path);
    assert(txt > 0);
    % find subject id
    % map sequenceid to eye
    map = containers.Map;
    subject_id = 0;
    foundID = false;
    line = fgetl(txt);
    while ~foundID && ischar(line)
        if ~isempty(strfind(line, 'subjectid'))
            subject_id = strsplit(line);
            subject_id = subject_id(3);
            subject_id = subject_id{1};
            foundID = true;
        end
        line = fgetl(txt);
    end
    fclose(txt);
    
    txt = fopen(current_txt_file_path);
    assert(txt > 0);
    line = fgetl(txt);
    while ischar(line)
        if ~isempty(strfind(line, 'sequenceid'))
            % find sequence id
            sequenceid = strsplit(line);
            sequenceid = sequenceid(3);
            sequenceid = sequenceid{1};
            % skip lines
            for n = 1:3
                fgets(txt);
            end
            % fetch eye
            line = fgetl(txt);
            eye = strsplit(line);
            eye = eye(3);
            eye = eye{1};
            map(sequenceid) = eye;
            
            logfile = strcat('../', logfilename);
            fid = fopen(logfile, 'at');
            fprintf(fid, 'sequenceid %s, eye %s\n', sequenceid, eye);
            fclose(fid);
            
        end
        % jump to next line
        line = fgetl(txt);
    end
    % fprintf('found sequence id and eye');
    fclose(txt);
    
    % process .tiff
    for k = 3:length(current_subject_files)
        if ~isempty(strfind(current_subject_files(k).name, current_subject_path))...
            && ~isempty(strfind(current_subject_files(k).name, '.tiff'))...
            && isempty(strfind(current_subject_files(k).name, '.mat'))
            current_tiff_name = current_subject_files(k).name;
            % create gallery entry
            try
                [gallery_entry(counter).template, gallery_entry(counter).mask] = createiristemplate(current_tiff_name);
                gallery_entry(counter).id = subject_id;
                gallery_entry(counter).image = current_tiff_name;
                curr_tiff_sequenceid = current_tiff_name(1:length(current_tiff_name) - 5);
                gallery_entry(counter).eye = map(curr_tiff_sequenceid);
                logfile = strcat('../', logfilename);
                fid = fopen(logfile, 'at');
                fprintf(fid, 'entry %d, image %s, sequenceid %s, eye %s\n', counter, current_tiff_name, curr_tiff_sequenceid, gallery_entry(counter).eye);
                fclose(fid);
                counter = counter + 1;
            catch
                errfile = strcat('../', errorfilename);
                fid = fopen(errfile, 'at');
                fprintf(fid, 'subfolder %s, image %s\n', current_subject_path,  current_tiff_name);
                fclose(fid);
            end
        end
    end
    
    cd('..')
    fprintf('%d subfolders done\n', i - 3)
end
cd('..')
end


            
                    
                
            
            
            
            
            
    
    
    
        
    

