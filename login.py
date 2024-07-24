#!D:\Python\Python312\python.exe

import sys
import cgi
import os
import ast
import secrets



import sub_def
import conf
import cgi_py

Conf = conf.Conf

sys.stdout.reconfigure(encoding='utf-8')
#自動でutf-8にエンコードされて出力される
#=============#
# my_page画面 #
#=============#
def my_page() :
	cgi_py.my_page.my_page(FORM)

def my_page2() :
	cgi_py.my_page2.my_page2(FORM)

def change() :
	cgi_py.change.change(FORM)
#================#
#	コメント更新  #
#================#
def comment() :
	cgi_py.comment.comment(FORM)
#==============#
#	魔物図鑑    #
#==============#
def zukan() :
	cgi_py.zukan.zukan(FORM)

#============#
#	本屋さん  #
#============#
def books() :
	cgi_py.books.books(FORM)

def book_read() :
	cgi_py.books.book_read(FORM)
#==========#
# 宿屋開始 #
#==========#
def yadoya() :
	cgi_py.yadoya.yadoya(FORM)

def yadoya_ok() :
	cgi_py.yadoya.yadoya_ok(FORM)
#==========#
# 教会     #
#==========#
def kyoukai() :
	cgi_py.kyoukai.kyoukai(FORM)

def kyoukai_ok() :
	cgi_py.kyoukai.kyoukai_ok(FORM)
#==============#
# メダル交換所 #
#==============#
def medal_shop() :
	cgi_py.medal_shop.medal_shop(FORM)

def medal_shop_ok() :
	cgi_py.medal_shop.medal_shop_ok(FORM)
#===============#
# ユーザー名変更 #
#===============#
def name_change() :
	cgi_py.name_change.name_change(FORM)

def name_change_check() :
	cgi_py.name_change.name_change_check(FORM)

def name_change_ok() :
	cgi_py.name_change.name_change_ok(FORM)
#==========#
# 性転換所  #
#==========#
def seitenkan() :
	cgi_py.seitenkan.seitenkan(FORM)

def seitenkan_ok() :
	cgi_py.seitenkan.seitenkan_ok(FORM)
#====================#
# モンスターパーク	#
#====================#
def park() :
	cgi_py.park.park(FORM)

def park_1() :
	cgi_py.park.park_1(FORM)

def park_2() :
	cgi_py.park.park_2(FORM)

#====================#
#	VIPS関連処理  #
#====================#
def v_shop() :
	cgi_py.v_shop.v_shop(FORM)

def v_shop_ok() :
	cgi_py.v_shop.v_shop_ok(FORM)

def v_shop2() :
	cgi_py.v_shop2.v_shop2(FORM)

def v_shop2_ok() :
	cgi_py.v_shop2.v_shop2_ok(FORM)

#========#
#	配合  #
#========#
def haigou_check() :
	cgi_py.haigou_check.haigou_check(FORM)

def haigou_hensin() :
	cgi_py.haigou_hensin.haigou_hensin(FORM)

#========#
#  戦闘  #
#========#
def battle_type() :
	cgi_py.battle_type.battle_type(FORM)

def battle_type2() :
	cgi_py.battle_type.battle_type2(FORM)

def battle_fight() :
	cgi_py.battle_fight.battle_fight(FORM)

#==================#
#  モンスタゲット   #
#==================#
def m_get() :
	cgi_py.m_get.m_get(FORM)

def m_bye() :
	cgi_py.m_bye.m_bye(FORM)

#============#
#  部屋鍵get  #
#============#
def roomkey_get() :
	cgi_py.roomkey_get.roomkey_get(FORM)

#=================#
#	メダル獲得杯   #
#=================#
def tournament_result() :
	cgi_py.tournament_result.tournament_result()

#================#
#	お見合い関係  #
#================#
def omiai_room():
	cgi_py.omiai_room.omiai_room(FORM)

def omiai_touroku():
	cgi_py.omiai_touroku.omiai_touroku(FORM)
