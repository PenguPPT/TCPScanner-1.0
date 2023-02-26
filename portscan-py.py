import asyncio
import socket
import time

def get_router_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 1))
        return s.getsockname()[0]

async def port_scanner(host, port):
    try:
        conn = asyncio.open_connection(host, port)
        _, writer = await asyncio.wait_for(conn, timeout=1)
        writer.close()
        return True
    except:
        return False

async def scan_ports(host, ports):
    tasks = []
    open_ports = []
    closed_ports = []
    for port in ports:
        tasks.append(asyncio.create_task(port_scanner(host, port)))
    results = await asyncio.gather(*tasks)
    for port, status in zip(ports, results):
        if status:
            open_ports.append(port)
        else:
            closed_ports.append(port)
    return open_ports, closed_ports

loop = asyncio.get_event_loop()
def main():
    host = get_router_ip()
    start_time = time.time()
    ports = range(1, 1024)
    chunk_size = 1024
    open_ports = []
    closed_ports = []
    print(f'Target {host}')
    print(f'Ports {ports[0]}-{ports[-1]}')
    for i in range(0, len(ports), chunk_size):
        open, closed = loop.run_until_complete(scan_ports(host, ports[i:i+chunk_size]))
        open_ports.extend(open)
        closed_ports.extend(closed)
    print("Open ports:")
    for port in open_ports:
        print(f'Port {port} Open')
    print(f'Open {len(open_ports)}')
    print(f'Close {len(closed_ports)}')
    print(f'Duration {time.time() - start_time} secs')
    

if __name__ == '__main__':
    main()
