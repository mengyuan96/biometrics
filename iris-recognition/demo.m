% Processes images and generates distributions, ROC curves and CMC curves.
% Author: Xinda Huang and Shiyu Luo

gallery_entries = create_gallery('2008-03-11_13');
probes1 = create_gallery('LG4000-2010-04-27_29');
probes2 = create_gallery('LG2200-2010-04-27_29');

gallery_map = group(gallery_entries);
probes1_map = group(probes1);
probes2_map = group(probes2);

% generate distribution by comparing probes with gallery
% left_genuine: a list of genuine difference scores of left eyes
% left_imposter: a list of imposter difference scores of left eyes
% right_genuine: a list of genuine difference scores of right eyes
% right_imposter: a list of imposter difference scores of right eyes
[left_genuine1, left_imposter1, right_genuine1, right_imposter1] = generate_distribution(gallery_map, probes1_map);
[left_genuine2, left_imposter2, right_genuine2, right_imposter2] = generate_distribution(gallery_map, probes2_map);

%plot the distribution
left_imposter_1=roundn(left_imposter1(:),-2);
left_genuine_1=roundn(left_genuine1(:),-2);
left_imposter_2=roundn(left_imposter2(:),-2);
left_genuine_2=roundn(left_genuine2(:),-2);

right_genuine_1=roundn(right_genuine1(:),-2);
right_imposter_1=roundn(right_imposter1(:),-2);
right_genuine_2=roundn(right_genuine2(:),-2);
right_imposter_2=roundn(right_imposter2(:),-2);

li1=tabulate(left_imposter_1(:));
lg1=tabulate(left_genuine_1(:));
li2=tabulate(left_imposter_2(:));
lg2=tabulate(left_genuine_2(:));

rg1=tabulate(right_genuine_1(:));
ri1=tabulate(right_imposter_1(:));
rg2=tabulate(right_genuine_2(:));
ri2=tabulate(right_imposter_2(:));

figure
plot(li1(:,1),li1(:,2)/max(li1(:,2)),'red','LineWidth',4)
hold on
plot(lg1(:,1),lg1(:,2)/max(lg1(:,2)),'blue','LineWidth',4)
axis([0,1,0,1])
title('Genuine and Imposter Distributions for Probe 1(left)');
xlabel('Hamming Distance');
ylabel('Frequency');
legend('Imposter','Genuine');

figure
plot(ri1(:,1),ri1(:,2)/max(ri1(:,2)),'red','LineWidth',4)
hold on
plot(rg1(:,1),rg1(:,2)/max(rg1(:,2)),'blue','LineWidth',4)
axis([0,1,0,1])
title('Genuine and Imposter Distributions for Probe 1(right)');
xlabel('Hamming Distance)');
ylabel('Frequency');
legend('Imposter','Genuine');

figure
plot(li2(:,1),li2(:,2)/max(li2(:,2)),'red','LineWidth',4)
hold on
plot(lg2(:,1),lg2(:,2)/max(lg2(:,2)),'blue','LineWidth',4)
axis([0,1,0,1])
title('Genuine and Imposter Distributions for Probe 2(left)');
xlabel('Hamming Distance');
ylabel('Frequency');
legend('Imposter','Genuine');

figure
plot(ri2(:,1),ri2(:,2)/max(ri2(:,2)),'red','LineWidth',4)
hold on
plot(rg2(:,1),rg2(:,2)/max(rg2(:,2)),'blue','LineWidth',4)
axis([0,1,0,1])
title('Genuine and Imposter Distributions for Probe 2(right)');
xlabel('Hamming Distance)');
ylabel('Frequency');
legend('Imposter','Genuine');

% generate ROC curve for probe 1
[fprs1, tprs1] = generate_ROC(gallery_map, probes1_map);
h_roc1 = figure('visible', 'off');
subplot(211);
plot(fprs1, tprs1)
axis([0, 1, 0, 1]);
xlabel('False Match Rate (FMR)');
ylabel('True Match Rate (TMR)');
title('ROC Curve, Probe 1');

% % generate ROC curve for probe 2
[fprs2, tprs2] = generate_ROC(gallery_map, probes1_map);
subplot(212);
plot(fprs2, tprs2)
axis([0, 1, 0, 1]);
xlabel('False Match Rate (FMR)');
ylabel('True Match Rate (TMR)');
title('ROC Curve, Probe 2');

print('roc-curves.png', '-dpng', '-r0')


% plot the CMC curve
rate1=generate_CMC(probes1,gallery_entries,gallery_map);
rate2=generate_CMC(probes2,gallery_entries,gallery_map);
figure
x=1:length(gallery_map);
plot(x,rate1,'r')
axis([1,length(gallery_map),0,1]);
xlabel('Rank Counted As Recognition');
ylabel('Recognition Rate');
title('CMC Curve for Probe 1');
figure
x=1:length(gallery_map);
plot(x,rate2,'r')
axis([1,length(gallery_map),0,1]);
xlabel('Rank Counted As Recognition');
ylabel('Recognition Rate');
title('CMC Curve for Probe 2');


