from machine import Pin
import utime

ir_pin = Pin(21, Pin.IN)
prev_value = 1
data = []

while True:
    ir_value = ir_pin.value()


    if ir_value == 0 and prev_value == 1:
        zero_start = utime.ticks_us()
        one_timed = utime.ticks_diff(utime.ticks_us(),one_start)
        #print(data)
        if one_timed < 50000:
            data.append((1, one_timed))
        
    if ir_value == 1 and prev_value == 0:
        one_start = utime.ticks_us()
        zero_timed = utime.ticks_diff(utime.ticks_us(),zero_start)

        if zero_timed < 50000:
            data.append((0, zero_timed))
        if one_timed > 100000 and len(data)>5:
            print(data, "\n", "Last one timed was", one_timed, "\n")
            data = []
            one_timed = utime.ticks_diff(utime.ticks_us(),one_start)

    prev_value = ir_value
