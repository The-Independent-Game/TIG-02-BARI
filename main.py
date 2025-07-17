from machine import Pin, PWM
import time

STEP = 500
# Configurazione pin
# Motore A
ain1 = Pin(26, Pin.OUT)
ain2 = Pin(27, Pin.OUT)
pwma = PWM(Pin(28))
pwma.freq(1000)

# Motore B  
bin1 = Pin(21, Pin.OUT)
bin2 = Pin(20, Pin.OUT)
pwmb = PWM(Pin(19))
pwmb.freq(1000)

# Standby
stby = Pin(22, Pin.OUT)
stby.on()  # Abilita driver

# Imposta direzione avanti
def forward():
    print("avanti")
    ain1.on()
    ain2.off()
    
def backwards():
    print("indietro")
    ain1.off()
    ain2.on()
    
def stop():
    ain1.off()
    ain2.off()
    pwma.duty_u16(0)

def speed_ramp():
    print("Accelerazione...")
    for speed in range(0, 65536, STEP):
        pwma.duty_u16(speed)
        print(f"PWM: {speed} ({speed/655.35:.1f}%)")
        time.sleep(0.05)

    print("Decelerazione...")
    for speed in range(65535, -1, -STEP):
        pwma.duty_u16(speed)
        print(f"PWM: {speed} ({speed/655.35:.1f}%)")
        time.sleep(0.05)

forward()
#pwma.duty_u16(40000)
#time.sleep(3)
speed_ramp()
stop()
backwards()
#pwma.duty_u16(40000)
#time.sleep(3)
speed_ramp()
stop()


