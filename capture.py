from machine import Pin
import utime

ir_pin = Pin(21, Pin.IN)
ir_out = Pin(23, Pin.OUT, Pin.PULL_DOWN)

ir_out.on()

noise = []

def falling(pin):
    global ir_pin
    global pulsetime
    global timer
    timer = utime.ticks_us()
    #print("Im falling")
    #print(ir_pin.value())
    ir_pin.irq(trigger=Pin.IRQ_RISING, handler=rising)


def rising(pin):
    global irq_pin
    global pulsetime
    global timer
    pulsetime = utime.ticks_us() - timer
    if len(noise) < 10:
        noise.append(pulsetime)
    else:
        noise.pop(0)

    noise_avg = int(sum(noise)/len(noise))
    noise_low = int(noise_avg*0.85)
    noise_high = int(noise_avg*1.15)
    pulsetimeint = int(pulsetime)
    #print(pulsetime, noise_avg, noise_high, noise_low)
    if pulsetimeint not in range(noise_low, noise_high):
        print(ir_pin.value(), pulsetime)
    #print("Im rising")
    ir_pin.irq(trigger=Pin.IRQ_FALLING, handler=falling)
    timer = 0


ir_pin.irq(trigger=Pin.IRQ_FALLING, handler=falling)

while True:
    if ir_out == 0:
        print("Im hight")