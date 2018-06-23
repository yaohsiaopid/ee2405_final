import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     # Subscribing in on_connect() - if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("ee2405/complete")
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))
#     if msg.payload == b"quit":
#         client.disconnect()

# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect("192.168.1.41", 1883, 60) # host ip
# # listening in the background thread
# client.loop_start()

# initialing publisher

while(1):
    time.sleep(.01)
    mesg = input("Enter the messages: ")
    publish.single("ee2405/complete", mesg, hostname="192.168.1.41")

    if(mesg == 'quit'):
        break

#end listening
client.loop_stop()