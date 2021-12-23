import re, datetime, ipaddress

# 解答に必要なパラメータを変数に代入
logfile = './testlog4.log'   # 読み込むログファイルのパス
n = 1   # n回連続してタイムアウトする時故障とみなす

class Server:
    def __init__(self, name, subnet):
        self.name = name
        self.time_list = []
        self.status_list = []
        self.subnet = subnet
        self.status_tf_list = []

    def find_mulfunction(self, n):
        start = 0
        end = 0
        stopping = False
        for i in range(len(self.status_list)):
            if self.status_list[i] == '-':
                if stopping == False:
                    start = i
                if i == len(self.status_list) - 1:
                    end = i
                    if (end + 1) - start >= n:
                        for j in range(start, end+1):
                            self.status_tf_list[j] = True
                stopping = True
            if stopping and self.status_list[i] != '-':
                end = i
                stopping = False
                if end - start >= n:
                    for i in range(start, end):
                        self.status_tf_list[i] = True

class Subnet:
    def __init__(self, name):
        self.name = name
        self.subnet_time_list = []
        self.server_status = []
        self.server_list = []


def get_mulfunction_period(status_tf_list, time_list):
    stopping = False
    start = 0
    end = 0
    mulfunction_period_list = []
    for i in range(len(status_tf_list)):
        if status_tf_list[i]:
            if stopping == False:
                start = i
                stopping = True
        elif stopping:
            end = i
            stopping = False
            now = False
            period = [time_list[start], time_list[end], now]
            mulfunction_period_list.append(period)
            stopping = False
        if i == len(status_tf_list) - 1 and status_tf_list[i]:
            end = i
            now = True
            period = [time_list[start], time_list[end], now]
            mulfunction_period_list.append(period)
    return mulfunction_period_list

with open(logfile, 'r', encoding='UTF-8') as file:
    data = file.readlines()

servers = [re.search(r',(.+),', line).group(1) for line in data]
servers = set(servers)

server_dict = {}

# 全てのサーバーインスタンスの作成と辞書管理
for server in servers:
    server_dict[server] = Server(name=server, subnet=ipaddress.ip_interface(server).network)

# サーバーインスタンスに初期属性の値を代入
for server in server_dict.values():
    for line in data:
        if server.name in line:
            time = line[0:14]
            time = datetime.datetime.strptime(time, '%Y%m%d%H%M%S')
            server.time_list.append(time)
            status = re.search(r'.*,(.+)$', line).group(1)
            server.status_list.append(status)
            server.status_tf_list.append(None)


subnets = {ipaddress.ip_interface(server).network for server in servers}


subnets_dict = {}
for subnet in subnets:
    subnets_dict[str(subnet)] = Subnet(name=subnet)

# 各Subnetインスタンスにserver_listとsubnet_time_listの値を持たせる
for subnet in subnets_dict.values():
    for server in server_dict.values():
        if server.subnet == subnet.name:
            subnet.server_list.append(server)
    subnet.subnet_time_list = subnet.server_list[0].time_list



for subnet in subnets_dict.values():
    # 各subnetインスタンスに属するserverごとにサーバーの故障を表示
    for server in subnet.server_list:
        server.find_mulfunction(n)
        periods = get_mulfunction_period(server.status_tf_list, server.time_list)
        if periods:
            print(f'サーバー{server.name}が故障しました')
            for period in periods:
                if period[2]:
                    print(f'    故障期間: {period[0]}から現在')
                else:
                    print(f'    故障期間: {period[0]}から{period[1]}')
            print()
    # Subnetインスタンスのsubnet_status_list属性の値を持たせる
    # subnetに属する全てのサーバーが故障中の位置にのみTrueが残る
    subnet.subnet_status_list = [True] * len(server.status_list)
    for server in subnet.server_list:
        for i in range(len(server.status_tf_list)):
            subnet.subnet_status_list[i] = subnet.subnet_status_list[i] and server.status_tf_list[i]

    if True in subnet.subnet_status_list:
        periods = get_mulfunction_period(subnet.subnet_status_list, subnet.server_list[0].time_list)
        if periods:
            print(f'サブネット{subnet.name}が故障しました')
            for period in periods:
                if period[2]:
                    print(f'    故障期間: {period[0]}から現在')
                else:
                    print(f'    故障期間: {period[0]}から{period[1]}')
            print()
    print()