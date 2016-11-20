from liblas import file
from PIL import Image


def getMaxMinCoordinates(lidarfile):
    max_x = -1
    min_x = 10000000000000
    max_y = -1
    min_y = 1000000000000
    for p in lidarfile:
        if p.x > max_x:
            max_x = int(p.x)
        if p.x < min_x:
            min_x = int(p.x)
        if p.y > max_y:
            max_y = int(p.y)
        if p.y < min_y:
            min_y = int(p.y)
    return min_x, max_x, min_y, max_y

def getMaxMinCoordinatesforlidarfile(lidarfile):
    max_x = -1
    min_x = 10000000000000
    max_y = -1
    min_y = 1000000000000
    lidarfile.seek(0)
    for p in lidarfile:
        if p.x > max_x:
            max_x = int(p.x)
        if p.x < min_x:
            min_x = int(p.x)
        if p.y > max_y:
            max_y = int(p.y)
        if p.y < min_y:
            min_y = int(p.y)
    return min_x, max_x, min_y, max_y


def createImageFile(lidarfile, filename,image_size_x,image_size_y, maxmincoordinates):
    i = Image.new(mode='RGB', size=(image_size_x,image_size_y), color=None)
    for p in f:
        i.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
    i.save(filename, format="JPEG")

def getlistoflidardata(lidarfile):
    listOfLidardata=[]
    for p in lidarfile:
        listOfLidardata.append(p)
    return listOfLidardata

def getlidardatafile(lidar_fileName):
    f = file.File(lidar_fileName, mode='r')
    return f

def createImageforregion(lidarfile,maxmincoordinates,imagefile):
    status = input('"Do you waant to create image for a particular region of lidar file? Enter Y/Yes or N/No')
    status=status.upper()
    if status =='Y' or status =='YES':
        print("min x coordinate:",maxmincoordinates[0],"max x coordinate",maxmincoordinates[1],"min y coordinate",maxmincoordinates[2],"max y coordinate",maxmincoordinates[3])
        upper_x=  int(input("Give the x coordinate of the uppermost left point in the diagonal"))
        upper_y=int(input("Give the y coordinate of the uppermost top point in the diagonal"))
        lower_x= int(input('Give the x coordinate of the lowermost right point in the diagonal'))
        lower_y= int(input("Give the y coordinate of the lowermost right point in the diagonal"))
        i = Image.new(mode='RGB',size=(lower_x-upper_x+1,lower_y-upper_y+1),color=None)
        for p in lidarfile:
            if int(p.x)>=upper_x and int(p.x)<=lower_x and int(p.y)>=upper_y and int(p.y)<=lower_y:
                i.putpixel((int(p.x)-upper_x,int(p.y)-upper_y),(p.color.red,p.color.green,p.color.blue))
        i.save(imagefile,format="JPEG")
    else:
        print("Exiting the application")

def printHeaderInformation(lidarfile):
    header = lidarfile.header
    print("Major Version:",header.major_version,", Minor Version:",header.minor_version)
    print("Data format id:",header.data_format_id)
    print("Header offset:",header.offset)
    print("Header max:",header.max)
    print("Header min:",header.min)
    print("sr.proj4",header.srs.proj4)
    print("srs.proj4.getproj4",header.srs.get_proj4())



if __name__=="__main__" :
    lidar_fileName = "las_tile_46138/2035000.25_541249.75_2036250.25_539999.75.las"
    #lidar_fileName = 'LAS12_Sample_withRGB_Quick_Terrain_Modeler_fixed.las.part'
    #lidar_fileName = '/home/kunal/Downloads/LAS12_Sample_withRGB_Quick_Terrain_Modeler_fixed.las.part'
    image_fileName = "lidar_image"
    #image_fileName = "/home/kunal/lidar_image"
    image_fileregion='lidar_image_rectangle'
    #image_fileregion='/home/kunal/lidar_image_rectangle'
    f = file.File(lidar_fileName, mode='r')
    printHeaderInformation(f)
    maxmincoordinates = getMaxMinCoordinates(f)
    f.seek(0)
    image_size_x = maxmincoordinates[1]-maxmincoordinates[0]+1
    image_size_y= maxmincoordinates[3]-maxmincoordinates[2]+1
    createImageFile(f, image_fileName,image_size_x,image_size_y, maxmincoordinates)
    f.seek(0)
    createImageforregion(f,maxmincoordinates,image_fileregion)










# header = f.header
# print(header.major_version,header.minor_version)
# print(header.data_format_id)
# print(header.offset)
# print(header.point_records_count)
# print(header.max)
"""
max_x=-1
min_x=10000000000000
max_y = -1
min_y=1000000000000

for p in f:
    if p.x>max_x:
        max_x = int(p.x)
    if p.x<min_x:
        min_x=int(p.x)
    if p.y>max_y:
        max_y=int(p.y)
    if p.y<min_y:
        min_y=int(p.y)

print("Min x co-ordinate",min_x)
print("Max x co-ordinate",max_x)
print("Min y co-ordinate",min_y)
print("Max y co-ordinate",max_y)

#p= f.read(0)
#print(p.x,p.y,p.z,p.color.red,p.color.green,p.color.blue)
count = 0
i=Image.new(mode='RGB',size=(1000,1000),color=None)
index =0

for p in f:
   #print('X={0} Y={1} Z={2} Red={3} Green={4} Blue={5}'.format(p.x,p.y,p.z,p.color.red,p.color.green,p.color.blue))
   i.putpixel((count,index),(p.color.red,p.color.green,p.color.blue))
   #count=count+1
   index = index + 1
   if index == 100:
       index = 0
       count = count +1
   if count>99:
       break
   #c = p.color
   #print(c.red)
   #print(c.blue)
   #print(c.green)
   #count =count +1
i.save('/home/kunal/lidar_image',format="JPEG")
#print(count)
"""
