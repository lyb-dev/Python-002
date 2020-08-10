import sys, getopt, platform, subprocess, socket, json
from concurrent.futures import ThreadPoolExecutor


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0


def ping_checking(ips, corePoolSize):
    with ThreadPoolExecutor(corePoolSize) as executor:
        futures = []
        for ip in ips:
            future = executor.submit(ping, ip)
            futures.append(future)
    ping_success_ip = []
    for idx, ip in enumerate(ips):
        if futures[idx].result():
            ping_success_ip.append(ip)
    print(ping_success_ip)
    return ping_success_ip


def socket_con(host, port):
    s = None
    try:
        # 创建一个socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        s.connect((host, port))
        print("tcp open port:" + str(port))
        return True
    except:
        print("tcp closed port:" + str(port))
        return False
    finally:
        if s is not None:
            s.close()


def tcp_checking(ips, core_pool_size):
    result = {}
    with ThreadPoolExecutor(core_pool_size) as executor:
        for ip in ips:
            futures = []
            ports = list(range(9090, 9093))
            for port in ports:
                future = executor.submit(socket_con, ip, port)
                futures.append(future)
            tcp_success_port = []
            for idx, port in enumerate(ports):
                if futures[idx].result():
                    tcp_success_port.append(port)
            result[ip] = tcp_success_port
        print(result)
    return result


def scan(argv):
    try:
        print(argv)
        opts, args = getopt.getopt(argv, 'n:f:w:', ['ip='])
    except getopt.GetoptError:
        print('python host_scanner.py -n 4 -f ping -w result.json --ip 192.168.2.1')
    print(opts)
    params = {}
    for opt, arg in opts:
        if opt == '-n':
            params['concurrency'] = arg
        elif opt == '-f':
            params['mode'] = arg
        elif opt == '-w':
            params['file'] = arg
        elif opt == '--ip':
            params['ip'] = arg
    ip = params.get('ip')
    ips = str(ip).split('-')
    core_pool_size = int(params.get('concurrency'))
    json_result = ''
    if params.get('mode') == 'ping':
        result = ping_checking(ips, core_pool_size)
        json_result = json.dumps(result)
    elif params.get('mode') == 'tcp':
        result = tcp_checking(ips, core_pool_size)
        json_result = json.dumps(result)
    f = open(str(params.get('file')), 'w')
    f.write(json_result)


scan(['-n', '4', '-f', 'ping', '-w', 'result.json', '--ip', '192.168.2.16-192.168.2.26'])
# tcp_checking(['192.168.2.16'], 4)
