import re, datetime

# 解答に必要なパラメータを変数に代入
logfile = './testlog1.log'   # 読み込むログファイルのパス

class Server:
    def __init__(self, name):
        self.name = name
        self.time_list = []
        self.status_list = []
        self.status_tf_list = []


    def find_mulfunction(self):
        start = 0
        end = 0
        stopping = False
        for i in range(len(self.status_list)):
            if self.status_list[i] == '-':
                if stopping == False:
                    start = i
                if i == len(self.status_list) - 1:
                    end = i
                    for j in range(start, end+1):
                        self.status_tf_list[j] = True
                stopping = True
            if stopping and self.status_list[i] != '-':
                end = i
                stopping = False
                for i in range(start, end):
                    self.status_tf_list[i] = True

def get_mulfunction_period(status_tf_list, time_list):
    # 次のfor文の中でstatus_tf_listのi-1の要素がTrueの時にstopping=Trueとして、Trueの値が連続していることを一時記憶させる
    stopping = False 
    start = 0
    end = 0
    mulfunction_period_list = []
    for i in range(len(status_tf_list)):
        # i番目で故障が開始した時の処理
        if status_tf_list[i]:
            if stopping == False:
                start = i
                stopping = True
        # i-1番目(以前)が故障中でi番目で故障が終了した時の処理
        elif stopping:
            end = i
            stopping = False
            # 最終ログ観測日時に故障中の場合のみnow=True
            now = False
            period = [time_list[start], time_list[end], now]
            mulfunction_period_list.append(period)
            stopping = False
        # i番目が故障中であり、かつ最後のログ観測日時である場合の処理
        if i == len(status_tf_list) - 1 and status_tf_list[i]:
            end = i
            now = True
            period = [time_list[start], time_list[end], now]
            mulfunction_period_list.append(period)
    return mulfunction_period_list



with open(logfile, 'r', encoding='UTF-8') as file:
    data = file.readlines()

# ログに書かれている全てのCIDR表記部分を取得
servers = [re.search(r',(.+),', line).group(1) for line in data]
servers = set(servers)

server_dict = {}

# 全てのサーバーインスタンスの作成と辞書管理
for server in servers:
    server_dict[server] = Server(name=server)

# サーバーインスタンスの属性の値を代入
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
    # serverのstatus_tf_listの各要素に故障中の時刻に相当する部分にTrueを入れる
    server.find_mulfunction()
    # serverの故障の開始日時と終了日時の情報が入ったリストを得る
    periods = get_mulfunction_period(server.status_tf_list, server.time_list)
    if periods:
        print(f'サーバー {server.name} が故障しました')
        for period in periods:
            if period[2]:
                print(f'    故障期間: {period[0]}から現在')
            else:
                print(f'    故障期間: {period[0]}から{period[1]}')
        print()