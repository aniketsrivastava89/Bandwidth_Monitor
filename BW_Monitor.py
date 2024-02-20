import psutil
import subprocess
import re
import datetime
import time


def get_network_interface_name():
    # Use PowerShell to get the network interface name on Windows
    cmd = 'Get-NetAdapter | Select-Object -ExpandProperty InterfaceDescription'
    process = subprocess.Popen(['powershell.exe', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    output = output.decode('utf-8').strip()
    # Use regex to extract the interface name from the output
    match = re.search(r'Realtek PCIe GbE Family Controller|Realtek RTL8822CE 802.11ac PCIe Adapter', output, re.IGNORECASE)
    if match:
        return match.group(0)
    return None



def log_bandwidth(interface, interval=1, duration=10):
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=duration)

    with open('bandwidth_log.txt', 'a') as file:
        file.write(f"Bandwidth Log for Interface {interface}\n")
        file.write("Timestamp,Bytes Sent,Bytes Received\n")

        while datetime.datetime.now() < end_time:
            stats = psutil.net_io_counters(pernic=True)
            if interface in stats:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                bytes_sent = stats[interface].bytes_sent
                bytes_recv = stats[interface].bytes_recv
                file.write(f"{timestamp},{bytes_sent},{bytes_recv}\n")
                time.sleep(interval)

if __name__ == '__main__':
    interface = get_network_interface_name()
    if interface:
        print(f"Monitoring bandwidth for interface: {interface}")
        log_bandwidth(interface, interval=1, duration=10)
    else:
        print("Unable to determine network interface name.")
