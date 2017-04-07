%% Generate Ture location
%% picture name list to be marked
filelist = fopen('testlist.txt');
tline = fgetl(filelist);
%% txt file to save marked groundtruth
filegt = fopen('testgt.txt','a+');
%% picture of classes to make marking work easier
%classpic=imread('classes.bmp');

%% when need to skip some picture, in case where we stop at some place
skipnum = 0;
count = 0;
while count<skipnum
    tline = fgetl(filelist);
    count = count + 1;
end
%% process
type = {'cat','dog','aeroplane','people'};
[ty,typenum] = size(type);
while ischar(tline)
        path = strcat('D:\SSD_data\testpic\',tline);% replace with your own path
        %path = tline;
        I = imread(path);
        [m n] = size(rgb2gray(I)); 
        classpic = [];
        black = uint8(zeros(40,100,3));
        white = black + 255;
        black = black + 180;
        for i=1:typenum
            if mod(i,2)==0
                classpic = [classpic black];
            else
                classpic = [classpic white];
            end                
        end
        classpic = imresize(classpic,[40,n]);
        I = [I;classpic];
        imshow(I);
        for i = 1:typenum
            text((i-0.5)*n/typenum,m+20,type{i},'horiz','center','color','r','fontsize',15);
        end
        for i = 1:20
            h = imrect;
            pos = uint16(getPosition(h));
            if pos(3)>8*pos(4) %when width is more than 8 times of the height, stop and turn to the next image
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
            [x0,y0] = ginput(1);% get the click position
            k = ceil(x0/(n/typenum));
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