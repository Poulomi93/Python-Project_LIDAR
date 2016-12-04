import numpy as np
from sklearn import svm
from liblas import file
import lidar_proocessing
from PIL import Image

def write_result(results):
    f = open('final_result','w')
    for result in results:
        f.write(str(result)+'\n')
    f.close()

def train_dataset():
    data_set = np.loadtxt('testdata.txt',delimiter=',')
    print(data_set.shape)
    X = data_set[:,0:4]
    y = data_set[:,4]
    print(X)
    print(y)
    print(X.shape[1])
    obj_svm = svm.SVC()
    obj_svm.gamma = 0.75
    print(obj_svm)
    obj_svm.fit(X,y)
    test_set = np.loadtxt('final_test_file.txt', delimiter=',')
    print(test_set.shape[1])
    print(test_set)
    results=obj_svm.predict(test_set)
    write_result(results)


def create_test_file(lidar_fileName):
    f = file.File(lidar_fileName, mode='r')
    test_file = open('final_test_file.txt','w')
    for p in f:
        test_file.write(str(p.color.red) + ',')
        test_file.write(str(p.color.green) + ',')
        test_file.write(str(p.color.blue) + '\n')
        #test_file.write(str(p.z)+'\n')
    test_file.close()

def draw_image(fileName):
    lidar_file = file.File(fileName, mode='r')
    maxmincoordinates = lidar_proocessing.getMaxMinCoordinatesforlidarfile(lidar_file)
    i = Image.new(mode='RGB', size=(maxmincoordinates[1] - maxmincoordinates[0] + 1, maxmincoordinates[3] - maxmincoordinates[2] + 1), color=None)
    result_file =open('final_test_file.txt','r')
    all_results = result_file.readlines()
    no = 0
    matched_points = 0
    for p in lidar_file:
        if all_results[no] == '1':
            i.putpixel((int(p.x) - maxmincoordinates[0], int(p.y) - maxmincoordinates[2]),
                   (p.color.red, p.color.green, p.color.blue))
            matched_points = matched_points+1
        no = no+1
    print(no)
    print('matched points:',matched_points)
    i.save('final_road_image', format="JPEG")


if __name__ == '__main__':
    lidar_fileName = "las_tile_46138/2037500.25_543749.75_2038750.25_542499.75.las"
    #create_test_file(lidar_fileName)
    train_dataset()
    draw_image(lidar_fileName)