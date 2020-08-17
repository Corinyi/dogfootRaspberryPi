# YEHS 메이커톤
### 하루만 더 줘

하드웨어 구성

- 메인컴퓨팅
    - 라즈베리파이 제로 W
- 전원부
    - 18650 배터리
    - 충전 모듈
    - 승압 모듈
- 영상인식부
    - raspi 전용 카메라
- 메인 몸체
    - 기성품 모자에 추가 모듈 장착

* marker_scan.py 파일이 마커 인식하면 터미널에 해당하는 출력 내보내는 파일이야. 이 파일에 코딩하거나 모듈로 쓰면 될것 같아.


필요한 파이썬 모듈

```
sudo apt-get install libhdf5-dev -y && sudo apt-get install libhdf5-serial-dev -y && sudo apt-get install libatlas-base-dev -y && sudo apt-get install libjasper-dev -y && sudo apt-get install libqtgui4 -y && sudo apt-get install libqt4-test -y
```
```
pip install opencv-contrib-python==4.1.0.25
```
```
pip install ar_markers
```
```
git clone https://github.com/MomsFriendlyRobotCompany/ar_markers.git
```

> 라즈베리파이 세팅 사이트
 https://maker.pro/raspberry-pi/tutorial/how-to-set-up-opencv-on-raspberry-pi-for-face-detection
 
> openCV 예제 사이트
https://m.blog.naver.com/PostView.nhn?blogId=chandong83&logNo=221291349712&proxyReferer=https:%2F%2Fwww.google.com%2F
