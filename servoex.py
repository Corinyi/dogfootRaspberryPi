import RPi.GPIO as GPIO  
from time import sleep



GPIO.setmode(GPIO.BOARD) 

GPIO.setup(12, GPIO.OUT) 
GPIO.setup(36, GPIO.OUT) 

p = GPIO.PWM(12, 50)
s = GPIO.PWM(36, 50) 

p.start(0)            
s.start(0) 

p.ChangeDutyCycle(3)
s.ChangeDutyCycle(3) 
sleep(1)

p.ChangeDutyCycle(12)
s.ChangeDutyCycle(12)
sleep(1) 

p.ChangeDutyCycle(7.5)
s.ChangeDutyCycle(7.5)
sleep(1)


'''
while(1):

  val = float(int(input('으아으아: ')))
  
  if val == -1 :break


  p.ChangeDutyCycle(val)
'''

p.stop()
s.stop()                
GPIO.setwarnings(False)
GPIO.cleanup() 