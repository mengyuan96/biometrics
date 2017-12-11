function rate=generate_CMC(probe,gallery,gallery_map)
%%%%%%%%%%%%%%%%create close set%%%%%%%%%%%%%%%%
galleryids=keys(gallery_map);
count=1;
probe_close=[];
for i=1:length(probe)
    for j = 1:length(gallery)
        if strcmp(num2str(probe(i).id),num2str(gallery(j).id))
            probe_close=[probe_close,probe(i)];
            count=count+1;
        end
    end
end

%%%%%%%%%%%%%%%%calculate score%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
probe_close_map = group(probe_close);
probecloseids=keys(probe_close_map);

distance=zeros(length(probecloseids),length(galleryids));
for m = 1:length(probecloseids)
    for n = 1:length(galleryids) 
        probecloseid = probecloseids(m);
        probecloseid = probecloseid{1};
        galleryid = galleryids(n);
        galleryid = galleryid{1};
        gallery_subject = gallery_map(galleryid);
        probe_close_subject = probe_close_map(probecloseid);
        leftscore = difference_score(probe_close_subject('Left'), gallery_subject('Left'));
        rightscore = difference_score(probe_close_subject('Right'), gallery_subject('Right'));
        distance(m,n)=(leftscore+rightscore)/2;
     end
end

%%%%%%%%%%%%%%%%%%%%%%% sorting%%%%%%%%%%%%%%%%%%%%%%%%%%%%
rank=[];
for k = 1:length(probecloseids)
    rankinfo = distance(k,:);
    [~,position] = sort(rankinfo,'ascend');
    for i = 1:length(galleryids) 
        if strcmp(probecloseids(k),galleryids(position(i)))
            rank(k)=i;
            break;
            
        end
    end
end
rate=zeros(1,length(galleryids));
for i =1:length(galleryids)
    count1=0;
    for j = 1:length(probecloseids)
        if rank(j) <= i
            count1=1+count1 ;   
        end
    end
    rate(i)=double(count1/length(probecloseids));
end


end