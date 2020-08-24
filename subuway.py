import cv2 as cv
from cv2 import aruco
import numpy as np

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

# Node

# 1. Destination node




#main code starts from here

charucoBoard = generateCharucoBoard()
getCharucoBoardImgfromCamera()
allCorners, allIds, imsize = calibrateFromCharucoBoardImage(charucoBoard)
ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners,allIds,imsize, charucoBoard)