"""Module for processing of lidar files"""
from liblas import file
from PIL import Image
import pyproj



def convert_northFL_to_wgs84(easting, northing):
    '''

    Parameters:
        easting: in feet
        northing: in feet
    '''
    #This are constants that are required for transformation
    wgs84 = pyproj.Proj(init='epsg:4326')
    northFL = pyproj.Proj(init='esri:102660')
    return pyproj.transform(northFL, wgs84,
                            easting * 0.3048, northing * 0.3048)


def getMaxMinCoordinatesforlidarfile(lidarfile):
    '''This is a helper function that gets the max and min co-ordinates of the data points present in lidar file. This is an additional function
      as the max min co-ordinates can be easily known from header information present in the lidar file
     '''
    lidarfile.seek(0)
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


def createImageFile(lidarfile,filename, image_size_x, image_size_y, maxmincoordinates):
    '''This function creates the image of the specified size'''
    i = Image.new(mode='RGB', size=(image_size_x, image_size_y), color=None)
    for p in f:
        i.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
    i.save(filename, format="JPEG")

def getlistoflidardata(lidarfile):
    '''This function returns the list of lidar data points'''
    listOfLidardata = []
    for p in lidarfile:
        listOfLidardata.append(p)
    return listOfLidardata

def getlidardatafile(lidar_fileName):
    '''This function returns the lidar file after opening it'''
    f = file.File(lidar_fileName, mode='r')
    return f

def createImageforregion(lidarfile, maxmincoordinates, imagefile):
    '''This function creates the image for a particular region of the lidar file'''
    status = input('"Do you waant to create image for a particular region of lidar file? Enter Y/Yes or N/No')
    status = status.upper()
    if status == 'Y' or status == 'YES':
        print("min x coordinate:", maxmincoordinates[0], "max x coordinate", maxmincoordinates[1], "min y coordinate", maxmincoordinates[2], "max y coordinate", maxmincoordinates[3])
        upper_x = int(input("Give the x coordinate of the uppermost left point in the diagonal"))
        upper_y = int(input("Give the y coordinate of the uppermost top point in the diagonal"))
        lower_x = int(input('Give the x coordinate of the lowermost right point in the diagonal'))
        lower_y = int(input("Give the y coordinate of the lowermost right point in the diagonal"))
        i = Image.new(mode='RGB', size=(lower_x-upper_x+1, lower_y-upper_y+1), color=None)
        for p in lidarfile:
            if int(p.x) >= upper_x and int(p.x) <= lower_x and int(p.y) >= upper_y and int(p.y) <= lower_y:
                i.putpixel((int(p.x)-upper_x, int(p.y) - upper_y), (p.color.red, p.color.green, p.color.blue))
        i.save(imagefile, format="JPEG")
    else:
        print("Exiting the application")

def printHeaderInformation(lidarfile):
    ''' This function prints the header information of the lidar file'''
    header = lidarfile.header
    print("Major Version:", header.major_version, ", Minor Version:", header.minor_version)
    print("Data format id:", header.data_format_id)
    print("Header offset:", header.offset)
    print("Header max:", header.max)
    print("Header min:", header.min)
    print("sr.proj4", header.srs.proj4)
    print("srs.proj4.getproj4", header.srs.get_proj4())
    print("Header Max latitude longitude:", convert_northFL_to_wgs84(header.max[0], header.max[1]))
    print("Header Min latitude longitude:", convert_northFL_to_wgs84(header.min[0], header.min[1]))

def getHeaderInformation(lidarfile):
    '''This function gets the header of the lidar data file'''
    header = lidarfile.header
    return header

if __name__ == "__main__":
    #lidar_fileName = "las_tile_46138/2035000.25_541249.75_2036250.25_539999.75.las"
    lidar_fileName = "las_tile_46138/2035000.25_544999.75_2036250.25_543749.75.las"
    image_fileName = "lidar_image2"
    image_fileregion = 'lidar_image_rectangle'
    f = file.File(lidar_fileName, mode='r')
    printHeaderInformation(f)
    maxmincoordinates = getMaxMinCoordinatesforlidarfile(f)
    image_size_x = maxmincoordinates[1]-maxmincoordinates[0]+1
    image_size_y = maxmincoordinates[3]-maxmincoordinates[2]+1
    createImageFile(f, lidar_fileName.replace('/', '')[:-4] + 'lidarimage', image_size_x, image_size_y, maxmincoordinates)
    f.seek(0)
    createImageforregion(f, maxmincoordinates, image_fileregion)
