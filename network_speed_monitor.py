import os
import psutil
import time
import pyfiglet

def get_network_stats(interval=1):
    network_stats1 = psutil.net_io_counters()
    time.sleep(interval)
    network_stats2 = psutil.net_io_counters()

    bytes_sent = network_stats2.bytes_sent - network_stats1.bytes_sent
    bytes_received = network_stats2.bytes_recv - network_stats1.bytes_recv

    return bytes_sent, bytes_received

def calculate_network_speed(bytes_sent, bytes_received, interval):
    upload_speed = (bytes_sent * 8) / (interval * 1024)  # Kbps
    download_speed = (bytes_received * 8) / (interval * 1024 * 1024)  # Mbps

    return upload_speed, download_speed

def styled_text(text, style):
    return f"\033[{style}m{text}\033[0m"

def custom_heading(text):
    custom_figlet = pyfiglet.Figlet()
    return custom_figlet.renderText(text)

if __name__ == "__main__":
    interval = 1  # Measurement interval in seconds
    total_upload = 0  # Initialize total_upload to 0
    total_download = 0  # Initialize total_download to 0
    last_update_time = time.time()

    try:
        while True:
            current_time = time.time()
            if current_time - last_update_time >= interval:
                bytes_sent, bytes_received = get_network_stats(interval)
                upload_speed, download_speed = calculate_network_speed(bytes_sent, bytes_received, interval)

                total_upload += bytes_sent / 1024 / 1024  # Update total upload in MB
                total_download += bytes_received / 1024 / 1024  # Update total download in MB

                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console screen

                # Print the custom heading and styled data with a margin
                heading = custom_heading("Network Monitor")
                print(styled_text(heading, "1;36;40"))
                print(f"\n{styled_text('Network Usage:', '1;32;40')}\n")
                print(f"Total Upload: {styled_text(f'{total_upload:.2f} MB', '1;34;40')}")
                print(f"Total Download: {styled_text(f'{total_download:.2f} MB', '1;34;40')}")
                print(f"Current Upload Speed: {styled_text(f'{upload_speed:.2f} Kbps', '1;33;40')}")
                print(f"Current Download Speed: {styled_text(f'{download_speed:.2f} Mbps', '1;33;40')}")
                print(f"\nMade with ❤️ by {styled_text('Harindu Jayakody', '1;35;40')}")
                print(f"GitHub: {styled_text('https://github.com/harindujayakody/network-monitor', '1;36;40')}")
                print("\nPress Ctrl+C to exit gracefully.")

                last_update_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        print(styled_text("\nExiting...", "1;31;40"))
