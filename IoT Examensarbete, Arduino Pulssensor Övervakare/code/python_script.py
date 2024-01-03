import asyncio
import uuid
import serial 
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

CONNECTION_STRING = ""

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