def omiai_touroku_cancel():
	cgi_py.omiai_touroku.omiai_touroku_cancel(FORM)

def omiai_request():
	cgi_py.omiai_request.omiai_request(FORM)
def omiai_request_ok():
	cgi_py.omiai_request.omiai_request_ok(FORM)
def omiai_request_cancel():
	cgi_py.omiai_request.omiai_request_cancel(FORM)

def omiai_answer_no():
	cgi_py.omiai_answer.omiai_answer_no(FORM)
def omiai_answer_ok():
	cgi_py.omiai_answer.omiai_answer_ok(FORM)
def omiai_answer_result():
	cgi_py.omiai_answer.omiai_answer_result(FORM)

def omiai_baby_get():
	cgi_py.omiai_baby.omiai_baby_get(FORM)


#================#
#	数値表記法    #
#================#
def number_unit():
	cgi_py.number_unit.number_unit(FORM)

#====================================================================================#

def top_level_functions(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def parse_ast(filename):
    with open(filename, "rt",encoding='utf-8') as file:
        return ast.parse(file.read(), filename=filename)

def token_check():
	FORM["s"] = sub_def.get_session()

	if not(FORM.get("token")) :
		sub_def.error("トークンが送信されてないです？<br>繰り返し表示される場合は管理人へ連絡を。","top")
		#pass

	if not(secrets.compare_digest(FORM["s"]["token"],FORM["token"])) :
		sub_def.error(f"{FORM['s']['token']}|<br>{FORM['token']}トークンが一致しないです？","top")
	#	pass

	token = secrets.token_hex(16)
	if(FORM.get("ref") == "top") :
		data = {"token":token , "name":FORM.get("name",""),"password":FORM.get("password","")}
	else :
		data = {"token":token ,"name":FORM.get("name",FORM["s"]["name"]),"password":FORM.get("password",FORM["s"]["password"])}

	sub_def.set_session(data)

	return data

def reg_check():
	if (FORM["name"] == "") :
		sub_def.error("名前がありません","top")

	if (FORM["password"] == "") :
		sub_def.error("パスワードがありません","top")

	if not (os.path.exists(Conf["datadir"] + "/" + FORM["name"])) :
		sub_def.error("あなたは未登録のようです。","top")

	user = sub_def.open_user(FORM["name"])
	if not(user["pass"] == sub_def.pass_encode(FORM["password"])) :
		sub_def.error("パスワードが違います","top")

	cookie = sub_def.get_cookie()
	cookie |= {"in_name":FORM["name"],"in_pass":FORM["password"]}

	sub_def.set_cookie(cookie)

	return cookie

#====================================================================================#

if __name__ == "__main__" :
	if (os.path.exists("mente.mente")) :
		sub_def.error("現在メンテナンスモードに入ってます。<br>終了までお待ちくださいませ。","top")

	#フォームを辞書化
	form = cgi.FieldStorage()
	FORM = { key:form.getvalue(key) for key in form.keys() }

	#このファイル内の関数一覧取得
	tree = parse_ast("login.py")
	func_list = [func.name for func in top_level_functions(tree.body)]

	#GETメゾットを利用した直アクセスはダメ！
	#他ユーザーのログイン画面と図鑑画面だけはOK
	if (os.environ["REQUEST_METHOD"] != "POST"):
		if (FORM.get("mode") in ("tournament_result","my_page2","zukan")) :
			eval(FORM["mode"]+"()")
			sys.exit()
		else :
			sub_def.error("不正だっちゃ1","top")

	#トークンチェック
	FORM |= token_check()
	FORM["c"] = reg_check()

	#FORM["mode"]内に実行関数名が入ってる
	#一覧にあれば実行
	if (FORM.get("mode") in func_list) :
		eval(FORM["mode"]+"()")
	else :
		sub_def.error(f"""[{FORM["mode"]}]が実行できませんでした。""","top")

	sub_def.header()
	print("あっれれ～？おっかしぃぞ～？")
	sub_def.footer()
