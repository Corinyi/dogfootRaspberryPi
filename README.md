# YEHS 메이커톤
### 하루만 더 줘

## 라즈베리파이에서 실행하는 법

라즈베리파이에 랩실이나 기숙사 와이파이 연결하세요~
라즈베리파이 이름 : pi
라즈베리파이 비밀번호 : abcd1234

ssh pi@주소
ex) ```ssh pi@192.158.1.100```

```$ ifconfig```

이렇게 해서 라즈베리파이가 연결된 ip 알아놓으세요~ 

```$ cd Desktop/final/dogfootRaspberryPi```

```$ node index.js```

서버 시작(브라우저에서 (   ip주소  ):3000  - ex) 192.168.1.100:3000 접속하면 바로 보입니다.)

창 하나 더 띄워서(서버 여는 창 하나, 마커 인식하는 창 하나 총 2개 필요)

```$ cd ~ ```

``` $ source dogfoot/bin/activate ```

virtualenv 이름이 dogfoot이고 여기에 필요한 모듈들(openCV, 뭐시기뭐시기 등등) 깔아놓음. dogfoot 으로 작업환경에 들어가는 코드

```$ python3 subuway.py```

서부외이 파이썬 파일 실행(나머지 코드는 ssh로 실행해도 되는데, 이 코드는 x-server 필요해서 웬만하면 그냥 라즈베리파이 자체에서 실행하세요)


### subuway.py 조금 달라진 부분
- cv.VideoCapture(1) -> cv.VideoCapture(0)
    라즈베리파이 카메라 모듈을 사용하려면 비디오 모듈 0번을 사용해야함.
- server의 html 데이터 실시간 변경
    171번째 줄에 stringList를 스트링으로 바꿔서 html에 띄우는 코드가 있음
    마지막 부분에 html_sending(stringList)로 해서 도출된 리스트를 웹으로 쏘아줌.
    * 웹에 잘 들어가는 것을 확인하기 위해서 html 타입으로 변경해줌 -> app inventor에서
    가져오려면 그냥 html 코드 없이 스트링만 쏴주면 됨


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

* 


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


