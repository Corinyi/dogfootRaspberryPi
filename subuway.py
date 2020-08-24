import cv2 as cv
from cv2 import aruco
import numpy as np
import glob
import time

print(cv.__version__)
print(np.__version__)

# We use 250 ID
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# 1~4는 그냥 카메라 캘리브레이션을 위해 제작한 코드이므로 딱히 신경쓸 필요는 없을듯.
# 1. Once it generate the board we print the board and take with our camera.
def generateCharucoBoard():
    board = aruco.CharucoBoard_create(7, 5, 0.04, 0.02, aruco_dict)
    imboard = board.draw((2000, 2000))
    cv.imwrite('charuco_board.tiff', imboard)
    return board

# 2. If press 'c' capture current image from camrera, If press 'esc' finish the task
def getCharucoBoardImgfromCamera():
    print("press esc to terminate")
    print("press c to capture")
    cap = cv.VideoCapture(1)
    i = 1 #step

    while (1):
        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_CUBIC)

        cv.imshow('output', frame)

        k = cv.waitKey(5) & 0xFF
        #press esc to terminate
        if k == 27:
            break

        #press c to capture
        #save our pictures in folder "calibpic"
        if k == ord('c'):
            workdir = "./calibpic/"
            cv.imwrite(workdir + 'calibBoard'+str(i)+'.jpg', frame)
            print('image' + str(i) + 'saved')
            i = int(i) + 1

    cv.destroyAllWindows()

# 3. We calibrate our camera to get camera matrix and distorsion vector
def calibrateFromCharucoBoardImage(board):
    #get pictures in folder "calibpic"
    workdir = "./calibpic/"
    images = glob.glob(workdir + '*.jpg')
    print(images)
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0

    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv.imread(im)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict)
        fixedcorners = []

        # If we detect the corners from image
        if len(corners) > 0:
            # SUB PIXEL DETECTION
            for corner in corners:
                corner2 = cv.cornerSubPix(gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria)
                fixedcorners.append(corner2)

            # InterpolateCornersCharuco return [1]:corners, [2]:Ids
            CornerandIds = aruco.interpolateCornersCharuco(fixedcorners, ids, gray, board)
            if CornerandIds[1] is not None and CornerandIds[2] is not None and len(CornerandIds[1]) > 3 and decimator % 1 == 0:
                allCorners.append(CornerandIds[1])
                allIds.append(CornerandIds[2])

        decimator += 1

    imsize = gray.shape
    return allCorners, allIds, imsize

