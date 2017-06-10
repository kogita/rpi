import cv2
import sys

cascade_file = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"

def get_face_list(image):
    # to gray scale
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # read face file
    cascade = cv2.CascadeClassifier(cascade_file)
    # detect face
    face_list = cascade.detectMultiScale(image_gs,
                                         scaleFactor=1.1,
                                         minNeighbors=1,
                                         minSize=(150,150))
    return face_list

def add_rectangle(image, face_list):
    color = (0, 0, 255)
    for face in face_list:
        x, y, w, h = face
        cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=8)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print("argument error\n")
        quit()

    image_file = argvs[1]
    print("image file name: {0}".format(image_file))
    image = cv2.imread(image_file)
    face_list = get_face_list(image)
    print("face list:", face_list)
    if len(face_list) > 0:
        add_rectangle(image, face_list)
        cv2.imwrite("facedetect-output.png", image)
    else:
        print("no face")
