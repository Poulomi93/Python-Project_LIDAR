import shapefile
from liblas import file
#noinspection PyUnresolvedReferences
import lidar_proocessing
import pyproj
from PIL import Image, ImageDraw
import math
from numpy import ones,vstack
from numpy.linalg import lstsq

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

def createImageFile(image_size_x, image_size_y):
    '''Creates the image file of particular size'''
    image_f = Image.new(mode='RGB', size=(image_size_x, image_size_y), color = None)
    return image_f

def getlistoflatlong(listoflidardatapoints):
    """This function will return the list of latitude longitude corresponding to all the data points in the lidar file"""
    latlonglist= []
    for i in range(0, len(listoflidardata)):
        latlonglist.append(convert_northFL_to_wgs84(listoflidardatapoints[i].x, listoflidardatapoints[i].y))
    return latlonglist

def getcroppedlistofshapes(shapefile, latlongmax, latlongmin):
    '''This function returns the cropped list of latitude and longitude'''
    croppedlistofshapes =[]
    for shp in sf.iterShapes():
        #print(shp.shapeType)
        if (shp.bbox[0] <= latlongmax[0] and shp.bbox[0] >= latlongmin[0]):
            if (shp.bbox[1] <= latlongmax[1] and shp.bbox[1] >= latlongmin[1]):
                print("Added to the shapefile list", shp.bbox[0], shp.bbox[1])
                croppedlistofshapes.append(shp)
        if (shp.bbox[2] <= latlongmax[0] and shp.bbox[2] >= latlongmin[0]):
            if (shp.bbox[3] <= latlongmax[1] and shp.bbox[3] >= latlongmin[1]):
                print("Added to the shapefile list", shp.bbox[2], shp.bbox[3])
                croppedlistofshapes.append(shp)
    return croppedlistofshapes

def getcroppedlistofshapes(shapefile, latlongmax, latlongmin):
    '''This function returns the cropped list of latitude and longitude'''
    croppedlistofshapes =[]
    print('Calling the modified cropped list function')
    for shp in sf.iterShapes():
        for p in shp.points:
            if p[0]<=latlongmax[0] and p[0]>=latlongmin[0]:
                if p[1] <= latlongmax[1] and p[1]>latlongmin[1]:
                    print("Added to the shape file list")
                    croppedlistofshapes.append(shp)
                    break
    return croppedlistofshapes

def getsetofmatchedlidarpoints(listofcroppedshapes,listoflatlong,listoflidardata):
    '''This function will return a set of datapoints that matches the cropped shapes points'''
    setofmatchedpoints = set()
    no_matched = 0
    for shapes in croppedshapes:
        for p in shapes.points:
            for i in range(len(listoflatlong)):
                if abs(p[0] - listoflatlong[i][0]) < 0.0001 and abs(p[1] - listoflatlong[i][1]) < 0.0001:
                    setofmatchedpoints.add(listoflidardata[i])
                    no_matched = no_matched + 1
    print("no matched:", no_matched)
    print('Length of matched points:', len(setofmatchedpoints))
    return setofmatchedpoints

def printlistofmatchedpoints(listoflistofpoints,listoflidardata):
    for listofpoints in listoflistofpoints:
        for point in listofpoints:
            no_matches = 0
            for i in range(len(listoflatlong)):
                if (abs(point[0]-listoflatlong[i][0])< 0.0000001 and abs(point[1]-listoflatlong[i][1] < 0.0000001)):
                    #print(point)
                    no_matches = no_matches +1
            print('No  matches for a point:',no_matches)

def colormatcheddatapoints(setoflidaradata,imagefile,maxmincoordinates,imagefileName):
    '''This function will color the matched data points'''
    for p in setoflidaradata:
        imagefile.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
    print('image file name:',imagefileName)
    imagefile.save(imagefileName,format="jpeg")

