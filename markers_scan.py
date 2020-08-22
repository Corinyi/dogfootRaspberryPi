#!/usr/bin/env python

from __future__ import print_function
from Naked.toolshed.shell import execute_js, muterun_js
import time

try:
    import cv2
    from ar_markers import detect_markers
except ImportError:
    raise Exception('Error: OpenCv is not installed')


if __name__ == '__main__':
    print('Press "q" to quit')
    capture = cv2.VideoCapture(0)
    idlist = [0]

    if capture.isOpened():  # try to get the first frame
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:
        markers = detect_markers(frame)
        for marker in markers:
            marker.highlite_marker(frame)
            temp = str(marker)
            markerid = int(temp[11:15]) # marker 프린트하니까 스트링 형태로 나와서 마커 아이디만 추출하는 부분

            if (markerid != idlist[-1]): # 새로운 마커 아이디가 기존 마커 리스트의 마지막과 다를 경우에만
                idlist.append(markerid) # 마커 리스트에 새로운 마커 아이디 추가(위 코드 없으면 계속해서 마커 리스트에 반복적 추가)
                # 아래부터는 그냥 내가 임의로 작성한 코드
                if(markerid == 611):
                    execute_js(left.js)
                if(markerid == 743):
                    execute_js(right.js)
                if(markerid == 877):
                    execute_js(right.js)
                if(markerid == 2296):
                    execute_js(right.js)
                if(markerid == 3803):
                    execute_js(left.js)
                if(markerid == 2312):
                    execute_js(left.js)
                if(markerid == 2296):
                    execute_js(left.js)
                if(markerid == 3734):
                    execute_js(left.js)
                time.sleep(1) # 마커 계속 인식하니까 인식 오류가 조금씩 나서 1초 딜레이 줌
    
            


        cv2.imshow('Test Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # frame 창에서 'q' 입력하면 종료
            break
        frame_captured, frame = capture.read()

    # When everything done, release the capture
    print(idlist)
    capture.release()
    cv2.destroyAllWindows()

