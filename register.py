#!D:\Python\Python312\python.exe

import sys
import cgi
import os
import datetime
import random
import secrets

import sub_def
import conf

Conf = conf.Conf
sys.stdout.reconfigure(encoding='utf-8')
#自動でutf-8にエンコードされて出力される

def newgame() :
	html = f"""
		<div class="new_title">新規ユーザー登録</div>
		<div class="new_txt">ユーザー名・パスワードを設定してください<br>(20文字以内。ユーザー名はひらがな等もOK<br>パスワードは英数字のみ。)</div>
		<form method="post" class="new_form">
			<div>
				ユーザー名:<input type="text" size="14" name="name" value=""><br>
				パスワード:<input type="password" size="14" name="password" value=""><br>
				<input type="submit" mode="sinki" value="　登　　録　">
				<input type="hidden" name="mode" value="sinki">
				<input type="hidden" name="token" value="{FORM["token"]}">
			</div>
		</form>
	"""

	sub_def.header()
	print(html)
	sub_def.footer()

def make_user_data(in_name="",in_pass="",crypted="") :

	try:
		os.makedirs(f"""{Conf["datadir"]}/{in_name}""")
	except OSError as ex:
		sub_def.error("データ作成に失敗しました。<br>ユーザー名を変更してみてください。","top")

	os.makedirs(f"""{Conf["datadir"]}/{in_name}/pickle""", exist_ok=True)

	crypted = crypted or sub_def.pass_encode(in_pass)

	time = datetime.datetime.now()
	bye_day = time + datetime.timedelta(days=Conf["goodbye"])
	bye_day = bye_day.strftime("%Y-%m-%d")

	host = sub_def.get_host()

	monset = ["スライム","ドラゴンキッズ","ベロゴン","ピッキー","マッドプラント","キリキリバッタ","ピクシー","ゴースト","トーテムキラー"]
	m_name = random.choice(monset)

	u_list = sub_def.open_user_list()
	u_list[in_name] = {
		"pass" : crypted,
		"host" : host,
		"bye" : bye_day,
		"key" :1,
		"m1_name" : m_name,
		"m1_hai" :0,
		"m1_lv" :5,
		"m2_name" : "",
		"m2_hai" : "",
		"m2_lv" : "",
		"m3_name" : "",
		"m3_hai" : "",
		"m3_lv" : "",
		"money" :50,
		"mes" :"未登録",
		"getm" : 0
	}
	sub_def.save_user_list(u_list)

	#ユーザーデータ
	user = {
		"name" :in_name,
		"pass" :crypted,
		"key" :1,
		"money" :100,
		"medal" :0,
		"isekai_limit" :0,
		"isekai_key" :1,
		"mes" :"未登録",
		"getm" :"0／0匹(0％)",
	}
	sub_def.save_user(user,in_name)

	#パーティーデータ
	party = [{
		"no" :1,
		"name" :m_name,
		"lv" : 1,
		"mlv" :10,
		"hai" :0,
		"hp" : 5,
		"mhp" : 5,
		"mp" : 5,
		"mmp" : 5,
		"atk" : 5,
		"def" : 5,
		"agi" : 5,
		"exp" : 0,
		"n_exp" : 10,
		"sei" : "ふつう",
		"sex" : random.choice(Conf["sex"])
	}]
	sub_def.save_party(party,in_name)

	#鍵
	Key_dat = sub_def.open_key_dat()
	key_set = { name :{"no":v["no"],"get":0} for name,v in Key_dat.items()}
	sub_def.save_room_key(key_set,in_name)

	#技
	Tokugi_dat = sub_def.open_tokugi_dat()
	waza = { name :{"no":v["no"], "type":v["type"] , "get":0} for name,v in Tokugi_dat.items()}
	waza["通常攻撃"]["get"] = 1
	sub_def.save_waza(waza,in_name)

	#図鑑
	M_list = sub_def.open_monster_dat()
	zukan = { name :{"no":v["no"], "m_type":v["m_type"] , "get":0} for name,v in M_list.items()}
	sub_def.save_zukan(zukan,in_name)

	#vips
	vips = {"パーク":0}
	sub_def.save_vips(vips,in_name)

	#パーク
	p_party = []
	sub_def.save_park(p_party,in_name)


	#bbsに新規告知
	logfile = "./" + Conf["datadir"] + "/bbslog.log"
	# 追加するログデータの作成
	newlog = f"""<hr><font color="red">{in_name}</font>さんが参加しました！。 <font size="1">--{time}</font>\n"""

	if not (os.path.exists(logfile)):
		with open(logfile, mode='w', encoding="utf-8_sig") as f:
			f.write("")
	with open(logfile, encoding="utf-8_sig") as f:
		log = f.readlines()

	# 先頭に新規ログデータを追加
	log.insert(0,newlog)

	# 保存行数を超える分末尾を削除
	while (len(log) > 50) :
		del log[-1]

	# 更新されたデータでログファイルに上書き
	with open(logfile, mode='w', encoding="utf-8_sig") as f:
		log = "".join(log)
		f.write(log)


