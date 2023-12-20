import os
import psutil
import time
import pyfiglet

LOG_FILE = "data_usage_log.txt"
TOTALS_FILE = "data_totals.txt"

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

def read_last_session_totals():
    total_upload = 0
    total_download = 0

    if os.path.exists(TOTALS_FILE):
        with open(TOTALS_FILE, "r") as totals_file:
            lines = totals_file.readlines()
            if lines:
                last_line = lines[-1]
                parts = last_line.split(',')
                if len(parts) >= 2:
                    total_upload_str = parts[0].split(':')[-1].strip()
                    total_download_str = parts[1].split(':')[-1].strip()

                    try:
                        total_upload = float(total_upload_str) if total_upload_str.replace('.', '').isdigit() else 0
                        total_download = float(total_download_str) if total_download_str.replace('.', '').isdigit() else 0
                    except ValueError as e:
                        print(f"Error converting values to float: {e}")

    return total_upload, total_download

def save_totals(total_upload, total_download):
    with open(TOTALS_FILE, "a") as totals_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        totals_file.write(f"{timestamp} - Upload: {total_upload:.2f} MB, Download: {total_download:.2f} MB\n")

def reset_totals_if_new_day(last_reset_time, current_time):
    last_reset_date = time.strftime("%Y-%m-%d", time.localtime(last_reset_time))
    current_date = time.strftime("%Y-%m-%d", time.localtime(current_time))

    return last_reset_date != current_date

def reset_totals():
    return 0, 0

def save_data_usage(total_upload, total_download):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - Total Upload: {total_upload:.2f} MB, Total Download: {total_download:.2f} MB\n")

def display_last_closed_totals():
    print("\nLast Closed Totals:")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            lines = log_file.readlines()
            if lines:
                last_line = lines[-1]
                print(last_line.strip())
    else:
        print("No recorded totals found.")

if __name__ == "__main__":
    interval = 1  # Measurement interval in seconds
    total_upload, total_download = read_last_session_totals()
    last_update_time = time.time()
    last_reset_time = time.time()
    last_log_time = time.time()

    try:
        # Display last closed totals when the program starts
        display_last_closed_totals()

        while True:
            current_time = time.time()

            # Reset totals if it's a new day
            if reset_totals_if_new_day(last_reset_time, current_time):
                last_reset_time = current_time
                total_upload, total_download = reset_totals()

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

                # Save totals every hour
                if current_time - last_log_time >= 3600:  # Log every 1 hour (3600 seconds)
                    save_totals(total_upload, total_download)
                    last_log_time = current_time

                last_update_time = current_time

            time.sleep(1)

    except KeyboardInterrupt:
        # Save data usage when the program is closed
        save_data_usage(total_upload, total_download)
        print(styled_text("\nExiting...", "1;31;40"))
