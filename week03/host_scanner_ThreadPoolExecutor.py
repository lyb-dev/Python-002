import sys, getopt, platform, subprocess, socket, json, time
from concurrent.futures import ThreadPoolExecutor


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0


def ping_checking(ips, workers):
    with ThreadPoolExecutor(workers) as executor:
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


def tcp_checking(ips, workers):
    result = {}
    with ThreadPoolExecutor(workers) as executor:
        for ip in ips:
            futures = []
            ports = list(range(1, 1024))
            # ports = [80]
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


def get_args(argv):
    try:
        print(argv)
        opts, args = getopt.getopt(argv, 'n:f:w:', ['ip='])
    except getopt.GetoptError:
        print('python host_scanner_ThreadPoolExecutor.py -n 4 -f ping -w result.json --ip 192.168.2.1')
        sys.exit(2)
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
    return params


def ip_format(ip_segment):
    ipx = str(ip_segment).split('-')

    ip2num = lambda x: sum([256 ** i * int(j) for i, j in enumerate(x.split('.')[::-1])])

    num2ip = lambda x: '.'.join([str(x // (256 ** i) % 256) for i in range(3, -1, -1)])

    a = [num2ip(i) for i in range(ip2num(ipx[0]), ip2num(ipx[1]) + 1) if not ((i + 1) % 256 == 0 or (i) % 256 == 0)]

    print(a)
    return a


def scan(argv):
    start_time = time.time()
    # 获取运行参数
    params = get_args(argv)
    mode = params.get('mode')
    ip_segment = params.get('ip')
    if '-' in ip_segment:
        ips = ip_format(ip_segment)
    else:
        ips = [ip_segment]
    workers = int(params.get('concurrency'))
    file_name = str(params.get('file'))
    json_result = ''
    # 执行扫描
    if mode == 'ping':
        result = ping_checking(ips, workers)
        json_result = json.dumps(result)
    elif mode == 'tcp':
        result = tcp_checking(ips, workers)
        json_result = json.dumps(result)
    # 保存结果
    f = open(file_name, 'w')
    f.write(json_result)

    cost_time = time.time() - start_time
    print('-------cost time:' + str(cost_time))


# scan(['-n', '4', '-f', 'ping', '-w', 'result.json', '--ip', 'www.baidu.com'])

if __name__ == '__main__':
    scan(sys.argv[1:])
