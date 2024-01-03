import asyncio
import uuid
import serial
import requests
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

CONNECTION_STRING = "HostName=hubarduino.azure-devices.net;DeviceId=arduinorev4;SharedAccessKey=XMW4t8iAMDzUZ9gGHIcS5z6Andr50iRXEAIoTGMqb1Y="

MESSAGE_TIMEOUT = 10000

async def main():
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        await client.connect()

        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        ser = serial.Serial('COM4', 115200)

        while True:
            pulse_sensor_data = ser.readline().decode().strip()

            msg_txt_formatted = f"{{\"pulseSensorData\": {pulse_sensor_data}}}"
            message = Message(msg_txt_formatted)

            message.message_id = uuid.uuid4()
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            print("Sending message: %s" % message.data)
            try:
                await client.send_message(message)
            except Exception as ex:
                print("Error sending message from device: {}".format(ex))


            try:
                response = requests.post('http://127.0.0.1:5000/receive_data', data={'pulse_sensor_data': pulse_sensor_data})
                response.raise_for_status()
                print(f"Data sent to Flask server. Server response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to Flask server: {e}")

            await asyncio.sleep(1)

    except Exception as iothub_error:
        print("Unexpected error %s from IoTHub" % iothub_error)
        return
    except asyncio.CancelledError:
        await client.shutdown()
        print('Shutting down device client')

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Keyboard Interrupt - sample stopped')
