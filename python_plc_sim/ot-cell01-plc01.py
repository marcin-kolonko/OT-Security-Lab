import time
import random
import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("######" , "######")
client.connect("10.252.10.11", 1883, 60)
client.loop_start()

state = "WAITING"
state_start = time.time()
motor_speed = 0
current = 0.2
temperature = 36.4
belt_speed =  0
product_detected = 0
state_stop = 0

try:
    while True:

        now = time.time()

        if state == "WAITING":
            motor_speed = 0
            current = 0.2
            temperature = 36.4
            belt_speed =  0

        if state == "WAITING" and now - state_start > (2 + random.uniform(0, 6)):
            state = "RUNNING"
            product_detected = 1

        if state == "RUNNING" and motor_speed < 1500:
            motor_speed = motor_speed + random.randint(150, 200)
            current = round(motor_speed / 700, 2)
            temperature = round(temperature + random.uniform(0, 0.3), 2)
            belt_speed = round(motor_speed / 800, 2)


        if state == "RUNNING" and motor_speed >= 1500:

            state = "STOPPING"
            product_detected = 0

        if state == "STOPPING":
            motor_speed = motor_speed - random.randint(200, 400)
            if motor_speed < 0:
                motor_speed = 0
                state = "WAITING"
                state_start = time.time()
            current = round(motor_speed / 700, 2)
            temperature = round(temperature - random.uniform(0, 0.3), 2)
            if temperature < 36.4:
                temperature = 36.4
            belt_speed = round(motor_speed / 800, 2)

        client.publish("cell01/plc01/motor/speed", f"{motor_speed} rpm")
        client.publish("cell01/plc01/motor/current", f"{current} A")
        client.publish("cell01/plc01/motor/temperature", f"{temperature} °C")
        client.publish("cell01/plc01/belt/speed", f"{belt_speed} m/s")
        client.publish("cell01/plc01/sensor/product", product_detected)
        client.publish("cell01/plc01/state", state)

        time.sleep(1)

finally:
    client.loop_stop()
    client.disconnect()
