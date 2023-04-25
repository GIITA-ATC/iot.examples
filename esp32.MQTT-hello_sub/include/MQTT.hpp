#pragma once

AsyncMqttClient mqttClient;

String GetPayloadContent(char *data, size_t len)
{
	String content = "";
	for (size_t i = 0; i < len; i++)
	{
		content.concat(data[i]);
	}
	return content;
}

void SuscribeMqtt()
{
	uint16_t packetIdSub = mqttClient.subscribe(MQTT_TOPIC, 0);
	Serial.print("Subscribing at QoS 2, packetId: ");
	Serial.println(packetIdSub);
}

void PublishMqtt(String payload)
{
	mqttClient.publish(MQTT_TOPIC, 0, true, (char *)payload.c_str());
}

void OnMqttReceived(char *topic, char *payload, AsyncMqttClientMessageProperties properties, size_t len, size_t index, size_t total)
{
	Serial.print("Received on ");
	Serial.print(topic);
	Serial.print(": ");

	String content = GetPayloadContent(payload, len);
	Serial.print(content);
	Serial.println();

	buzzer_state = content == "ON" ? true : false;

	Serial.print("Buzzer state: ");
	Serial.println(buzzer_state);
}