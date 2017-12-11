% Mapping subject ID to related gallery entries.
% Attribute:
%   <gallery_entries>: a structure array returned by function create_gallery(fpath).
%
% For example, id_entries_map('nd1S05033') = eye_entries_map
% eye_entries_map('Left') = all entries in gallery_entries that 1) are
% associated with id 'nd1S05033', and 2) contain left eye images, templates
% and masks.
%
% Note that keys for both id_entries_map and eye_entries_map are strings.
% Valid keys for id_entries_map are subject ids indicated by .txt files
% under each subfolder. Valid keys for eye_entries_map are: 'Left' and
% 'Right'.
%
% Author: Shiyu Luo

function id_entries_map = group(gallery_entries)
id_entries_map = containers.Map;

num_entries = length(gallery_entries);
for i = 1:num_entries
    curr_entry = gallery_entries(i);
    curr_id = curr_entry.id;
    curr_eye = curr_entry.eye;
    
    % if curr_id is not in id_entries_map,
    % create a new pair with key = curr_id,
    % value = a map mapping eye to entries
    if ~isKey(id_entries_map, curr_id)
        eye_entries_map = containers.Map({'Left', 'Right'}, {[], []});
        id_entries_map(curr_id) = eye_entries_map;
    end
    
    eye_entries_map = id_entries_map(curr_id);
    value = eye_entries_map(curr_eye);
    value = [value, curr_entry];
    eye_entries_map(curr_eye) = value;
    id_entries_map(curr_id) = eye_entries_map;
end      
end
        
    
