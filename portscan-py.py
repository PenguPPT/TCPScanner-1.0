import socket
import time

host = '192.168.1.4'
ports = range(1, 1024)
open_ports = []
closed_ports = []
start_time = time.time()

print(f'Target {host}')
print(f'Ports {ports[0]}-{ports[-1]}')

for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        s.connect((host, port))
        open_ports.append(port)
        print(f'Port {port} Open')
    except (ConnectionRefusedError, socket.timeout):
        closed_ports.append(port)
    except PermissionError:
        pass
    finally:
        s.close()

print(f'Open {len(open_ports)}')
print(f'Close {len(closed_ports)}')
print(f'Duration {time.time() - start_time} secs')
