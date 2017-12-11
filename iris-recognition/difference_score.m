% Computes the difference score of the specified probe subject and gallery subject.
% Attributes:
%	<probe_subject>: A structure array (with fields 'id', 'template', 'mask', 'eye', and 'image')
%					that contains left/right eyes information of a same probe subject.
%	<gallery_subject>: A structure array (as specified above) that contains left/right(same as above)
%					information of a same gallery subject.
% Returns: 
%	<score>: the difference score
%
% Author: Shiyu Luo

function score = difference_score(probe_subject, gallery_subject)
M = length(probe_subject);
N = length(gallery_subject);
dist = 0;

count_nan = 0;
% iterate over all (probe_subject, gallery_subject) pairs and computes the
% total distance
for m = 1 : M
    for n = 1 : N
        hd = gethammingdistance(probe_subject(m).template, probe_subject(m).mask, gallery_subject(n).template, gallery_subject(n).mask, 1);
        if ~isnan(hd)
            dist = dist + hd;
        else
            count_nan = count_nan + 1;
        end
    end
end

% averaging distance
score = dist / (M * N - count_nan);
end
     
        