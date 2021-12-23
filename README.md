# answers

プログラミング試験の答案です。  
設問の問題番号と答案のファイル名の番号が対応しています。　　


### 設問1  
実行方法  
answer1.pyを開いて変数logfileに読み込むログファイルのパスを入力して実行します。   

内容  
ログファイルを開いて行ごとに読みこんだ後、正規表現などを使ってサーバーのCIDR表記、確認日時、応答時間の値を抽出します。  
得られたサーバーのCIDR表記の値を使ってServerクラスのインスタンスを作成します。  
サーバーインスタンスにはそのサーバーの確認日時のリスト(time_list)、応答時間のリスト(status_list)、故障状態かどうかの真偽値のリスト(status_tf_list)を持たせます。それぞれのリストの長さは等しく、応答時間と故障状態のリストのi番目の要素はそのサーバーのi番目の確認日時における応答時間と故障状態の真偽に対応します。故障状態でTrueを入れます。   
status_tf_listとtime_listを関数get_mulfunction_periodに入れて以下の構造のリストを返すようにします。  

[ [[故障開始日時,故障終了日時], True または False ], [故障開始日時,故障終了日時], True または False ], 　・・・ ]   

内側のリストの最後の真偽値要素は最後のログの確認時刻において故障中であった場合にのみTrueを入れてます。最後の結果の出力をする時に使います。  
最後に前の手順で得られたリストをfor文を使って出力します。内側のリストの最後の真偽値がTrueの時は故障終了日時は出力せずに故障開始日時と文字列'現在まで'を出力します。


### 設問2  
実行方法  
answer2.pyを開いて変数logfileに読み込むログファイルのパスを入力、変数nに何回連続してタイムアウトの場合故障とみなすかを入力して実行します。  

内容  
サーバーのstatus_listからstatus_tf_listを作成するfind_mulfunctionに引数nを加えて処理を書き換えます。  
status_listで'-'がn回以上連続した時のみstatus_tf_listにTrueを入れます。  
後の処理は設問1と同様です。

### 設問3
実行方法  
answer3.pyを開いて変数に値を入力して実行します。  
- logfile: 読み込むログファイルのパス  
- n: 何回連続してタイムアウトの場合故障とみなすか
- m: 直近何回の応答時間平均を求めるか
- t: 応答時間平均が何ミリ秒を超える時高負荷状態とみなすか  

内容  
高負荷状態とは直近m回の応答時間平均がtミリ秒を超える結果が得られた時の確認日時から開始し、直近m回の応答時間平均がtミリ秒以下になる結果が得られた時の確認日時までとする。  
関数get_n_meanを定義する。サーバーのsatus_listとmとtを引数として入れてmean_status_tf_listを返す。  
mean_status_tf_listは前問のstatus_tf_listと同様の考え方のリストで、長さはサーバーのログファイルの行数に等しく、高負荷状態の時にのみTrueが入る。　　
得られたmean_status_tf_listを前問と同じように関数get_mulfunction_periodに入れる。以下の出力処理は前問と同様にする。  

### 設問4  
実行方法  
answer4.pyを開いて変数logfileに読み込むログファイルのパスを入力、変数nに何回連続してタイムアウトの場合故障とみなすかを入力して実行します。  

内容  
同一のサブネットに属するサーバー間の確認日時のズレは数秒以内に収まると仮定し、サブネットの故障とみなされるときに出力される故障期間はそのサブネットに属するサーバーの内のどれか一つの確認日時で代表させる。  
CIDR表記からpythonのipaddressモジュールを使ってログファイルのデータ中に登場するサブネットを得る。各サブネットインスタンスに自分の属するサブネットの属性の値を持たせる。
'''ipaddress.ip_interface('CIDR').network'''
