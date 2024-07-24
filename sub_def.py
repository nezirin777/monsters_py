#!D:\Python\Python312\python.exe

import sys
import os

import datetime
import urllib.parse
from http import cookies
import socket #host取得
import shutil #ファイル操作
import hashlib #暗号化
import base64  #暗号化
import cryptocode #暗号化
import pandas as pd
import random
import pickle
import secrets

import conf
import exLock

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
lock = exLock.exLock("./lock_fol")
Conf = conf.Conf

#===========#
# 暗号化	#
#===========#
def pass_encode(p) :
	return base64.b64encode(hashlib.sha1(str(p).encode('utf-8')).digest()).decode()

#===========#
# ヘッダー	#
#===========#
def header():
	print("Content-Type: text/html; charset=utf-8\r\n\r\n")
	html = f"""
		<HTML>
		<HEAD>
			<TITLE> MONSTER'S 改 </TITLE>
			<LINK REL="stylesheet" HREF="./css_js/style.min.css" TYPE="text/css">
			<script src="./css_js/jquery.min.js"></script>
			<script src="./css_js/main.js"></script>

			</HEAD>
		<BODY>
	"""
	print(html)

#============#
#	フッター  #
#============#
def footer () :
	html = f"""
		<div id="footer">
			<div id="f_box">
				<div id="f_t">MONSTER'S 改 {Conf["ver"]}</div>
				<div><span>【改造】</span>おくた</div>
				<div><span>【ドット絵】</span>
					<A href="http://wpdot.blog106.fc2.com/">wp～ドット絵倉庫～</A></div>
				<div><span>【ドット絵】</span>
					<A href="https://www.pixiv.net/users/26734">chopper氏</A></div>
				<div><span>【ドット絵】</span>
					<A href="http://deepmoon.sakura.ne.jp/icon/"></A>DMF別館 アイコン素材屋</div>
				<div><span>【ドット絵】</span>
					<A href="https://dfp2013.jimdofree.com/">Dragon Fake Project</A></div>
				<div><span>【作成・配布】</span>
					<A href="http://park16.wakwak.com/~mikio-palace/">MIKIO-PALACE</A></div>
				<div>Copyright (C) 2002-2004：MIKIO</div>
			</div>
		</div>

		</BODY>
		</HTML>
	"""
	print(html)
	sys.exit()

#===========#
# Javascript#
#===========#
def jscript(party,m_name,count):
	main = ""
	#モンスターGET時用などに0番が必要
	if (party) :
		p = "/" + "/".join([pt["name"] for pt in party])
		main = f"""main("{Conf["imgpath"]}/","{p}","{m_name}")\n"""		#プルダウン選択モンスター画像切り替え用

	if (count):
		count = f"""<script src="./css_js/CountDown.js"></script>"""		#戦闘クールダウンカウントダウン用

	html = f"""
		<SCRIPT language="JavaScript">
			{main}
		</SCRIPT>
		{count}
	"""
	print(html)

#============#
#ログインボタン#
#============#
def my_page_button (token="") :
	html = f"""
		<form action="{Conf["cgi_url"]}" method="post">
			<input type="hidden" name="mode" value="my_page">
			<input type="hidden" name="token" value="{token}">
			<button>マイページへ</button>
		</form>
		<form action="{Conf["top_url"]}" method="post">
			<button>TOPへ</button>
		</form>
	"""
	print(html)
	footer()

#==========#
# リザルト #
#==========#
def result(txt="",html="",token="") :

	h = f"""
		<div id ="result">
			<span>{txt}</span>
		</div>
		{html}
	"""

	header()
	print(h)
	my_page_button(token)

#========#
# エラー #
#========#
def error(txt,jump="") :
	#	post("{Conf["cgi_url"]}", {{"mode":"my_page","token":"{token}"}})

	token = secrets.token_hex(16)
	session = {}
	if(jump !="top") :
		session = get_session()
	set_session(session|{"token":token,"error":1})

	url = f"""{Conf["cgi_url"]}"""
	par = f""" {{"mode":"my_page","token":"{token}"}} """

	if (jump == "top") :
		url = f"""{Conf["top_url"]}"""
		par = f""" {{}} """
	elif(jump == "kanri") :
		url = f"""{Conf["kanri_url"]}"""
		par = f""" {{"mode":"KANRI","token":"{token}"}} """

	html = f"""
		<SCRIPT language="JavaScript">
			window.addEventListener('DOMContentLoaded', function(){{
				setTimeout(() => {{post("{url}", {par}); }}, 1000);
			}});
		</SCRIPT>
		<div id ="error">
			<span>{txt}<br>自動移動します</span>
		</div>
	"""

	if (session.get("error") or jump == 99) :
		html = f"""
			<div id ="error">
				<span>{txt}</span>
			</div>
		"""

	header()
	print(html)
	footer()

