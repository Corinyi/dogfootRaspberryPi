import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  #time 라이브러리의 sleep함수 사용

servoPin1          = 12
servoPin2          = 36   # 서보 핀
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기

GPIO.setmode(GPIO.BOARD)        # GPIO 설정
GPIO.setup(servoPin1, GPIO.OUT)  # 서보핀 출력으로 설정
GPIO.setup(servoPin2, GPIO.OUT)

servo1 = GPIO.PWM(servoPin1, 50)
servo2 = GPIO.PWM(servoPin2, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo1.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.
servo2.start(0)


'''
서보 위치 제어 함수
degree에 각도를 입력하면 duty로 변환후 서보 제어(ChangeDutyCycle)
'''
def setServoPos1(degree):
  # 각도는 180도를 넘을 수 없다.
  if degree > 180:
    degree = 180

  # 각도(degree)를 duty로 변경한다.
  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # duty 값 출력
  #print("Degree: {} to {}(Duty)".format(degree, duty))

  # 변경된 duty값을 서보 pwm에 적용
  servo1.ChangeDutyCycle(duty)
def setServoPos2(degree):
  # 각도는 180도를 넘을 수 없다.
  if degree > 180:
    degree = 180

  # 각도(degree)를 duty로 변경한다.
  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  # 변경된 duty값을 서보 pwm에 적용
  servo2.ChangeDutyCycle(duty)

for i in range (5):
    setServoPos1((180/4)*i)
    setServoPos2((180/4)*i)
    sleep(1)

# 서보 PWM 정지
servo1.stop()
servo2.stop()
# GPIO 모드 초기화
GPIO.cleanup()