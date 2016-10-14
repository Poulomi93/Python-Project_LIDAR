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


def createImageFile(lidarfile, filename, maxmincoordinates):
    i = Image.new(mode='RGB', size=(
    maxmincoordinates[1] - maxmincoordinates[0] + 1, maxmincoordinates[3] - maxmincoordinates[2] + 1), color=None)
    for p in f:
        i.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
    i.save(filename, format="JPEG")


lidar_fileName = '/home/kunal/Downloads/LAS12_Sample_withRGB_Quick_Terrain_Modeler_fixed.las.part'
image_fileName = "/home/kunal/lidar_image"

f = file.File(lidar_fileName, mode='r')
maxmincoordinates = getMaxMinCoordinates(f)
f.seek(0)
createImageFile(f, image_fileName, maxmincoordinates)
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
