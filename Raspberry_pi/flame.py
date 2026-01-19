import asyncio
import requests
from bleak import BleakScanner, BleakClient

# ------------------ ThingSpeak settings ------------------
THINGSPEAK_WRITE_KEY = "HITKR226V904U31A"
THINGSPEAK_CHANNEL_ID = "3231008"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ------------------ Arduino BLE UUID ------------------
DATA_UUID = "19B10001-E8F2-537E-4F6C-D104768A1216"

async def main():
    print("--- Searching for UNO_R4_FIRE (Make sure Serial Monitor is closed) ---")
    device = await BleakScanner.find_device_by_name("UNO_R4_FIRE", timeout=15.0)

    if not device:
        print("? Device not found. Power cycle the Arduino if needed.")
        return

    async with BleakClient(device) as client:
        print(f"? Connected to {device.address}")

        def notification_handler(sender, data):
            try:
                # Clean the incoming data
                msg = data.decode('utf-8').strip().split('|')
                if len(msg) >= 5:
                    status, temp, gas, hum, flame = [x.strip() for x in msg]
                    flame_label = "FLAME!" if flame == "1" else "Safe"
                    print(f"[{status}] T:{temp}C | H:{hum}% | Gas:{gas} | Flame:{flame_label}")

                    # ------------------ Send to ThingSpeak ------------------
                    payload = {
                        "api_key": THINGSPEAK_WRITE_KEY,
                        "field1": status,
                        "field2": temp,
                        "field3": gas,
                        "field4": hum,
                        "field5": flame
                    }
                    try:
                        r = requests.get(THINGSPEAK_URL, params=payload, timeout=5)
                        if r.status_code == 200:
                            print("? Data uploaded to ThingSpeak")
                        else:
                            print(f"? ThingSpeak error: {r.status_code}")
                    except Exception as e:
                        print("? Exception sending to ThingSpeak:", e)
            except Exception as e:
                print("? Error parsing BLE data:", e)

        # Subscribe to notifications
        await client.start_notify(DATA_UUID, notification_handler)

        print("? Listening for BLE notifications... Press Ctrl+C to stop.")
        # Keep running while BLE is connected
        while True:
            if not client.is_connected:
                print("! BLE disconnected")
                break
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping...")