def sinki(kanri_name="",kanri_pass="" , kanri=0) :
	#引数は管理画面からの強制登録用

	in_name = kanri_name or FORM.get("name")
	in_pass = kanri_pass or FORM.get("password")

	if not(in_name) :
		sub_def.error("名前がありません","top")
	if not(in_pass) :
		sub_def.error("パスワードがありません","top")
	if (in_name == in_pass) :
		sub_def.error("名前とパスワードは違うものにして下さい","top")

	if (2 <= len(in_name) >= 20) :
		sub_def.error("ユーザー名は2文字以上20文字以下で入力して下さい。","top")
	if (2 <= len(in_pass) >= 20) :
		sub_def.error("パスワードは2文字以上20文字以下で入力して下さい。","top")

	val = ['　' , ' ' , '\\' , '/' , ';' , ':'  , ',' , '*' , '?' , '\'' , '<' , '>' , '|' , '"' , '~' , '$' , '&' , '`' , '^' ]
	for i in val :
		if (i in in_name) :
			sub_def.error(f"使用できない文字 {i} が含まれています","top")

	if (os.path.exists(Conf["datadir"]+ "/" + in_name)) :
		sub_def.error("その名前は既に登録されています","top")

	u_list = sub_def.open_user_list()

	for u_name in u_list :
		if(u_name.casefold() == in_name.casefold()) :
			sub_def.error("その名前では登録することができません。","top")

	sub_def.set_cookie({"in_name":in_name, "in_pass":in_pass, "last_floor":1,"last_room":""})

	if (Conf["iplog"] == 1 and kanri == 0) : #管理モードの強制登録では重複判定スルー
		host = sub_def.get_host()
		for u in u_list.values() :
			if (host == u["host"]) :
				sub_def.error("重複登録の可能性があります。現在の設定では参加出来ません。","top")

	make_user_data(in_name,in_pass)
	sub_def.backup()

	party = sub_def.open_party(in_name)

	k_txt = "以下の内容で登録が完了しました。"
	if (kanri) :
		k_txt = "管理モードで強制登録しました。"

	html = f"""
		<div class="new_ok">{k_txt}</div>
		<div class="new_result">
			<div class="new_1"><div>ユーザー名</div><span>{in_name}</span></div>
			<div class="new_1"><div>パスワード</div><span>{in_pass}</span></div>
			<div class="new_1"><div>所 持 金</div>50</div>
			<div class="new_1"><div>鍵入手</div>地下1階</div>
		</div>
		<div class="new_mons">
			<img src="{Conf["imgpath"]}/{party[0]["name"]}.gif">
			<div>
				<div>名前：{party[0]["name"]}</div>
				<div>性別：-{party[0]["sex"]}-</div>
				<div>性格：{party[0]["sei"]}</div>
			</div>
		</div>
		<div class="new_result">
			<div class="new_1"><div>配 合 数</div>0回</div>
			<div class="new_1"><div>LEVEL</div>1 / 10</div>
			<div class="new_1"><div>H P</div>5 /5</div>
			<div class="new_1"><div>M P</div>5 /5</div>
			<div class="new_1"><div>攻 撃 力</div>5</div>
			<div class="new_1"><div>守 備 力</div>5</div>
			<div class="new_1"><div>経 験 値</div>0 /10</div>
		</div>

		<form action="{Conf["top_url"]}" method="post">
			<button> T O Pへ</button>
		</form>
	"""

	sub_def.header()
	print(html)

#====================================================================================#
def token_check():
	session = sub_def.get_session()

	if(FORM.get("token")) :
		if not(secrets.compare_digest(session["token"],FORM["token"])) :
			sub_def.error(f"{session['token']}|<br>{FORM['token']}トークンが一致しないです？","top")
	else :
		sub_def.error("トークンが送信されてないです？<br>繰り返し表示される場合は管理人へ連絡を。","top")

	token = secrets.token_hex(16)

	session |= {"token":token}
	sub_def.set_session(session)

	return session

#====================================================================================#

if __name__ == "__main__":
	if (os.path.exists("mente.mente")) :
		sub_def.error("現在メンテナンスモードに入ってます。<br>終了までお待ちくださいませ。","top")

	#フォームを辞書化
	form = cgi.FieldStorage()
	FORM = { key:form.getvalue(key) for key in form.keys() }

	u_list = sub_def.open_user_list()
	if (len(u_list) >= Conf["sankaMAX"]) :
		sub_def.error("参加人数上限を超えています。申し訳ありません。","top")

	cookie = sub_def.get_cookie()
	if(cookie.get("bye")) :
		sub_def.error("放棄後30日間は登録出来ません。","top")

	if ("mode" not in FORM) :
		sub_def.set_session(FORM := {"token":secrets.token_hex(16)})
		newgame()
	elif  (FORM["mode"] == "sinki") :
		FORM |= token_check()
		sinki()
		sub_def.footer()

	sys.exit()
