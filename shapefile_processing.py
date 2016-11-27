import shapefile
from liblas import file
#noinspection PyUnresolvedReferences
import lidar_proocessing
import pyproj
from PIL import Image

#Constants that are importnat for transformation
wgs84 = pyproj.Proj(init='epsg:4326')
northFL = pyproj.Proj(init='esri:102660')
no_matched = 0

def convert_wgs84_to_northFL(lon, lat):
    '''

    Parameters:
      lon:Longitude of a place
      lat:Latitude of a place
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
    '''Creates the image file of particular size'''
    image_f = Image.new(mode='RGB', size=(image_size_x, image_size_y), color=None)
    return image_f

def getlistoflatlong(listoflidardatapoints):
    """This function will return the list of latitude longitude corresponding to all the data points in the lidar file"""
    latlonglist= []
    for i in range(0, len(listoflidardata)):
        latlonglist.append(convert_northFL_to_wgs84(listoflidardatapoints[i].x, listoflidardatapoints[i].y))
    return latlonglist

def getcroppedlistofshapes(shapefile,latlongmax,latlongmin):
    '''This function returns the cropped list of latitude and longitude'''
    croppedlistofshapes =[]
    for shp in sf.iterShapes():
        #print(shp.shapeType)
        if (shp.bbox[0]<=latlongmax[0] and shp.bbox[0]>=latlongmin[0]):
            if (shp.bbox[1]<=latlongmax[1] and shp.bbox[1]>=latlongmin[1]):
                print("Added to the shapefile list",shp.bbox[0],shp.bbox[1])
                croppedlistofshapes.append(shp)
        if (shp.bbox[2]<=latlongmax[0] and shp.bbox[2]>=latlongmin[0]):
            if (shp.bbox[3]<=latlongmax[1] and shp.bbox[3]>=latlongmin[1]):
                print("Added to the shapefile list",shp.bbox[2],shp.bbox[3])
                croppedlistofshapes.append(shp)
    return croppedlistofshapes

def getsetofmatchedlidarpoints(listofcroppedshapes,listoflatlong,listoflidardata):
    '''This function will return a set of datapoints that matches the cropped shapes points'''
    setofmatchedpoints = set()
    no_matched = 0
    for shapes in croppedshapes:
        for p in shapes.points:
            for i in range(len(listoflatlong)):
                if abs(p[0] - listoflatlong[i][0]) < 0.0004 and abs(p[1] - listoflatlong[i][1]) < 0.0004:
                    setofmatchedpoints.add(listoflidardata[i])
                    no_matched = no_matched + 1
    print("no matched:", no_matched)
    print('Length of matched points:', len(setofmatchedpoints))
    return setofmatchedpoints

def colormatcheddatapoints(setoflidaradata,imagefile,maxmincoordinates,imagefileName):
    '''This function will color the matched data points'''
    for p in setoflidaradata:
        imagefile.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
    print('image file name:',imagefileName)
    imagefile.save(imagefileName,format="jpeg")

sf = shapefile.Reader('tl_2016_12073_roads/tl_2016_12073_roads.shp')
lidar_fileName = "las_tile_46138/2035000.25_541249.75_2036250.25_539999.75.las"
lidar_file = lidar_proocessing.getlidardatafile(lidar_fileName)
listoflidardata= lidar_proocessing.getlistoflidardata(lidar_file)
lidarfile_header = lidar_proocessing.getHeaderInformation(lidar_file)
print("No of data points:",len(listoflidardata))
maxmincoordinates = lidar_proocessing.getMaxMinCoordinatesforlidarfile(lidar_file)
image_size_x = maxmincoordinates[1] - maxmincoordinates[0] + 1
image_size_y = maxmincoordinates[3] - maxmincoordinates[2] + 1
imagefile = createImageFile(image_size_x,image_size_y)
listoflatlong = getlistoflatlong(listoflidardata)
maxlatlong = convert_northFL_to_wgs84(lidarfile_header.max[0],lidarfile_header.max[1])
minlatlong = convert_northFL_to_wgs84(lidarfile_header.min[0],lidarfile_header.min[1])
print(maxlatlong)
print(minlatlong)
print("Number of shape file records:",len(list(sf.iterShapes())))
croppedshapes = getcroppedlistofshapes(sf,maxlatlong,minlatlong)
print(len(croppedshapes))
print(croppedshapes[0].bbox)
print(croppedshapes[1].bbox)
setofmatchedlidarpoints=getsetofmatchedlidarpoints(croppedshapes,listoflatlong,listoflidardata)
colormatcheddatapoints(setofmatchedlidarpoints,imagefile,maxmincoordinates,lidar_fileName.replace('/','')[:-4]+'road_image')
lidar_file.close()
