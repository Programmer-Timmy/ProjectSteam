from copyreg import dispatch_table

import serial
import time
import requests
from requests.utils import resolve_proxies

api_key = "c907d723-535a-477b-91d9-e7da056a3fba"  #Put your API key over here
# url = "http://localhost:8000/raspberry/status/"
url = "http://localhost:8000/raspberry/is_to_close/"


#Simple program to test the connection between the raspberry and the computer.
def communicate_with_pico():
    port = "COM3"
    baudrate = 9600
    last_update = False
    pico_uart = serial.Serial(port, baudrate, timeout=1)

    try:
        time.sleep(1)

        while True:
            if pico_uart.in_waiting > 0:
                try:
                    data = pico_uart.read_until()
                    data = data.decode('utf-8').strip() == 'True'
                    print(data)
                    # distance = float(decoded_data)
                    if data and not last_update:
                        update_user_is_to_close(True)
                        last_update = True
                        print("Updated status to: True")
                    if not data and last_update:
                        update_user_is_to_close(False)
                        last_update = False
                        print("Updated status to: False")



                except UnicodeDecodeError:
                    print("Failed to decode data from Pico. Received:")

            else:
                print("No data received yet.")

            time.sleep(0.5)

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        pico_uart.close()
        print("Serial port closed.")


#Makes a request to the django view to update the user status. It uses a generated api key.
def update_user_status(is_online):
    import requests
    # Make the request
    response = requests.post(url, data={'api_key': api_key, 'is_online': is_online})

    # Check the response
    if response.status_code == 200:
        print("Status updated successfully!")
    else:
        print(f"Failed to update status. Status code: {response.status_code}, Response: {response.text}")

def update_user_is_to_close(is_to_close):
    import requests

    response = requests.post(url, data={'api_key': api_key, 'is_to_close': is_to_close})
    if response.status_code == 200:
        print("Status updated successfully!")
    else:
        print(f"Failed to update status. Status code: {response.status_code}, Response: {response.text}")
if __name__ == "__main__":
    communicate_with_pico()
    # update_user_status(Trdaue)