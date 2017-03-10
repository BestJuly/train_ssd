%% Generate Ture location
%% picture name list to be marked
filelist = fopen('testlist.txt');
tline = fgetl(filelist);
%% txt file to save marked groundtruth
filegt = fopen('testgt.txt','a+');
%% picture of classes to make marking work easier
classpic=imread('classes.bmp');

%% when need to skip some picture, in case where we stop at some place
skipnum = 0;
count = 0;
while count<skipnum
    tline = fgetl(filelist);
    count = count + 1;
end
%% process
type = {'van','car','suv','bus','keche','huoche','breadcar','othercar','moto','people','tricycle','bicycle','e-bike'};
while ischar(tline)
        path = strcat('D:\SSD_data\testpic\',tline);% replace with your own path
        I = imread(path);
        [m n] = size(rgb2gray(I));  
        classpic = imresize(classpic,[60,n]);
        I = [I;classpic];
        imshow(I);
        for i = 1:20
            h = imrect;
            pos = uint16(getPosition(h));
            if pos(3)>8*pos(4) %当宽远大于高时，标志操作已完成
                i = i - 1;
                break;
            end
            u1 = pos(1);u2 = pos(1)+pos(3);v1 = pos(2); v2 = pos(2)+pos(4);
            if u1 < 1
                u1 = 1;
            end
            if v1 < 1
                v1 = 1;
            end
            if u2 > n;
                u2 = n;
            end
            if v2 > m
                v2 = m;
            end
            [x0,y0] = ginput(1);%获取鼠标点击的位置
            k = ceil(x0/(n/13));
            %fprintf(filegt,'%s %s %d %d %d %d\n',tline,type{k},u1,v1,u2,v2);
            fprintf(filegt,'%s,%d,%d,%d,%d,%s\n',tline,u1,v1,u2,v2,type{k});
        end
    %fprintf(filegt,'\n');
    tline = fgetl(filelist);
    disp(count);
    count = count + 1;
end
fclose(filelist);
fclose(filegt);
