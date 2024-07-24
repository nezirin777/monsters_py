
Conf = {}

Conf["top_url"] = "./monster.py"
Conf["cgi_url"] = "./login.py"
Conf["kanri_url"] = "./kanri.py"
Conf["reg_url"] = "./register.py"

Conf["ver"] = "Ver1.8改 vips_3.0"

# ************* 変更する所はここから *******************
# 管理用マスターネーム ※他人に知られてはいけない
Conf["master_name"] = ""
# 管理用マスターパスワード ※他人に知られてはいけない
Conf["master_password"] = ""
# 暗号化用秘密キー ※他人に知られてはいけない
Conf["secret_key"] = ""

#ホームページ
Conf["homepage"] = "../../"
Conf["home_title"] = "おくたのCGIゲームス"

# ファイルのロック(Mkdir = 2,Symlink=1,No = 0)
#Conf["lockkey"] = 2
# ロックファイル名＆パス
Conf["lockfile"] = "./mons.lock"

# データ格納フォルダ（適当な名前を付けてください）
Conf["datadir"] = "save"

# 画像へのパス
# 実際に画像が入ってるフォルダ名まで
Conf["imgpath"] = "./img"

# 参加人数を設定（30人以下推奨）
Conf["sankaMAX"] = 200  # (参加総数の設定です)
Conf["maxshow"] = 30  # (TOP画面に表示される数です。)

# データ保存期間
Conf["goodbye"] = 45

# 初期レベルＵＰ値
Conf["nextup"] = 10
# 戦闘可能ラウンド数（5以下）
Conf["maxround"] = 5
# 戦闘後何秒後に戦闘できるか 30 = 30秒後
Conf["nextplay"] = 10
# 配合を許可するレベル
Conf["haigoulevel"] = 10
# 配合料金（配合回数×Conf["Mmoney"]）Gになります
Conf["Mmoney"] = 100

# バックアップをとるか とる=1 とらない=0
Conf["backup"] = 1
# バックアップ用フォルダ（適当な名前を付けてください）
Conf["backfolder"] = "backup"

# 性別
Conf["sex"] = ["陰" ,"陽"]

# 重複チェックをする時は=1 しない時は=0
Conf["iplog"] = 0


# アクセスを禁止するIPを入力して下さい
#【例 127.0.0.1の場合は ("127.0.0")と書いて下さい)
# 複数の設定の場合は("127.0.0","211.56.108","61.123.45")の様に,をはさんで" "で囲み入力して下さい。
#アクセス制限をかけない時は必ず半角スペース(" ")を入力しておいて下さい。
noip = [" "]


#以下管理画面から書き換えあり。

#異世界最深部
Conf["isekai_max_limit"] = 190

#イベント発生しているか
Conf["event_boost"] = 0

############################ 設定はここまで ########################
1