def getlistofpoints(listofCroppedPoints, latlongmax,latlongmin):
    no_matches = 0
    listoflistofpoints = []
    for shapes in croppedshapes:
        no_matches = 0
        listofpoints = []
        for p in shapes.points:
            if (p[0] <= latlongmax[0] and p[0] >= latlongmin[0]):
                if (p[1] <= latlongmax[1] and p[1] >= latlongmin[1]):
                    no_matches = no_matches +1
                    listofpoints.append(p)
                else:
                    no_matches = no_matches+1
                    listofpoints.append(p)
                    #break
            else:
                no_matches = no_matches+1
                listofpoints.append(p)
                #break
        listoflistofpoints.append(listofpoints)
    print(listoflistofpoints)
    return listoflistofpoints

def drawlinesinimage(width,height,listoflistofpoints,maxmincoordinates):
    #base = Image.open('lidarimage').convert('RGBA')
    #im = Image.new('RGBA',(width, height),(0,255, 0,0))
    im = Image.open('Compositeimage1').convert('RGBA')
    draw = ImageDraw.Draw(im)
    listofequationoflines = []
    for listofpoints in listoflistofpoints:
        for i in range(len(listofpoints) -1):
            points =[(listofpoints[i][0],listofpoints[i][1]),(listofpoints[i+1][0],listofpoints[i+1][1])]
            x_coords, y_coords = zip(*points)
            A = vstack([x_coords, ones(len(x_coords))]).T
            m, c = lstsq(A, y_coords)[0]
            listofequationoflines.append((m,c))
            print("For ",i,"th line:")
            print(int(listofpoints[i][0])-maxmincoordinates[0],int(listofpoints[i][1]-maxmincoordinates[2]),int(listofpoints[i+1][0])-maxmincoordinates[0],int(listofpoints[i+1][1]-maxmincoordinates[2]))
            draw.line((int(listofpoints[i][0])-maxmincoordinates[0],int(listofpoints[i][1]-maxmincoordinates[2]),int(listofpoints[i+1][0])-maxmincoordinates[0],
                       int(listofpoints[i+1][1]-maxmincoordinates[2])),fill= 128,width=3)
    im.save('roadimagefile1',format='jpeg')
    return listofequationoflines

def convertlattowgs(listoflistofpoints):
    listoflistofwgs =[]
    for listoflatlong in listoflistofpoints:
        listofpoints = []
        for p in listoflatlong:
            new_p = convert_wgs84_to_northFL(p[0],p[1])
            #print(p,new_p)
            listofpoints.append(new_p)
        listoflistofwgs.append(listofpoints)
    #print(listoflistofwgs)
    return listoflistofwgs

def getlidarpointsclosest(listoflistofpoints,listoflidardata):
    print('Inside get lidar data points closest')
    listoflistoflidarpoints =[]
    for listofpoints in listoflistofpoints:
        listoflidarpoints = []
        for point in listofpoints:
            minimum_distance = 1
            for p in listoflidardata:
                dist = math.hypot(point[0]-p.x,point[1]-p.y)
                if (dist<minimum_distance):
                    minimum_distance = dist
                    print(minimum_distance)



if __name__ == "__main__":
    sf = shapefile.Reader('tl_2016_12073_roads/tl_2016_12073_roads.shp')
    #lidar_fileName = "las_tile_46138/2035000.25_541249.75_2036250.25_539999.75.las"
    lidar_fileName = "las_tile_46138/2035000.25_544999.75_2036250.25_543749.75.las"
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
    listoflistofpoints = getlistofpoints(croppedshapes,maxlatlong,minlatlong)
    #printlistofmatchedpoints(listoflistofpoints,listoflidardata)
    newlistoflistofpoints = convertlattowgs(listoflistofpoints)
    listoflineequations = drawlinesinimage(image_size_x,image_size_y,newlistoflistofpoints,maxmincoordinates)
    print(listoflineequations)
    exit(0)
    getlidarpointsclosest(newlistoflistofpoints,listoflidardata)
    setofmatchedlidarpoints=getsetofmatchedlidarpoints(croppedshapes,listoflatlong,listoflidardata)
    colormatcheddatapoints(setofmatchedlidarpoints,imagefile,maxmincoordinates,lidar_fileName.replace('/','')[:-4]+'road_image')
    lidar_file.close()
