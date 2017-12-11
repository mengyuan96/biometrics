% Generates genuine and imposter distributions based on iris data in path1, path2.
% Attributes:
%   <path1>: path of gallery iris images
%   <path2>: path of probe iris images
% Returns:
%   <left_genuine>: an array of difference scores computed by comparing
%              images in path1 and path2 of left eyes of same subjects
%   <left_imposter>: an array of difference scores computed by comparing
%              images in path1 and path2 of left eyes of different subjects
%   <right_genuine>: an array of difference scores computed by comparing
%              images in path1 and path2 of right eyes of same subjects
%   <right_imposter>: an array of difference scores computed by comparing
%              images in path1 and path2 of right eyes of different subjects
%
% Author: Shiyu Luo

function [left_genuine, left_imposter, right_genuine, right_imposter] = generate_distribution(gallery_map, probe_map)


left_genuine = [];
left_imposter = [];
right_genuine = [];
right_imposter = [];

probeids = keys(probe_map);
galleryids = keys(gallery_map);

for i = 1:length(probeids)
    for j = 1:length(galleryids) 
        % iterate over all possible (probe subject, gallery subject) combinations
        probeid = probeids(i);
        probeid = probeid{1};
        galleryid = galleryids(j);
        galleryid = galleryid{1};
        gallery_subject = gallery_map(galleryid);
        probe_subject = probe_map(probeid);
        
        % compute scores of this (probe subject, gallery subject) pair
        % left eye score
        left_score = difference_score(probe_subject('Left'), gallery_subject('Left'));
        % right eye score
        right_score = difference_score(probe_subject('Right'), gallery_subject('Right'));
        
        % genuine or imposter?
        if ~isnan(left_score)
            if strcmp(probeid, galleryid)
                left_genuine = [left_genuine, left_score];
            else
                left_imposter = [left_imposter,left_score];
            end
        end
        
        if ~isnan(right_score)
            if strcmp(probeid, galleryid)
                right_genuine = [right_genuine, right_score];
            else
                right_imposter = [right_imposter, right_score];
            end
        end
    end
end
end

