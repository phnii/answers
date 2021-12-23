import re, datetime

# 解答に必要なパラメータを変数に代入
logfile = './testlog3.log'   # 読み込むログファイルのパス
n = 2   # n回連続してタイムアウトする時故障とみなす
m = 2   # 直近m回の応答時間の平均が、
t = 4   # tミリ秒を超える時高負荷状態にあるとみなす

class Server:
    def __init__(self, name):
        self.name = name
        self.time_list = []
        self.status_list = []
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

# 直近m個の応答時間の平均を求めてリストに収納し、応答時間平均とパラメータtを比較して負荷状態と判定された位置にTrueを置いたリストを返す
def get_n_mean(status_list, m, t):
    mean_list = [None] * len(status_list)
    for i in range(m-1, len(status_list)):
        sum = 0
        counter = 0
        for j in range(i-m+1, i+1):
            if status_list[j] != '-':
                sum += int(status_list[j])
            else:
                counter += 1
        if m - counter > 0: # n=counterつまり直近n回すべてタイムアウトの場合過負荷状態とは出力しない
            mean_list[i] = sum / (m - counter)
    
    mean_status_tf_list = [None] * len(status_list)
    for i in range(len(mean_list)):
        if mean_list[i] != None:
            if mean_list[i] > t:
                mean_status_tf_list[i] = True #過負荷状態でTrue
            elif mean_list[i] <= t:
                mean_status_tf_list[i] = False #平均応答時間がt以下の時False
    return mean_status_tf_list


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
    server_dict[server] = Server(name=server)

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


for server in server_dict.values():
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
print('--------------------------------------------------------------')
for server in server_dict.values():
    mean_status_tf_list = get_n_mean(server.status_list, m, t)
    # 故障期間を求めるget_mulfunction_periodの関数を流用
    overload_periods = get_mulfunction_period(mean_status_tf_list, server.time_list)
    if overload_periods:
        print(f'サーバー{server.name}が高負荷状態になりました')
        for period in overload_periods:
            if period[2]:
                print(f'    高負荷期間: {period[0]}から現在')
            if period[2] == False:
                print(f'    高負荷期間: {period[0]}から{period[1]}')
        print()