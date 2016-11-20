import shapefile
from liblas import file
#noinspection PyUnresolvedReferences
import lidar_proocessing
import pyproj
from PIL import Image

wgs84 = pyproj.Proj(init='epsg:4326')
northFL = pyproj.Proj(init='esri:102660')
no_matched = 0

def convert_wgs84_to_northFL(lon, lat):
    '''
    '''
    x, y = pyproj.transform(wgs84, northFL, lon, lat)
    return x / 0.3048, y / 0.3048

def convert_northFL_to_wgs84(easting, northing):
    '''

    Parameters:
        easting: in feet
        northing: in feet
    '''
    return pyproj.transform(northFL, wgs84,
                            easting * 0.3048, northing * 0.3048)

def createImageFile(image_size_x,image_size_y):
    image_f = Image.new(mode='RGB', size=(image_size_x, image_size_y), color=None)
    return image_f

sf = shapefile.Reader('tl_2016_12073_roads/tl_2016_12073_roads.shp')
lidar_fileName = "las_tile_46138/2035000.25_541249.75_2036250.25_539999.75.las"
lidar_file = lidar_proocessing.getlidardatafile(lidar_fileName)
listoflidardata= lidar_proocessing.getlistoflidardata(lidar_file)
print("No of data points:",len(listoflidardata))
maxmincoordinates = lidar_proocessing.getMaxMinCoordinates(lidar_file)
image_size_x = maxmincoordinates[1] - maxmincoordinates[0] + 1
image_size_y = maxmincoordinates[3] - maxmincoordinates[2] + 1
imagefile = createImageFile(image_size_x,image_size_y)
#print(maxmincoordinates[0],',',maxmincoordinates[1],',',maxmincoordinates[2],',',maxmincoordinates[3])
listoflatlong = []
for i in range(0,len(listoflidardata)):
    listoflatlong.append(convert_northFL_to_wgs84(listoflidardata[i].x, listoflidardata[i].y))
#for p in listoflidardata:
#    listoflatlong.append(convert_northFL_to_wgs84(p.x,p.y))

#for p in listoflatlong:
    #print(p)
#    pass
for shp in sf.iterShapes():
    for i in range(0,len(listoflatlong)):
        if (shp.bbox[0]<=listoflatlong[i][0] and listoflatlong[i][0]<=shp.bbox[2]):
            if (shp.bbox[1]<=listoflatlong[i][1] and listoflatlong[i][1]<=shp.bbox[3]):
                #print('matched')
                imagefile.putpixel((int(listoflidardata[i].x) - maxmincoordinates[0], int(listoflidardata[i].y) - maxmincoordinates[2]),
                           (listoflidardata[i].color.red, listoflidardata[i].color.green, listoflidardata[i].color.blue))
                no_matched = no_matched+1

#for shp in sf.iterShapes():
#    for p in shp.points:
#        for i in range(0,len(listoflatlong)):
#           print(round(p[0],2),round(p[1],2),round(listoflatlong[i][0],2),round(listoflatlong[i][1],2))
#           if round(p[0],2)==round(listoflatlong[i][0],2) and round(p[1],2)== round(listoflatlong[i][1],2):
#               print('matched')
#               imagefile.putpixel((int(listoflidardata[i].x) - maxmincoordinates[0], int(listoflidardata[i].y) - maxmincoordinates[2]),
#                                  (listoflidardata[i].color.red, listoflidardata[i].color.green, listoflidardata[i].color.blue))
#               no_matched = no_matched+1

#for shp in sf.iterShapes():
    #print("bbox:",shp.bbox)
#    for p in listoflatlong:
#        if (shp.bbox[0]<=p[0] and p[0]<=shp.bbox[2]):
#            if (shp.bbox[1]<=p[1] and p[1]<=shp.bbox[3]):
#                print('matched')
#                no_matched = no_matched+1
imagefile.save("road_image", format="JPEG")
print("No of data points matched",no_matched)

#print(listoflidardata)
#shapes = sf.shapes()
#print(len(shapes))
#for shp in sf.iterShapes():
    #print("Shape Type: ",shp.shapeType, "bbox: ",shp.bbox,"parts: ",shp.parts ,"points: ", shp.points)
#    for p in shp.points:
        #print(p[0],p[1])
#        x , y =convert_wgs84_to_northFL(p[1],p[0])
        #print('Trying to check x,:',int(x),'y:',int(y))
#        for lidarpoint in listoflidardata:
#            if int(lidarpoint.x) == int(x)  and int(lidarpoint.y) == int(y):
#                print('Matched')
#                no_matched = no_matched+1

#print(no_matched)
