import paho.mqtt.client as mqtt
import json
import time
import random
import threading

# Configuración
ID_RED_IOT = "red_talavera"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Cliente MQTT
client = mqtt.Client()
boards_id = ["4F:3C:2D:1A:0B:00", "4F:3C:2D:1A:0B:01", "4F:3C:2D:1A:0B:02"]

def publish_sensor_data():
    topic = f"{ID_RED_IOT}/environment/{boards_id[0]}"
    while True:
        data = {
            "id_board": boards_id[0],
            "temperature": round(random.uniform(10.0, 35.0), 2),
            "humidity": round(random.uniform(30.0, 90.0), 2)
        }
        client.publish(topic, json.dumps(data))
        print(f"[{topic}] {data}")
        time.sleep(5)


def publish_potentiometer_event():
    topic = f"{ID_RED_IOT}/potentiometer/{boards_id[0]}"
    while True:
        data = {
            "id_board": boards_id[0],
            "potentiometer": random.randint(15, 30)
        }
        client.publish(topic, json.dumps(data))
        print(f"[{topic}] {data}")
        time.sleep(5)

def publish_presence_event():
    topic = f"{ID_RED_IOT}/presence/{boards_id[0]}"
    while True:
        data = {
            "id_board": random.choice(boards_id),
            "timestamp": int(time.time()),
            "presence": random.choice([True, False])
        }
        client.publish(topic, json.dumps(data))
        print(f"[{topic}] {data}")
        time.sleep(5)


def main():
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    threading.Thread(target=publish_sensor_data, daemon=True).start()
    threading.Thread(target=publish_potentiometer_event, daemon=True).start()
    threading.Thread(target=publish_presence_event, daemon=True).start()
    print("Publicando datos de sensores...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Finalizando...")
        client.loop_stop()


if __name__ == "__main__":
    main()