# 4. calibrate and get the vectors
def calibrate_camera(allCorners,allIds,imsize, board):
    """
    Calibrates the camera using the dected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv.CALIB_USE_INTRINSIC_GUESS + cv.CALIB_RATIONAL_MODEL + cv.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients0,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv.TERM_CRITERIA_EPS & cv.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

# 5. Dectect Id and Calculate the distance, rotation vector from aruco marker by camera
def detectMarker(ret, mtx, dist, rvecs, tvecs):
    start = time.time()
    cap = cv.VideoCapture(1)
    i = 1  # step

    while (1):
        # wait for 1 seconds
        if time.time() - start > 1:
            break

        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        frame = cv.resize(frame, None, fx=1, fy=1, interpolation=cv.INTER_CUBIC)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # SUB PIXEL DETECTION
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
        fixedCorners = []

        for corner in corners:
            corner2 = cv.cornerSubPix(gray, corner, winSize=(3, 3), zeroZone=(-1, -1), criteria=criteria)
            fixedCorners.append(corner2)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), fixedCorners, ids)

        size_of_marker = 0.0285  # side lenght of the marker in meter
        rvecs, tvecs, _obj = aruco.estimatePoseSingleMarkers(fixedCorners, size_of_marker, mtx, dist)

        if tvecs is None:
            cv.imshow('output', frame)
            print("-----------------------------")
            cv.waitKey(10)
            return None, None, None, None

        cv.imshow('output', frame_markers)

        k = cv.waitKey(30) & 0xFF
        # press esc to terminate
        if k == 27:
            break

    cv.destroyAllWindows()

    return ids, fixedCorners, rvecs, tvecs

# Node and Route information data structure

class markerNode:
    """
    Save marker data
    Floor : current floor
    Id : id of the marker
    northConnectedNode : connected node which located in north
    southConnectedNode : connected node which located in south
    westConnectedNode : connected node which located in west
    eastConnectedNode : connected node which located in east
    nextNode : next node for the route

    1. Destination Node
        For elevator, toilet, exit etc
        Use Id from 1~50
    2. Marker Node
        For the way point
        Use Id from over 50
    """
    def __init__(self, name, floor, id, north = None, south = None, west = None, east = None):
        self.name = name
        self.floor = floor
        self.id = id
        self.northConnectedNode = north
        self.southConnectedNode = south
        self.westConnectedNode = west
        self.eastConnectedNode = east
        self.next = None

    def update(self, north = None, south = None, west = None, east = None):
        self.northConnectedNode = north
        self.southConnectedNode = south
        self.westConnectedNode = west
        self.eastConnectedNode = east
        self.next = None

class markerGraph:
    """
    Fixed map graph for Seolleung station
    Not made yet
    """
    def __init__(self):
        self.size = 1000

class routeData:
    """
    Stack the ordered route information
    """
    def __init__(self, markerNode = None):
        self.head = markerNode
        self.routeLength = 1

    def insertFirstNode(self, firstNode):
        new_node = firstNode
        temp_node = self.head
        self.head = new_node
        self.head.next = temp_node
        self.routeLength += 1

    def insertLast(self, insertNode):
        node = self.head
        while True:
            if node.next == None:
                break
            node = node.next

        new_node = insertNode
        node.next = new_node
        self.routeLength += 1

    def selectNode(self, num):
        if self.routeLength < num:
            print("Overflow")
            return
        node = self.head
        count = 0
        while count < num:
            node = node.next
            count += 1
        return node

    def deleteHead(self):
        node = self.head
        self.head = node.next
        del node
        self.routeLength -= 1

    def length(self):
        return str(self.routeLength)

def createB2mapInSeooleung():
    """
    Seolleung station marker nodes in B2 Floor
    :return: way points in Seolleung station B2
    """
    #railWay marker
    global railWay_7_4_Seolleung_B2
    global railWay_8_1_Seolleung_B2, railWay_8_2_Seolleung_B2, railWay_8_3_Seolleung_B2, railWay_8_4_Seolleung_B2
    global railWay_9_1_Seolleung_B2
    # blockWay marker
    global blockWay_51_Seolleung_B2, blockWay_52_Seolleung_B2
    # elevator marker
    global elevator_2_Seolleung_B2

    # railWay marker
    railWay_7_4_Seolleung_B2 = markerNode("Seolleung_7_4_B2", 2, 1)
    railWay_8_1_Seolleung_B2 = markerNode("Seolleung_8_1_B2", 2, 2)
    railWay_8_2_Seolleung_B2 = markerNode("Seolleung_8_2_B2", 2, 2)
    railWay_8_3_Seolleung_B2 = markerNode("Seolleung_8_3_B2", 2, 2)
    railWay_8_4_Seolleung_B2 = markerNode("Seolleung_8_4_B2", 2, 2)
    railWay_9_1_Seolleung_B2 = markerNode("Seolleung_9_1_B2", 2, 2)

    # blockWay marke
    blockWay_51_Seolleung_B2 = markerNode("Seolleung_51_B2", 2, 51)
    blockWay_52_Seolleung_B2 = markerNode("Seolleung_52_B2", 2, 52)

    # elevator marker
    elevator_2_Seolleung_B2 = markerNode("Seolleung_EV_2_B2", 2, 3)

    #update
    railWay_7_4_Seolleung_B2.update(north = blockWay_51_Seolleung_B2, east = railWay_8_1_Seolleung_B2)
    railWay_8_1_Seolleung_B2.update(west = railWay_7_4_Seolleung_B2, east = railWay_8_2_Seolleung_B2)
    railWay_8_2_Seolleung_B2.update(west = railWay_8_1_Seolleung_B2, east = railWay_8_3_Seolleung_B2)
    railWay_8_3_Seolleung_B2.update(west = railWay_8_2_Seolleung_B2, east = railWay_8_4_Seolleung_B2)
    railWay_8_4_Seolleung_B2.update(west = railWay_8_3_Seolleung_B2, east = railWay_9_1_Seolleung_B2)
    railWay_9_1_Seolleung_B2.update(west = railWay_8_4_Seolleung_B2)

    blockWay_51_Seolleung_B2.update(north = blockWay_52_Seolleung_B2, west = railWay_7_4_Seolleung_B2)
    blockWay_52_Seolleung_B2.update(south = blockWay_51_Seolleung_B2, east = elevator_2_Seolleung_B2)

    elevator_2_Seolleung_B2.update(west = blockWay_52_Seolleung_B2)


def createB3mapInSeooleung():
    """
    Seolleung station marker nodes in B3 Floor
    :return: way points in Seolleung station B3
    """
    # railWay marker
    global railWay_2_4_Seolleung_B3
    # blockWay marker
    global blockWay_53_Seolleung_B3, blockWay_54_Seolleung_B3, blockWay_55_Seolleung_B3
    # elevator marker
    global elevator_2_Seolleung_B3

    # railWay marker
    railWay_2_4_Seolleung_B3 = markerNode("Seolleung_2_4_B3", 3, 4)

    # blockWay marker
    blockWay_53_Seolleung_B3 = markerNode("Seolleung_53_B3", 3, 53)
    blockWay_54_Seolleung_B3 = markerNode("Seolleung_54_B3", 3, 54)
    blockWay_55_Seolleung_B3 = markerNode("Seolleung_55_B3", 3, 55)

    # elevator marker
    elevator_2_Seolleung_B3 = markerNode("Seolleung_EV_2_B3", 3, 3)

    #update
    railWay_2_4_Seolleung_B3.update(east=blockWay_55_Seolleung_B3)

    blockWay_53_Seolleung_B3.update(west=blockWay_54_Seolleung_B3, south=elevator_2_Seolleung_B3)
    blockWay_54_Seolleung_B3.update(east=blockWay_53_Seolleung_B3, north=blockWay_55_Seolleung_B3)
    blockWay_55_Seolleung_B3.update(west=railWay_2_4_Seolleung_B3, south=blockWay_54_Seolleung_B3)

    elevator_2_Seolleung_B3.update(north = blockWay_53_Seolleung_B3)


def createB1mapInHanti():
    """
    Hanti station marker nodes in B4 Floor
    :return: way points in Hanti station B4
    """
    #railWay marker

    #blockWay marker
    global blockWay_59_Hanti_B1
    # elevator marker
    global elevator_1_Hanti_B1, elevator_2_Hanti_B1

    # blockWay marker
    blockWay_59_Hanti_B1 = markerNode("Hanti_59_B1", 1, 59)

    # elevator marker
    elevator_1_Hanti_B1 = markerNode("Hanti_EV_1_B1", 1, 7)
    elevator_2_Hanti_B1 = markerNode("Hanti_EV_2_B1", 1, 8)

    #update
    blockWay_59_Hanti_B1.update(south = elevator_2_Hanti_B1, east = elevator_1_Hanti_B1)

    elevator_1_Hanti_B1.update(west = blockWay_59_Hanti_B1)
    elevator_2_Hanti_B1.update(north = blockWay_59_Hanti_B1)


def createB4mapInHanti():
    """
    Hanti station marker nodes in B4 Floor
    :return: way points in Hanti station B4
    """
    #railWay marker
    global railWay_2_4_Hanti_B4
    global railWay_3_1_Hanti_B4, railWay_3_2_Hanti_B4
    # blockWay marker
    global blockWay_56_Hanti_B4, blockWay_57_Hanti_B4, blockWay_58_Hanti_B4
    # elevator marker
    global elevator_1_Hanti_B4

    # railWay marker
    railWay_2_4_Hanti_B4 = markerNode("Hanti_2_4_B4", 4, 4)
    railWay_3_1_Hanti_B4 = markerNode("Hanti_3_1_B4", 4, 5)
    railWay_3_2_Hanti_B4 = markerNode("Hanti_3_2_B4", 4, 6)

    #blockWay marker
    blockWay_56_Hanti_B4 = markerNode("Hanti_56_B4", 4, 56)
    blockWay_57_Hanti_B4 = markerNode("Hanti_57_B4", 4, 57)
    blockWay_58_Hanti_B4 = markerNode("Hanti_58_B4", 4, 58)

    # elevator marker
    elevator_1_Hanti_B4 = markerNode("Hanti_EV_1_B4", 4, 7)

    #update
    railWay_2_4_Hanti_B4.update(west = railWay_3_1_Hanti_B4)
    railWay_3_1_Hanti_B4.update(west = railWay_3_2_Hanti_B4, east = railWay_2_4_Hanti_B4)
    railWay_3_2_Hanti_B4.update(north = blockWay_56_Hanti_B4, east = railWay_3_1_Hanti_B4)

    blockWay_56_Hanti_B4.update(south = railWay_3_2_Hanti_B4, west = blockWay_57_Hanti_B4)
    blockWay_57_Hanti_B4.update(north = blockWay_58_Hanti_B4, east = blockWay_56_Hanti_B4)
    blockWay_58_Hanti_B4.update(south = blockWay_57_Hanti_B4, west = elevator_1_Hanti_B4)

    elevator_1_Hanti_B4.update(east = blockWay_58_Hanti_B4)


def createRouteForTransfer():
    # Seolleung station B2 way point
    global routeDataList
    routeDataList = routeData(railWay_9_1_Seolleung_B2)
    routeDataList.insertLast(railWay_8_4_Seolleung_B2)
    routeDataList.insertLast(railWay_8_3_Seolleung_B2)
    routeDataList.insertLast(railWay_8_2_Seolleung_B2)
    routeDataList.insertLast(railWay_8_1_Seolleung_B2)
    routeDataList.insertLast(railWay_7_4_Seolleung_B2)
    routeDataList.insertLast(blockWay_51_Seolleung_B2)
    routeDataList.insertLast(blockWay_52_Seolleung_B2)
    routeDataList.insertLast(elevator_2_Seolleung_B2)
    routeDataList.insertLast(elevator_2_Seolleung_B3)
    routeDataList.insertLast(blockWay_53_Seolleung_B3)
    routeDataList.insertLast(blockWay_54_Seolleung_B3)
    routeDataList.insertLast(blockWay_55_Seolleung_B3)
    routeDataList.insertLast(railWay_2_4_Seolleung_B3)
    routeDataList.insertLast(railWay_2_4_Hanti_B4)
    routeDataList.insertLast(railWay_3_1_Hanti_B4)
    routeDataList.insertLast(railWay_3_2_Hanti_B4)
    routeDataList.insertLast(blockWay_56_Hanti_B4)
    routeDataList.insertLast(blockWay_57_Hanti_B4)
    routeDataList.insertLast(blockWay_58_Hanti_B4)
    routeDataList.insertLast(elevator_1_Hanti_B4)
    routeDataList.insertLast(elevator_1_Hanti_B1)
    routeDataList.insertLast(blockWay_59_Hanti_B1)
    routeDataList.insertLast(elevator_2_Hanti_B1)

class currentLocation:
    def __init__(self, floor, prev = None, cur = None, next = None):
        self.floor = floor
        self.prev = prev
        self.cur = cur
        self.next = next

    def updateFloor(self, floor):
        self.floor = floor

    def updateLocation(self, next):
        self.prev = self.cur
        self.cur = self.next
        self.next = next

def findMarkerLocation(findId):
    node = routeDataList.head
    while True:
        if node.id == findId:
            return node
        node = node.next
        if node.next == None:
            print("Not found")
            return

def dataForNextNode(currentLoc, mode):
    """
    get the data to go to next node

    :param node: Get the current node data
    :param mode:
    0 : Nothing, just go forward
    1 : Riding elevator, change to E.V. sign
    2 : Riding subway, change to wait sign
    3 : Etc, depending on the situation

    :return: string list data which will be sent to web
    """
    prev  = currentLoc.prev
    cur = currentLoc.cur
    next = currentLoc.next
    stringList = []

    if mode == 0:
        if cur.northConnectedNode == next:
            if cur.southConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.eastConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.westConnectedNode == next:
            if cur.eastConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.northConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.southConnectedNode == next:
            if cur.northConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.westConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.eastConnectedNode == next:
            if cur.westConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.southConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        stringList.append("F")

    elif mode == 1:
        if next == None:
            stringList.append("E")
            stringList.append("FINISH")
            stringList.append("E")
            return stringList

        stringList.append("E")
        stringList.append("Go_to_B" + str(next.floor) + "_floor")
        stringList.append("E")

    elif mode == 2:
        stringList.append("S")
        stringList.append("Get_off_at_" + str(next.name) + "_platform")
        stringList.append("S")

    elif mode == 3:
        if cur == railWay_9_1_Seolleung_B2:
            stringList.append("L")
            stringList.append("Turn_Left")
            stringList.append("F")
        elif cur == railWay_7_4_Seolleung_B2:
            stringList.append("R")
            stringList.append("Turn_Right_Go_Straight_Turn_Right")
            stringList.append("F")
        elif cur == elevator_2_Seolleung_B3:
            stringList.append("F")
            stringList.append("Get_off_EV_Go_Straight")
            stringList.append("F")
        elif cur == railWay_2_4_Hanti_B4:
            stringList.append("L")
            stringList.append("Get_off_Subway_Turn_Left")
            stringList.append("F")
        elif cur == elevator_1_Hanti_B1:
            stringList.append("L")
            stringList.append("Get_off_EV_Turn_Left")
            stringList.append("F")

    return stringList

#main function
if __name__ == '__main__':
    charucoBoard = generateCharucoBoard()
    getCharucoBoardImgfromCamera()
    allCorners, allIds, imsize = calibrateFromCharucoBoardImage(charucoBoard)
    ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners, allIds, imsize, charucoBoard)

    createB2mapInSeooleung()
    createB3mapInSeooleung()
    createB1mapInHanti()
    createB4mapInHanti()
    createRouteForTransfer()

    IdList = [2, 2, 2, 2, 2, 1, 51, 52, 3, 3, 53, 54, 55, 4, 4, 5, 6, 56, 57, 58, 7, 7, 59, 8]
    modeList = [3, 0, 0, 0, 0, 3, 0, 0, 1, 3, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 1, 3, 0, 1]

    i = 0

    while True:
        if i == 8:
            print("")

        if routeDataList.routeLength == 0:
            print("The end")
            break

        #First recognization
        ids, fixedCorners, rvecs, tvecs = detectMarker(ret, mtx, dist, rvecs, tvecs)

        if ids == None:
            print("Can't recognize")
            continue
        else:
            currentNode = findMarkerLocation(ids)
            if currentNode is None:
                print("Wrong way")
                continue

        mode = modeList[i]

        if i == 0:
            currentLocation = currentLocation(currentNode.floor, cur = currentNode, next = currentNode.next)
        else:
            currentLocation.updateLocation(currentNode.next)
            if currentLocation.prev.floor != currentLocation.cur.floor:
                currentLocation.updateFloor(currentLocation.cur.floor)

        stringList = dataForNextNode(currentLocation, mode)
        print("step " + str(i))
        print(stringList)

        routeDataList.deleteHead()

        print("Wait a moment")
        cv.waitKey(1000)
        print("NEXT")

        i += 1