from django_cron import CronJobBase, Schedule
import paho.mqtt.client as mqtt
from django.utils.timezone import now
from web.models import MyPayment

# MQTT Broker details
mqtt_broker = "164.90.230.152"
mqtt_port = 1883

def check_and_update_doors():
    # Fetch expired payments where the current time is >= end_date
    expired_payments = MyPayment.objects.filter(end_date__lte=now(), Payment_status='paid')

    for payment in expired_payments:
        room_number = payment.Room.Room_Number
        try:
            if room_number == "1":
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'highdoorone')
            elif room_number == "2":
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'highdoorone')
        except Exception as e:
            print(f"Error processing room {room_number}: {e}")

