#!D:\Python\Python312\python.exe

import sys
import cgi
import os
import datetime
import urllib.parse
import re #正規表現

import conf
import sub_def

sys.stdout.reconfigure(encoding='utf-8')
#自動でutf-8にエンコードされて出力される

Conf = conf.Conf

#================#
# 設定変数の定義 #

# スクリプト名
mycgi = "bbs.py"

# ログファイル名
logfile = "./" + Conf["datadir"] + "/bbslog.log"

# ログの保存行数
maxlog = 50

# 発言文字色
msgcol = ('#000000','#ff0000','#008000','#000080','#0080ff','#9400d3','#cd5c5c')

#==========#
# 発言処理 #

FORM = cgi.FieldStorage()

# 本文が入力されていたら書き込み
if ("bbs_txt" in FORM) :
	txt = urllib.parse.unquote(FORM["bbs_txt"].value)
	txt = re.sub("[<, >,\r ,\n,]","-",txt)
	if ("color" in FORM) :
		color = urllib.parse.unquote(FORM["color"].value)
	else :
		color = "#000000"

	if (len(txt) > 60) :
		sub_def.error("60文字以下でお願いします")

	cookie = sub_def.get_cookie()

	time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	# 追加するログデータの作成
	newlog = f"""<hr><font color="{color}"><b>{cookie["in_name"]}</b> > {txt} <font size="1">--{time}</font></font>\n"""

	if not (os.path.exists(logfile)):
		with open(logfile, mode='w', encoding="utf-8_sig") as f:
			f.write("")
	with open(logfile, encoding="utf-8_sig") as f:
		log = f.readlines()

	# 先頭に新規ログデータを追加
	log.insert(0,newlog)

	# 保存行数を超える分末尾を削除
	while (len(log) > maxlog) :
		del log[-1]

	# 更新されたデータでログファイルに上書き
	with open(logfile, mode='w', encoding="utf-8_sig") as f:
		log = "".join(log)
		f.write(log)

#==========#
# 出力処理 #

# ログファイル読込
if not (os.path.exists(logfile)):
	with open(logfile, mode='w', encoding="utf-8_sig") as f:
		f.write("")
with open(logfile, encoding="utf-8_sig") as f:
	log = f.read()

# 色選択フォーム作成
	colform = ""
	for msg in msgcol:
		colform += f"""
			<input type=radio name=color value="{msg}"><font color="{msg}">●</font>
		"""

# 出力
html = f"""
	<HTML>
	<HEAD>
	<META HTTP-EQUIV="Content-type" CONTENT="text/html charset=utf-8">
	<title>一行掲示板</title>
	</HEAD>
	<BODY bgcolor="#e6e6fa">
		<form method="post" action="{mycgi}" >
				<input placeholder="発言" name=bbs_txt size=40>
				<button>送信</button>
				<button onclick="window.location.reload();">更新</button>
				<br>{colform}
		</form>
		{log}
	</body>
	</html>
"""

print("Content-Type: text/html\r\n\r\n")

print(html)
sys.exit()