#=============#
# クッキーSET #
#=============#
def set_cookie(c_data):
	cookie = cookies.SimpleCookie()

	cook = ",".join([str(k)+":"+str(v) for k,v in c_data.items()])
	cook = cryptocode.encrypt(cook,Conf["secret_key"])
	cookie["MONSTERS2"] = urllib.parse.quote_plus(cook)
	cookie["MONSTERS2"]["path"] = "/"

	#UTCじゃないとブラウザ保存時にローカル時間にさらにタイムゾーンが追加される
	expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=60)
	cookie["MONSTERS2"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
	cookie["MONSTERS2"]["SameSite"] = "Strict"

	print(cookie)

def set_cookie_bye():
	cookie = cookies.SimpleCookie()

	cook = "BYE:8181"
	cook = cryptocode.encrypt(cook,Conf["secret_key"])
	cookie["MONSTERS2"] = urllib.parse.quote_plus(cook)
	cookie["MONSTERS2"]["path"] = "/"

	#UTCじゃないとブラウザ保存時にローカル時間にさらにタイムゾーンが追加される
	expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
	cookie["MONSTERS2"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
	cookie["MONSTERS2"]["SameSite"] = "Strict"
	print(cookie)

def set_session(data=""):
	cookie = cookies.SimpleCookie()

	cook = ",".join([str(k)+":"+str(v) for k,v in data.items()])
	cook = cryptocode.encrypt(cook,Conf["secret_key"])
	cookie["session"] = urllib.parse.quote_plus(cook)
	cookie["session"]["path"] = "/"
	cookie["session"]["SameSite"] = "Strict"

	#UTCじゃないとブラウザ保存時にローカル時間にさらにタイムゾーンが追加される
	expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
	cookie["session"]["expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
	print(cookie)

#=============#
# クッキーGET #
#=============#
def get_cookie():
	cookie = {}
	if "HTTP_COOKIE" in os.environ :
		cook = cookies.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
		if (cook.get("MONSTERS2")) :
			pairs = urllib.parse.unquote_plus(cook["MONSTERS2"].value)
			pairs = cryptocode.decrypt(pairs,Conf["secret_key"]).split(",")
			for pair in pairs :
				vale = pair.split(":")
				if(vale[1].isdecimal()) :
					cookie[vale[0]] = int(vale[1])
				else :
					cookie[vale[0]] = vale[1]
	return cookie

def get_session():
	session = {}
	if "HTTP_COOKIE" in os.environ :
		cook = cookies.SimpleCookie(os.environ.get('HTTP_COOKIE',''))

		if not(cook.get("session")) :
			error("セッションが切れてるみたいです。","top")

		pairs = urllib.parse.unquote_plus(cook["session"].value)
		pairs = cryptocode.decrypt(pairs,Conf["secret_key"]).split(",")
		for pair in pairs :
			vale = pair.split(":")
			session[vale[0]] = vale[1]
	else :
		error("えらーです？？？","top")

	return session

#===================#
#ファイルopen_pickle #
#===================#
def pickle_load(file,user=""):
	s = get_session()

	name = user or s.get("name") or ""
	if not(name) :
		error(f"pickleファイル読み込みエラー{file}/ユーザー名：{name}が存在してないようです？",99)
	file = Conf["datadir"] + "/"+ name +"/pickle/" + file + ".pickle"

	with open(file, mode='rb') as f:
		return pickle.load(f)

def pickle_dump(l,file,user=""):
	lock.lock()
	s = get_session()
	name = user or s.get("name") or ""
	if not(name) :
		error(f"pickleファイル読み込みエラー{file}/ユーザー名：{name}が存在してないようです？",99)
	file = Conf["datadir"] + "/"+ name +"/pickle/" + file + ".pickle"

	with open(file, mode='wb') as f:
		pickle.dump(l,f)
	lock.unlock()

#===============#
#ファイルopen_csv#
#===============#
#return pd.read_csv(file, encoding="utf-8_sig",index_col="name").convert_dtypes().fillna("").sort_values("no").to_dict(orient='index')
def open_csv(file,name="",flg=0,flg2=0,col_names="") :
	if (name):
		file_p = Conf["datadir"] + "/"+ name +"/" + file
	else :
		file_p = file

	if(flg2) :
		try :
			return pd.read_csv(file_p, encoding="utf-8_sig",index_col="name").convert_dtypes().sort_values("no").to_dict(orient='index')
		except :
			return pd.read_csv(file_p, encoding="utf-8_sig",index_col="name",names=col_names).convert_dtypes().sort_values("no").to_dict(orient='index')
	else:
		reader = pd.read_csv(file_p, encoding="utf-8_sig").dropna(how='all').convert_dtypes()

		if (reader.dropna(how='all').empty) :
			reader = reader.astype("string").fillna("")
		else :
			for i in reader :
				if (reader[i].dtype == "string") :
					reader[i].fillna("", inplace=True)
				elif (reader[i].isnull().any()) :
					reader[i] = reader[i].astype("Int64")
				if (reader[i].dtype == "Float64") :
					reader[i] = reader[i].astype("Int64")

		hed = [i for i in reader]
		li = [list(reader[i]) for i in hed]
		dic = [ { h: li[i][s] for i,h in enumerate(hed) } for s in range(len(reader))]

		if (flg) :
			dic = dic[0]

		return dic

def save_csv(l,file,name="",label="name") :
	lock.lock()
	if (name):
		file = Conf["datadir"] + "/"+ name +"/" + file

	if not(len(l)) :
		error("対象のデータは空っぽのようです。<br>出力できませんでした。",99)
		pass

	flg = 0
	if (type(l) == dict) :
		for _, value in l.items():
			if isinstance(value, dict):
				df = pd.DataFrame().from_dict(l,orient='index')
				flg = 1
				break
			else :
				df = pd.DataFrame().from_dict([l])
	elif (type(l) == list) :
		df = pd.DataFrame().from_dict(l).convert_dtypes()
	else :
		df = l

	if(flg) :
		df.to_csv(file ,index="True",index_label=label, encoding="utf-8_sig")
	else :
		df.to_csv(file ,index=False, encoding="utf-8_sig")

	lock.unlock()

#=================================================================================================#
#ファイルopen_user_list                                                                            #
#=================================================================================================#
# name,pass,host,bye,key,m1_name,m1_hai,m1_lv,m2_name,m2_hai,m2_lv,m3_name,m3_hai,m3_lv,money,mes #
#=================================================================================================#
#管理モードからも読んでる為別関数にしておく。
def make_user_list():
	lock.lock()
	u_list = {}
	with open(Conf["datadir"] + "/user_list.pickle", mode='wb') as f:
		pickle.dump(u_list,f)
	lock.unlock()

def open_user_list() :
	lock.lock()
	file = Conf["datadir"]+"/user_list.pickle"
	if not (os.path.exists(file)) :
		make_user_list()
	with open(file, mode='rb') as f:
		l = pickle.load(f)

	#l.sort(key=lambda x: x['key'],reverse=True)
	if (l) :
		dic = sorted(l.items(), key=lambda x:x[1]["key"], reverse=True)
		l.clear()
		l.update(dic)
		for i,(k,v) in enumerate(l.items(),1) :
			l[k]["rank"] = i

	lock.unlock()
	return l

def save_user_list(l):
	import tempfile
	import shutil

	with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
		# pickle.dumpが途中で止まると壊れるのは防げないので、tempileに書き込む
		pickle.dump(l, f)
		# (1) f.flush -> os.fsyncを使い、データが確実にファイルに書き込まれた状態にする
		f.flush()
		os.fsync(f.fileno())
		temp_file_path = f.name

	lock.lock()
	shutil.move(temp_file_path , Conf["datadir"]+"/user_list.pickle")
	#os.replace(temp_file_path, Conf["datadir"]+"/user_list.pickle")
	#with open(Conf["datadir"]+"/user_list.pickle", mode='wb') as f:
	#	pickle.dump(l,f)
	lock.unlock()

#========================================================================#
#おみあい所登録データ                                                      #
#========================================================================#
# user,pass,name,lv,mlv,hai,hp,mhp,mp,mmp,atk,def,agi,ex,nex,sei,sex,mes #
#========================================================================#
#管理モードからも読んでる為別関数にしておく。
def make_omiai_list():
	omiai_list = {}
	lock.lock()
	with open(Conf["datadir"] + "/omiai_list.pickle", mode='wb') as f:
		pickle.dump(omiai_list,f)
	lock.unlock()

def open_omiai_list ():
	file = Conf["datadir"]+"/omiai_list.pickle"
	if not (os.path.exists(file)):
		make_omiai_list()
	with open(file, mode='rb') as f:
		return  pickle.load(f)

def save_omiai_list(l):
	lock.lock()
	with open(Conf["datadir"]+"/omiai_list.pickle", mode='wb') as f:
		pickle.dump(l,f)
	lock.unlock()

#=========================#
# メダル杯開催時間ファイル  #
#=========================#
def timesyori():
	time = datetime.date.today()
	d = time.day

	if (1 <= d < 11):
		x = 11
	elif (11 <= d < 21):
		x = 21
	elif (21 <= d):
		time += datetime.timedelta(days=20) #次の月に
		x = 1

	time = time.replace(day=x)
	with open(Conf["datadir"]+"/tournament_time.txt", mode='w',encoding='utf-8') as f:
		f.write(time.strftime("%Y年%m月%d日"))

	return time.strftime("%Y年%m月%d日")

def open_tournament_time() :
	if not (os.path.exists(Conf["datadir"]+"/tournament_time.txt")):
		t = timesyori()
	else :
		with open(Conf["datadir"]+"/tournament_time.txt",encoding='utf-8') as f:
			t = f.read()
			try:
				datetime.datetime.strptime(t,"%Y年%m月%d日")
			except ValueError as error:
				t = timesyori()

	return t

#================#
# データファイル  #
#================#
def open_dat(file):
	#return pd.read_csv(file, encoding="utf-8_sig").convert_dtypes().sort_values("no").to_dict(orient='records')
	with open(file+".pickle", mode='rb') as f:
		l = pickle.load(f)

	dic = sorted(l.items(), key=lambda x:x[1]["no"])
	l.clear()
	l.update(dic)

	return l

#==============================================================================#
# モンスターデータ                                                               #
# no,name,hp,mp,atk,def,agi,exp,money,waza,type,m_type,room,階層A,階層B,get  #
# 血統1,相手1,血統2,相手2,血統3,相手3,お見合いA1,お見合いB1,お見合いA2,お見合いB2    #
#================================================================================#
def open_monster_dat():
	return open_dat("./dat/pickle/monster_dat")

def open_monster_boss_dat() :
	return open_dat("./dat/pickle/monster_boss_dat")

#========================================#
# 鍵データ                                 #
# no,type,name1,name2 name1=鍵,name2=部屋 #
#=========================================#
def open_key_dat():
	return open_dat("./dat/pickle/key_dat")

#=======================#
# 特技データ             #
# no,name,mp,damage,type#
#=======================#
def open_tokugi_dat():
	return open_dat("./dat/pickle/tokugi_dat")

#==============================#
# 性格データ                    #
# no,name,勇気,優しさ,知性,行動 #
#==============================#
def open_seikaku_dat():
	return open_dat("./dat/pickle/seikaku_dat")

#=========================#
# 本データ                 #
# no,name,勇気,優しさ,知性  #
#=========================#
def open_book_dat():
	return open_dat("./dat/pickle/book_dat")

#=========================#
# メダル交換所             #
# no,name,price,type      #
#=========================#
def open_medal_shop_dat():
	return open_dat("./dat/pickle/medal_shop_dat")

#=========================#
# vips交換所               #
# no,name,price,type      #
#=========================#
def open_vips_shop_dat():
	return open_dat("./dat/pickle/vips_shop_dat")

def open_vips_shop2_dat():
	return open_dat("./dat/pickle/vips_shop2_dat")

#=====================================#
# ユーザーデータ                      #
# name,pass,key,medal,money,mes,getm #
#=====================================#
def open_user(user=""):
	return pickle_load("user",user)

def save_user(csv,user=""):
	pickle_dump(csv,"user",user)

#===============================================================#
# パーティー                                                     #
# no,name,lv,mlv,hai,hp,mhp,mp,mmp,atk,def,agi,exp,n_exp,sei,sex#
#===============================================================#
def open_party(user=""):
	return pickle_load("party",user)

def save_party(csv,user=""):
	pickle_dump(csv,"party",user)

#==========================================================#
# モンスターパーク                                           #
# name,lv,mlv,hai,hp,mhp,mp,mmp,atk,def,agi,ex,nex,sei,sex #
#==========================================================#
def open_park(user=""):
	return pickle_load("park",user)

def save_park(csv,user=""):
	pickle_dump(csv,"park",user)

#=============================#
# vipsデータ                   #
#=============================#
def open_vips(user=""):
	return pickle_load("vips",user)

def save_vips(csv,user=""):
	pickle_dump(csv,"vips",user)

#==================#
# 習得特技          #
# no,name,type,get #
#==================#
def open_waza(user=""):
	return pickle_load("waza",user)

def save_waza(csv,user=""):
	pickle_dump(csv,"waza",user)

#=========================#
# 所持鍵                   #
# no,type,name1,name2,get #
#=========================#
def open_room_key(user=""):
	return pickle_load("room_key",user)

def save_room_key(csv,user=""):
	pickle_dump(csv,"room_key",user)

#=========================#
# 図鑑                    #
# no,name,m_type,get #
#=========================#
def open_zukan(user=""):
	return pickle_load("zukan",user)

def save_zukan(csv,user=""):
	pickle_dump(csv,"zukan",user)

#======================================================#
# 戦闘一時データ                                        #
# no,name,name2,hp,mhp,mp,mmp,atk,def,agi,exp,money,sex#
#======================================================#
def open_battle(user=""):
	return pickle_load("battle",user)

def save_battle(csv,user=""):
	pickle_dump(csv,"battle",user)

#==========#
# host取得 #
#==========#
def get_host():
	try:
		return socket.gethostbyaddr(os.environ['REMOTE_ADDR'])[0]
	except socket.herror:
		return os.environ['REMOTE_ADDR']

	#return socket.gethostbyaddr(os.environ['REMOTE_ADDR'])[0]

#==============#
# バックアップ #
#==============#
def backup():
	if (Conf["backup"] == 1) :
		time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
		shutil.copytree(Conf["datadir"] , Conf["backfolder"] + f"/{time}/")

#=============#
# 削除時間取得 #
#=============#
def getdelday(bye) :
	return (datetime.datetime.strptime(str(bye), '%Y-%m-%d') - datetime.datetime.now() ).days

#================#
#	保存期間調査  #
#================#
def delete_user(target) :
	#お見合い登録データから対象ユーザー削除
	omiai_list = open_omiai_list()

	if (omiai_list) :
		for name , opt in omiai_list.items() :
			if (name == target) :
				del omiai_list[name]
				break

		#対象ユーザーにお見合い申請している場合の対処
		for name , opt in omiai_list.items() :
			if (opt["request"] == target) :
				opt[name]["request"] = ""
				opt[name]["cancel"] = f"{target}さんへの依頼はお断りされてしまったようです・・・"

		save_omiai_list(omiai_list)

	shutil.rmtree(f"{Conf['datadir']}/{target}")

def delete_check() :
	u_list = open_user_list()
	if(u_list) :
		for key,u in list(u_list.items())[:] :
			#削除日時計算
			delday = getdelday(u["bye"])
			if (int(delday) <= 0) :
				delete_user(key)
				del u_list[key]
		save_user_list(u_list)

#==========#
# 特技取得  #
#==========#
def waza_get(target ,user_name="") :
	waza = open_waza(user_name)
	waza[target]["get"] = 1
	save_waza(waza,user_name)

#==========#
# 図鑑登録  #
#==========#
def zukan_get(target,user_name="") :
	user = open_user(user_name)
	zukan = open_zukan(user_name)

	zukan[target]["get"] = 1
	save_zukan(zukan,user_name)

	get = [1 for val in zukan.values() if(val["get"])]
	get = len(get)

	mleng = len(zukan)
	s = get / mleng * 100
	#user["getm"] = f"{get}／{mleng}匹 ({'{:.2f}'.format(s)}％)"
	user["getm"] = f"{get}／{mleng}匹 ({s:.2f}％)"

	save_user(user,user_name)


#==================#
# モンスターセレクト#
#==================#
#配合、交換所等GET 基礎ステ + 補正(配合回数/2)
def monster_select(target,hosei=0,get=0,user_name="") :
	Mons = open_monster_dat()
	Seikaku_dat = open_seikaku_dat()

	mon = Mons[target]
	new_mob = {
		"name" : target ,
		"lv" : 2 ,
		"mlv" : 10 ,
		"hp" : int(mon["hp"] + hosei) ,
		"mhp" : int(mon["hp"] + hosei) ,
		"mp" : int(mon["mp"] + hosei) ,
		"mmp" : int(mon["mp"] + hosei) ,
		"atk" : int(mon["atk"] + hosei) ,
		"def" : int(mon["def"] + hosei) ,
		"agi" : int(mon["agi"] + hosei) ,
		"hai" : 0 ,
		"exp" : 0 ,
		"n_exp" :int(Conf["nextup"]) ,
		"sex" : random.choice(Conf["sex"]) ,
		"sei" :  random.choice(list(Seikaku_dat.keys()))
	}

	if (get) :
		waza_get(mon.pop("waza"),user_name)
		zukan_get(new_mob["name"],user_name)

	return new_mob

def battle_mob_select(target,hosei,in_floor) :
	Mons = open_monster_dat()
	Seikaku_dat = open_seikaku_dat()

	mon = Mons[target]
	new_mob = {
		"name" : target ,
		"name2" : target ,
		"hp" : int(mon["hp"] * hosei) ,
		"mhp" : int(mon["hp"] * hosei) ,
		"mp" : int(mon["mp"] * hosei) ,
		"mmp" : int(mon["mp"] * hosei) ,
		"atk" : int(mon["atk"] * hosei) ,
		"def" : int(mon["def"] * hosei) ,
		"agi" : int(mon["agi"] * hosei) ,
		"exp" : int(mon["exp"] * in_floor) ,
		"money" : int(mon["money"] * in_floor) ,
		"sex" : random.choice(Conf["sex"]) ,
		"sei" :  random.choice(list(Seikaku_dat.keys()))
	}

	return new_mob

def battle_boss_select(target,hosei,in_floor) :
	Mons = open_monster_boss_dat()
	Seikaku_dat = open_seikaku_dat()

	mon = Mons[target]
	new_mob = {
		"name" : target ,
		"name2" : target ,
		"hp" : int(mon["hp"] * hosei) ,
		"mhp" : int(mon["hp"] * hosei) ,
		"mp" : int(mon["mp"] * hosei) ,
		"mmp" : int(mon["mp"] * hosei) ,
		"atk" : int(mon["atk"] * hosei) ,
		"def" : int(mon["def"] * hosei) ,
		"agi" : int(mon["agi"] * hosei) ,
		"exp" : int(mon["exp"] * in_floor) ,
		"money" : int(mon["money"] * in_floor) ,
		"sex" : random.choice(Conf["sex"]) ,
		"sei" :  random.choice(list(Seikaku_dat.keys()))
	}

	return new_mob

#=============#
# 数値表記変換#
#=============#
def slim_number(item) :
	import copy

	new_item = ""

	cookie = get_cookie()
	unit_type = cookie.get("unit_type",0)

	if(unit_type == 0) :
		return item

	def num_slice(v,sw) :
		num = 0
		arr = ["","","","",]

		if(sw == 1) :
			return f"{v:,}"
		elif(sw == 2) :
			arr = ["","k","M","G","T","P"]
			num = 1000
		elif (sw == 3) :
			arr = ["","万","億","兆","京",""]
			num = 10000

		v = int(v)
		if (v >= 1000000 and num !=0) :
			while(v >= num) :
				v = v / num
				arr.pop(0)
			if(v.is_integer()) :
				return f"{int(v):,}" + arr[0]
			return f"{v:,.2f}" + arr[0]
		return f"{v:,}"

	if isinstance(item, dict) :
		new_item = item.copy()
		for n,v in new_item.items() :
			if (str(v).isdecimal()) :
				new_item[n] = num_slice(v,unit_type)

	elif isinstance(item, list) :
		new_item = copy.deepcopy(item)
		for i , items in enumerate(item) :
			for n,v in items.items() :
				if (str(v).isdecimal()) :
					new_item[i][n] = num_slice(v,unit_type)

	elif (str(item).isdecimal()) :
		new_item = num_slice(item,unit_type)

	return new_item
