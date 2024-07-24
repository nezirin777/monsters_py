#!D:\Python\Python312\python.exe

import sys
import cgi
import os
import datetime
import shutil
import secrets
import ast

import sub_def
import register
import conf
import cgi_py

Conf = conf.Conf

sys.stdout.reconfigure(encoding='utf-8')
#自動でutf-8にエンコードされて出力される

#==============#
#	チェック	#
#==============#
def admin_check()  :
	in_m_name = FORM["m_name"]
	in_m_pass = FORM["m_password"]

	if (in_m_name == "") : sub_def.error("MASTER_NAMEが有りません","kanri")
	if (in_m_pass == "") : sub_def.error("MASTER_PASSWORDが有りません","kanri")
	if (in_m_name != Conf["master_name"]) : sub_def.error("MASTER_NAMEが違います","kanri")
	if (in_m_pass != Conf["master_password"]) : sub_def.error("MASTER_PASSWORDが違います","kanri")

	return

#==============#
#	戻りボタン	#
#==============#
def kanri_back() :
	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="KANRI">
			<input type="hidden" name="token" value="{FORM["token"]}">
			<button>管理メニューへ</button>
		</form>
		<form action="{Conf["top_url"]}" method="post">
			<input type="hidden" name="mode" value="">
			<button>TOPへ</button>
		</form>
	"""
	print(html)
	sub_def.footer()

#==========#
# リザルト #
#==========#
def result(txt="") :
	h = f"""
		<div id ="result">
			<span>{txt}</span>
		</div>
	"""

	sub_def.header()
	print(h)
	kanri_back()

#==============#
#	管理モード	#
#==============#
def OPEN_K() :
	html = f"""
		<div class="kanri_title">管理モード</div>
		<div class="kanri_login">
			<form method="post">
				MASTER_NAME<br>
				<input type="text" name="m_name"><br>
				MASTER_PASSWORD<br>
				<input type="password" name="m_password"><br>
				<input type="hidden" name="mode" value="KANRI">
				<input type="hidden" name="token" value="{FORM["token"]}">
				<button>管理モード</button>
			</form>
		</div>
	"""
	sub_def.header()
	print(html)
	sub_def.footer()

def KANRI () :
	token = FORM["token"]
	u_list = sub_def.open_user_list()

	txt = ""
	if (u_list) :
		txt = "".join([f"""<option value={key}>{key}</option>\n""" for key in u_list.keys()])

	mente_chek = ""
	if (os.path.exists("mente.mente")) :
		mente_chek = "<div class=\"kanri_title\">メンテナンスモード中</div>"

	event_txt = ""
	if(Conf["event_boost"]) :
		event_txt = "<div class=\"kanri_title\">ブースト発動中!!</div>"

	html = f"""
		<div class="kanri_title">管理モード</div>
		{mente_chek}
		{event_txt}
		<div class="kanri_menu_top">
			<div class="kanri_menu">
				メンテナンスモード
				<br>
				<form method="post" class="flex">
					<button>開始</button>
					<input type="hidden" name="mode" value="MENTE">
					<input type="hidden" name="mente" value="start">
					<input type="hidden" name="token" value="{token}">
				</form>
				<form method="post" class="flex">
					<button>終了</button>
					<input type="hidden" name="mode" value="MENTE">
					<input type="hidden" name="mente" value="stop">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				イベントモード
				<br>
				<form method="post" class="flex">
					<button>ブースト開始</button>
					<input type="hidden" name="mode" value="event_boost">
					<input type="hidden" name="event_boost" value="start">
					<input type="hidden" name="token" value="{token}">
				</form>
				<form method="post" class="flex">
					<button>ブースト終了</button>
					<input type="hidden" name="mode" value="event_boost">
					<input type="hidden" name="event_boost" value="stop">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				cgiからpythonへ移行のデータ変換
				<form method="post">
					<button>実行</button>
					<input type="hidden" name="mode" value="cgi_python">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				datファイル更新<br>(モンスターデータ等)
				<form method="post">
					<button>実行</button>
					<input type="hidden" name="mode" value="dat_update">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				モンスター配布
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象の人を選択</option>
						{txt}
					</select>
					<button>ユーザー決定</button>
					<input type="hidden" name="mode" value="MON_PRESENT">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				お金やメダルを贈る
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象の人を選択</option>
						<option value="全員">全員</option>
						<option value="">------</option>
						{txt}
					</select>
					<br>
					お金   <input class="flex" type=number name="money" size=7 value=0>
					メダル <input class="flex" type=number name="medal" size=7 value=0>
					階層鍵 <input class="flex" type=number name="key" size=7 value=0>
					<button>決定</button>
					<input type="hidden" name="mode" value="PRESENT">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				セーブデータ編集
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象を選択</option>
						<option value="user_list">user_list</option>
						<option value="omiai_list">omiai_list</option>
						<option value="">--↓各ユーザー↓--</option>
						{txt}
					</select>
					<button>決定</button>
					<input type="hidden" name="mode" value="save_edit_select">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				pickleセーブデータ→csv出力
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象を選択</option>
						<option value="user_list">user_list</option>
						<option value="omiai_list">omiai_list</option>
						<option value="">---------</option>
						<option value="全員">全員</option>
						<option value="">---------</option>
						{txt}
					</select>
					<button>決定</button>
					<input type="hidden" name="mode" value="pickle_to">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				csv→pickle変換
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象を選択</option>
						<option value="user_list">user_list</option>
						<option value="omiai_list">omiai_list</option>
						<option value="">---------</option>
						<option value="全員">全員</option>
						<option value="">---------</option>
						{txt}
					</select>
					<button>決定</button>
					<input type="hidden" name="mode" value="csv_to">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				ユーザー登録データ(user_list.pickle)の再構築
				<form method="post">
					<button>復元する</button>
					<input type="hidden" name="mode" value="FUKUGEN">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				再スタート
				<form method="post">
					確認<input type="checkbox" name="Reset_ck" value="on">
					<button>RESTART</button>
					<input type="hidden" name="mode" value="RESTART">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				データ一括削除
				<form method="post">
					確認<input type="checkbox" name="Reset_ck" value="on">
					<button>全部削除</button>
					<input type="hidden" name="mode" value="ALLDEL">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				ルール違反者と思われる人の削除を行います
				<form method="post">
					<select name="target_name">
						<option value="" hidden>対象の人を選択</option>
						{txt}
					</select>
					<br>
					確認<input type="checkbox" name="Del_ck" value="on">
					<button>管理削除</button>
					<input type="hidden" name="mode" value="DEL">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				パスワードの変更 <br>
				<form method="post">
					<select name=target_name>
						<option value="" hidden>対象の人を選択</option>
						{txt}
					</select>
					<br>
					NEWパスワード
					<input type=text name=newpass><br>
					<button>パスワード決定</button>
					<input type="hidden" name="mode" value="NEWPASS">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="kanri_menu">
				重複の対象のためエラーが出る人を新規登録します
				<form method="post">
					登録ユーザー名<input type=text name=make_name ><br>
					登録パスワード<input type=password name=make_password><br>
					<button>管理登録</button>
					<input type="hidden" name="mode" value="NEW">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>
		</div>
	"""

	sub_def.header()
	print(html)
	sub_def.footer()

#====================#
# メンテナンスモード   #
#====================#
def MENTE () :
	if (FORM["mente"] == "start") :
		os.makedirs("mente.mente")
		txt = "メンテナンスモードに入りました。"
	else :
		if (os.path.exists("mente.mente")):
			os.rmdir("mente.mente")
		txt = "メンテナンスモードを終了しました。"
	result(txt)

#========================#
# イベントブーストモード   #
#========================#
def event_boost () :
	import fileinput
	import re

	if (FORM["event_boost"] == "start") :
		val = 1
		txt = "イベントブーストモードに入りました。"
	else :
		val = 0
		txt = "イベントブーストモードを終了しました。"

	with fileinput.FileInput("conf.py", inplace=True, backup=".bak" ,encoding="utf-8") as f:
		for line in f:
			print(re.sub(r"Conf\[\"event_boost\"\] = \d" ,f"Conf[\"event_boost\"] = {val}" ,line ), end="")

	result(txt)

#=========#
# 強制登録 #
#=========#
def NEW () :
	register.sinki(FORM["make_name"],FORM["make_password"],1)
	kanri_back()

#================#
# パスワード変更  #
#================#
def NEWPASS () :
	target_name = FORM.get("target_name")
	newpass = FORM.get("newpass")

	if not(target_name) : sub_def.error("対象ユーザーが選択されていません。","kanri")
	if not(newpass) : sub_def.error("新しいパスワードが入力されていません。","kanri")

	crypted = sub_def.pass_encode(newpass)
	u_list = sub_def.open_user_list()
	user = sub_def.open_user(target_name)

	user["pass"] = crypted
	u_list[target_name]["pass"] = crypted

	sub_def.save_user_list(u_list)
	sub_def.save_user(user,target_name)

	result(f"管理モードで<span>{target_name}</span>のパスワードを変更しました")

#=============#
# ユーザー削除 #
#=============#
def DEL () :
	target_name = FORM.get("target_name")

	if (FORM.get("Del_ck") != "on") : sub_def.error("確認チェックがONになっていません。","kanri")
	if not(target_name) : sub_def.error("対象ユーザーが選択されていません。","kanri")

	u_list = sub_def.open_user_list()

	sub_def.delete_user(target_name)
	del u_list[target_name]

	sub_def.save_user_list(u_list)

	result(f"<span>{target_name}</span>を管理モードで強制削除しました")

#=================#
# saveフォルダ削除 #
#=================#
def data_del() :
	sub_def.backup()

	shutil.rmtree(Conf["datadir"])
	os.makedirs(Conf["datadir"])

	with open(Conf["datadir"]+"/tournament.log", mode='w',encoding='utf-8') as f:
		f.write("""<div class="medal_battle_title">まだ大会は一度も開かれていません</div><br><br><br>""")

	with open(Conf["datadir"] + "/bbslog.log", mode='w', encoding="utf-8_sig") as f:
		f.write("")

	sub_def.make_user_list()
	sub_def.make_omiai_list()

#===========#
# リスタート #
#===========#
def RESTART () :
	if (FORM.get("Reset_ck") != "on") : sub_def.error("確認チェックがONになっていません。","kanri")

	u_list = sub_def.open_user_list()
	user = [{"name":name, "crypted": v["pass"]} for name,v in u_list.items()]

	data_del()

	for u in user :
		register.make_user_data(in_name=u["name"],crypted=u["crypted"])

	result("ゲームを初期化、リスタートしました。")

#=======#
# 初期化 #
#=======#
def ALLDEL () :
	if (FORM["Reset_ck"] != "on") : sub_def.error("確認チェックがONになっていません。","kanri")

	data_del()

	result("全データを削除しました。")

#====================#
# ユーザーデータ再構築 #
# user_list.pickle    #
#====================#
def FUKUGEN () :
	#セーブデータフォルダ内各ユーザー名取得
	files = os.listdir(Conf["datadir"])
	files_dir = [f for f in files if os.path.isdir(os.path.join(Conf["datadir"], f))]

	bye_day = (datetime.datetime.now() + datetime.timedelta(days=Conf["goodbye"])).strftime("%Y-%m-%d")

	u_list = {}
	for in_name in files_dir :
		user = sub_def.open_user(in_name)
		pt = sub_def.open_party(in_name)

		u_list[in_name] = {
			"pass" 		: user["pass"],
			"host" 		: "",
			"bye"		: bye_day,
			"m1_name"	: pt[0]["name"],
			"m1_hai"	: pt[0]["hai"],
			"m1_lv"		: pt[0]["lv"],
			"m2_hai"	: pt[1]["hai"] if(pt[1:2]) else "",
			"m2_lv"		: pt[1]["lv"] if(pt[1:2]) else "",
			"m2_name" 	: pt[1]["name"] if(pt[1:2]) else "",
			"m3_hai"	: pt[2]["hai"] if(pt[2:3]) else "",
			"m3_lv"		: pt[2]["lv"] if(pt[2:3]) else "",
			"m3_name" 	: pt[2]["name"] if(pt[2:3]) else "",
			"key"		: user["key"],
			"money"		: user["money"],
			"mes"		: user["mes"],
		}

	sub_def.save_user_list(u_list)

	result("ユーザー登録データ(user_list.pickle)を再構築しました。")

#====================#
# モンスター配布      #
#====================#
def MON_PRESENT () :
	target_name = FORM.get("target_name","")

	if(target_name == "") :sub_def.error("対象ユーザーが選択されていません。","kanri")

	M_list = sub_def.open_monster_dat()
	txt = "".join([f"""<option value={name}>{name}</option>\n""" for name in M_list.keys()])

	html = f"""
		<div class="kanri_title">モンスター配布</div>
		<div class="kanri_menu_top">
			<div class="kanri_menu">
				対象ユーザーは<span>{target_name}</span>です
				<form method="post">
					配布モンスター<br>
					<select name="Mons_name">
						<option value="" hidden>選択してください</option>
						{txt}
						</select>
					<br>
					性別
					<br>
					<select name="sex">
						<option value="" hidden>選択してください</option>
						<option value="陰">陰</option>
						<option value="陽">陽</option>
					</select>
					<br>
					MAXレベル
					<br>
					<input type="number" name="max_level"><br>
					配合回数<br>
					<input type="number" name="haigou"><br>
					<button>配布する</button>
					<input type="hidden" name="mode" value="MON_PRESENT_OK">
					<input type="hidden" name="target_name" value="{target_name}">
					<input type="hidden" name="token" value="{FORM["token"]}">
				</form>
			</div>
		</div>
	"""

	sub_def.header()
	print(html)
	kanri_back()

#====================#
# モンスター配布 処理 #
#====================#
def MON_PRESENT_OK () :
	target_name = FORM["target_name"]
	Mons_name	= FORM.get("Mons_name")
	sex			= FORM.get("sex")
	max_level	= int(FORM.get("max_level",0))
	haigou		= int(FORM.get("haigou",0))

	if not(Mons_name) : sub_def.error("モンスターを選択してください","kanri")
	if not(sex)	:sub_def.error("性別を選択してください","kanri")
	if not(max_level)	:sub_def.error("MAXレベルを入力してください","kanri")
	if not(haigou)	: sub_def.error("配合回数を入力してください","kanri")

	party = sub_def.open_party(target_name)

	if (len(party) >= 10) :
		sub_def.error("パーティがいっぱいで追加することができません。","kanri")

	new_mob = sub_def.monster_select(Mons_name,haigou)
	new_mob["lv"] = 1
	new_mob["mlv"] = max_level
	new_mob["sex"] = sex
	new_mob["hai"] = haigou

	party.append(new_mob)
	for i,pt in enumerate(party,1) :
		pt["no"] = i

	sub_def.save_party(party,target_name)

	result(f"{target_name}へモンスターを配布しました")

#====================#
# プレゼント          #
#====================#
def PRESENT () :
	target_name = FORM.get("target_name","")

	money = FORM.get("money","")
	medal = FORM.get("medal","")
	key = FORM.get("key","")

	if (target_name == "") : sub_def.error("ユーザーが選択されていません。","kanri")
	if (money == "" or medal == "" or key == "") : sub_def.error("お金やメダルが入力されていません。","kanri")

	def haifu(name) :
		user = sub_def.open_user(name)
		user["money"] += int(money)
		user["medal"] += int(medal)
		user["key"]  += int(key)
		sub_def.save_user(user,name)

	if (target_name == "全員") :
		u_list = sub_def.open_user_list()
		[haifu(name) for name in u_list.keys()]
	else :
		haifu(target_name)

	result(f"{target_name}にプレゼントを送りました。")

#====================#
# csv → pickle       #
#====================#
def csv_to() :
	#user_listや各種ユーザーデータはpickle変換後csvは削除される
	target_name = FORM.get("target_name")

	if not(target_name) : sub_def.error("対象が選択されていません。","kanri")

	cgi_py.csv_to_pickle.csv_to_pickle(target_name)

	result(f"{target_name}のcsv→pickle変換が完了しました。")

#====================#
# pickle → csv       #
#====================#
def pickle_to() :
	target_name = FORM.get("target_name")

	if not(target_name) : sub_def.error("対象が選択されていません。","kanri")

	sub_def.backup()
	cgi_py.pickle_to_csv.pickle_to_csv(target_name)

	result(f"{target_name}のpickle→csv変換が完了しました。")

#================#
# save_edit      #
#================#
def make_table(save_data) :
	target_name = FORM.get("target_name")
	target_data = FORM.get("target_data")

	tr = ""
	no_edit = ("no" , "name", "pass" , "type" , "m_type" ,"host", "rank" ,"getm")

	th = "".join([f"""<th>{key}</th>""" for key in save_data[0].keys()])

	for i in range(len(save_data)) :
		td = ""
		for key in save_data[0].keys() :
			val = save_data[i][key]
			if (key in no_edit) :
				td += f"""
					<td>{val}</td>
					<input type="hidden" name="{i},{key}" value="{val}">
				"""
			else :
				td += f"""
					<td><input type="text" name="{i},{key}" value="{val}" size=10></td>
				"""
		tr += f"""<tr>{td}</tr>"""

	table = f"""
		<form method="post">
			<table border="1" class="kanri_save_edit_table">
				<tr>{th}</tr>
				{tr}
				<tr>{th}</tr>
			</table>
			<input type="hidden" name="mode" value="save_edit_save">
			<input type="hidden" name="target_name" value="{target_name}">
			<input type="hidden" name="target_data" value="{target_data}">
			<input type="hidden" name="token" value="{FORM["token"]}">
			<button>更新</button>
		</form>
	"""
	return table

def save_editer() :
	target_name = FORM.get("target_name")
	target_data = FORM.get("target_data")

	if not(target_name) : sub_def.error("対象が選択されていません。" , "kanri")

	match target_name :
		case "user_list" :
			save_data = sub_def.open_user_list()
			if not(save_data) :
				sub_def.error("現在登録者はいないようです。<br>編集できません。","kanri")
			save_data = [{"name":u}| v for u,v in save_data.items() ]
			txt = "登録ユーザーリスト"
		case "omiai_list" :
			if not(save_data) :
				sub_def.error("現在お見合い登録者はいないようです。<br>編集できません。","kanri")
			save_data = [{"user":u}| v for u,v in save_data.items() ]
			txt = "お見合いリスト"

	match target_data :
		case "user_data" :
			save_data = sub_def.open_user(target_name)
			txt = "ユーザー情報"
		case "party_data" :
			save_data = sub_def.open_party(target_name)
			txt = "パーティーデータ"
		case "room_key_data" :
			save_data = sub_def.open_room_key(target_name)
			save_data = [{"name":u}|v  for u,v in save_data.items() ]
			txt = "部屋の鍵データ"
		case "waza_data" :
			save_data = sub_def.open_waza(target_name)
			save_data = [{"name":u}|v  for u,v in save_data.items() ]
			txt = "習得特技データ"
		case "zukan_data" :
			save_data = sub_def.open_zukan(target_name)
			save_data = [{"name":u}|v  for u,v in save_data.items() ]
			txt = "図鑑データ"
		case "park_data" :
			save_data = sub_def.open_park(target_name)
			txt = "モンスターパークデータ"
			if not(save_data) :
				sub_def.error("現在パーク内にモンスターはいないようです。<br>編集できません。","kanri")
		case "vips_data" :
			save_data = sub_def.open_vips(target_name)
			txt = "その他データ"

	table = f"""
		<div class="kanri_save_edit_caution">
			データの整合性等のチェックはありません。<br>
			正常に動作しなくなる可能性がありますので<br>
			内容を把握したうえで変更してください。<br>
		</div>
		<div class="kanri_save_edit_title">{txt}</div>
	"""

	if (type(save_data) == list) :
		table += make_table(save_data)
	else :
		table += make_table([save_data])

	sub_def.header()
	print(table)
	kanri_back()

def save_edit_select() :
	target_name = FORM.get("target_name")

	if not(target_name) : sub_def.error("対象が選択されていません。","kanri")

	html = f"""
		<div class="kanri_save_edit_title">
			<form method="post">
				対象ユーザー:{target_name}<br>
				<select name="target_data">
					<option value="" hidden>対象データを選択</option>
					<option value="user_data">ユーザーデータ</option>
					<option value="party_data">パーティデータ</option>
					<option value="room_key_data">所持部屋の鍵データ</option>
					<option value="waza_data">取得特技データ</option>
					<option value="zukan_data">図鑑データ</option>
					<option value="park_data">モンスターパークデータ</option>
					<option value="vips_data">vipsデータ</option>
				</select>
				<button>データ決定</button>
				<input type="hidden" name="mode" value="save_editer">
				<input type="hidden" name="target_name" value="{target_name}">
				<input type="hidden" name="token" value="{FORM["token"]}">
			</form>
		</div>
	"""

	if(target_name == "user_list") :
		save_editer()
	elif(target_name == "omiai_list") :
		save_editer()
	else :
		sub_def.header()
		print(html)
		kanri_back()

def save_edit_save() :
	target_name = FORM["target_name"]
	target_data = FORM["target_data"]

	for key in FORM.keys():
		if(FORM[key].isdecimal()) :
			FORM[key] = int(FORM[key])
		else :
			FORM[key] = FORM[key]

	match target_name :
		case "user_list" :
			txt = "ユーザーリストを更新しました。"
			save_data = sub_def.open_user_list()
			save_data = {FORM[f"{i},name"] : {v : FORM.get(f"{i},{v}","") for v in save_data[FORM[f"{i},name"]].keys()} for i in range(len(save_data)) }

			sub_def.save_user_list(save_data)

		case "omiai_list" :
			txt = "お見合いリストを更新しました。"
			save_data = sub_def.open_omiai_list()
			save_data = {FORM[f"{i},name"] : {v : FORM.get(f"{i},{v}","") for v in save_data[FORM[f"{i},name"]].keys()} for i in range(len(save_data)) }

			sub_def.save_omiai_list(save_data)

	match target_data :
		case "user_data" :
			txt = "ユーザー情報"
			save_data = sub_def.open_user(target_name)
			save_data = {v : FORM[f"0,{v}"] for v in save_data.keys()}
			sub_def.save_user(save_data, target_name)

		case "vips_data" :
			txt = "その他データ"
			save_data = sub_def.open_vips(target_name)
			save_data = {v : FORM[f"0,{v}"] for v in save_data.keys()}
			sub_def.save_vips(save_data, target_name)

		case "room_key_data" :
			txt = "部屋の鍵データ"
			save_data = sub_def.open_room_key(target_name)
			save_data = {FORM[f"{i},name"] : {v : FORM[f"{i},{v}"] for v in save_data[FORM[f"{i},name"]].keys()} for i in range(len(save_data)) }
			sub_def.save_room_key(save_data, target_name)

		case "waza_data" :
			txt = "収得特技データ"
			save_data = sub_def.open_waza(target_name)
			save_data = {FORM[f"{i},name"] : {v : FORM[f"{i},{v}"] for v in save_data[FORM[f"{i},name"]].keys()} for i in range(len(save_data)) }
			sub_def.save_waza(save_data, target_name)

		case "zukan_data" :
			txt = "図鑑データ"
			save_data = sub_def.open_zukan(target_name)
			save_data = {FORM[f"{i},name"] : {v : FORM[f"{i},{v}"] for v in save_data[FORM[f"{i},name"]].keys()} for i in range(len(save_data)) }
			sub_def.save_zukan(save_data, target_name)

		case "party_data" :
			txt = "パーティーデータ"
			save_data = sub_def.open_party(target_name)
			save_data = [ {v : FORM[f"{i},{v}"] for v in save_data[i].keys() } for i in range(len(save_data)) ]
			sub_def.save_party(save_data, target_name)

		case "park_data" :
			txt = "モンスターパークデータ"
			save_data = sub_def.open_park(target_name)
			save_data = [ {v : FORM[f"{i},{v}"] for v in save_data[i].keys() } for i in range(len(save_data)) ]
			sub_def.save_park(save_data, target_name)

	result(f"{target_name}の{txt}を更新しました。")

#================#
# dat_update     #
#================#
def dat_update_check (in_name , M_list , Tokugi_dat) :

	user = sub_def.open_user(in_name)
	zukan = sub_def.open_zukan(in_name)
	waza  = sub_def.open_waza(in_name)

	def zukan_update() :
		new_zukan = {name: {"no":mon["no"],"m_type":mon["m_type"],"get":0} for name,mon in M_list.items()}
		for name,v in zukan.items() :
			new_zukan[name]["get"] = v["get"]

		sub_def.save_zukan(new_zukan,in_name)

		get = len([1 for v in new_zukan.values() if(v.get("get") == 1)])

		mleng = len(new_zukan)
		s = get / mleng * 100
		user["getm"] = f"{get}／{mleng}匹 ({s:.2f}％)"
		sub_def.save_user(user,in_name)

	def waza_update() :
		new_waza = {name:{ "no":v["no"], "type":v["type"], "get":0} for name,v in Tokugi_dat.items()}

		for name,v in waza.items() :
			new_waza[name]["get"] = v["get"]

		sub_def.save_waza(new_waza,in_name)

	if (len(M_list) != len(zukan)) :
		zukan_update()

	if (len(Tokugi_dat) != len(waza)) :
		waza_update()

	return

def dat_file() :
	import pickle
	import pandas as pd
	import glob

	def pickle_dump(obj, path):
		with open(path, mode='wb') as f:
			pickle.dump(obj,f)

	def open_dat(file):
		return pd.read_csv(file, encoding="utf-8_sig",index_col="name").convert_dtypes().fillna("").sort_values("no").to_dict(orient='index')

	files = glob.glob("./dat/*.csv")
	os.makedirs("./dat/pickle", exist_ok=True)

	for f in files :
		fp = f.replace('csv', 'pickle')
		fpp = fp.replace('./dat', './dat/pickle')
		pickle_dump(open_dat(f),fpp)

def dat_update() :
	import fileinput
	import re

	dat_file()

	M_list = sub_def.open_monster_dat()
	Tokugi_dat = sub_def.open_tokugi_dat()

	#異世界最深部設定
	#confファイルを書き換えるので注意！
	isekai_max_limit = max([mon["階層B"] for mon in M_list.values() if(mon["room"] in ("特殊"))])
	with fileinput.FileInput("conf.py", inplace=True, backup=".bak" ,encoding="utf-8") as f:
		for line in f:
			print(re.sub(r"Conf\[\"isekai_max_limit\"\] = \d*" ,f"Conf[\"isekai_max_limit\"] = {isekai_max_limit}" ,line ), end="")

	u_list = sub_def.open_user_list()
	for name in u_list.keys() :
		dat_update_check(name , M_list ,Tokugi_dat)

	result("datファイルの更新を反映しました。")

#================#
# cgi_python     #
#================#
def cgi_python() :
	dat_file()
	cgi_py.cgi_python.cgi_python()

	result("python環境へデータ変換しました。")

#============================================================#

def token_check():
	session = sub_def.get_session()

	if(FORM.get("token")) :
		if not(secrets.compare_digest(session["token"],FORM["token"])) :
			sub_def.error(f"トークンが一致しないです？","kanri")
			pass
	else :
		sub_def.error("トークンが送信されてないです？<br>繰り返し表示される場合は管理人へ連絡を。","kanri")


	token = secrets.token_hex(16)
	data = {"token":token , "m_name":FORM.get("m_name",session.get("m_name","")),"m_password":FORM.get("m_password",session.get("m_password",""))}

	session |= data
	sub_def.set_session(session)

	return session

def top_level_functions(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def parse_ast(filename):
    with open(filename, "rt",encoding='utf-8') as file:
        return ast.parse(file.read(), filename=filename)

#============================================================#

if __name__ == "__main__" :

	#フォームを辞書化
	form = cgi.FieldStorage()
	FORM = { key:form.getvalue(key) for key in form.keys() }

	if ("mode" not in FORM) :
		sub_def.set_session(FORM := {"token":secrets.token_hex(16)})
		OPEN_K()
	elif (os.environ["REQUEST_METHOD"] != "POST"):
		sub_def.error("不正ですか？by管理モード","top")

	#このファイル内の関数一覧と取得
	tree = parse_ast("kanri.py")
	func_list = [func.name for func in top_level_functions(tree.body)]

	#FORM["mode"]内に実行関数名が入ってる
	#一覧にあれば実行
	if (FORM["mode"] in func_list) :
		FORM |= token_check()
		admin_check()
		eval(FORM["mode"]+"()")
	else :
		sub_def.error(f"""[{FORM["mode"]}]が実行できませんでした。""","top")

	sub_def.header()
	print("あっれれ～？おっかしぃぞぉ～by管理モード")
