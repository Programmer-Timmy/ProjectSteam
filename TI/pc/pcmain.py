import serial
import time


#Simple program to test the connection between the raspberry and the computer.
def communicate_with_pico():
    port = "COM3"
    baudrate = 9600

    with serial.Serial(port, baudrate, timeout=1) as pico_uart:
        time.sleep(2)
        pico_uart.write(b'm')
        print("Sent 'm' to Pico.")
        while True:
            if pico_uart.in_waiting > 0:
                data = pico_uart.read_until()
                print(f"Received from Pico: {data}")
            else:
                print("No data received yet.")
            time.sleep(1)

import requests

#Functions isn't working yet. But if it works is would update the user status when the pico wants to.
def update_user_status(is_online):

    url = "http://localhost:8000/raspberry/status/"

    data = {'status': True}  # Convert boolean to 'true' or 'false'


    token = "781bed26e3942f9211bd549ce86e3650d3ea2380"  # Replace with the actual token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',  # Ensure JSON data
    }
    data = {
        'status': str(is_online).lower()
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("User status updated successfully.")
        else:
            print(f"Failed to update status. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    update_user_status(True)