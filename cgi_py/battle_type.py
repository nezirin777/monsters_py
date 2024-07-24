def battle_type (FORM) :
	import time
	import random

	import cgi_py
	import sub_def
	import conf

	Conf = conf.Conf

	in_floor = int(FORM["in_floor"])
	in_room = FORM["in_room"]

	user = sub_def.open_user()
	party = sub_def.open_party()

	if not(0 < in_floor <= user["key"] ) :
		sub_def.error("階層指定がおかしいです")

	if (len(party) < 1) :
		sub_def.error("パーティがいません。最低1体は必要です。")
	if (party[0]["hp"] <= 0) :
		sub_def.error("先頭のモンスターのHPが0です。<br>回復するか他のモンスターにしてください。")

	val = [0]
	randam = 25

	if (Conf["event_boost"]) :
		randam = 20

	if (random.randint(1,randam) == 1) :
		val = ["わたぼう"]
		room_key = sub_def.open_room_key()
		for r_key in room_key.values() :
			if (r_key["get"] == 0) :
				val = ["わたぼう","スライム"]
				break
		if(in_floor >= 1001 + 500 * (user.get("isekai_limit",0) / 10)) :
			#↑500階おきに次のエリアに進めるようになる
			if(user.get("isekai_limit",0) < user.get("isekai_key",0)) :
				if (user.get("isekai_limit",0) != Conf["isekai_max_limit"]) :
					val = ["vipsg"]

	s = random.choice(val)

	next_t = time.time() + Conf["nextplay"] #エポック秒

	FORM["c"] |= {"last_floor":in_floor , "last_room":in_room,"special":s,"next_t":next_t,"turn":1}
	sub_def.set_cookie(FORM["c"])

	if (s == 0) :
		txt = cgi_py.battle_normal_encount.battle_normal_encount(FORM)
		txt += cgi_py.battle_normal_menu.battle_normal_menu(FORM)
	elif (s == "スライム" or s == "わたぼう") :
		txt = cgi_py.battle_special.battle_special_encount(FORM,s)
		txt += cgi_py.battle_special.battle_special_menu(FORM)
	elif(s == "vipsg") :
		txt = cgi_py.battle_vipsg.battle_vipsg_encount(FORM)
		txt += cgi_py.battle_normal_menu.battle_normal_menu(FORM)

	sub_def.header()
	print(txt)
	sub_def.footer()

def battle_type2 (FORM) :
	import time

	import cgi_py
	import sub_def
	import conf

	Conf = conf.Conf

	in_isekai = int(FORM["in_isekai"])

	user = sub_def.open_user()
	party = sub_def.open_party()

	if not(0 <= in_isekai <= user["isekai_key"]) :
		sub_def.error("異世界は1Fづつしか進めません。")

	if (in_isekai > user["isekai_limit"]) :
		sub_def.error("探索限界に達しています")

	if (len(party) < 1) :
		sub_def.error("パーティがいません。最低1体は必要です。")
	if (party[0]["hp"] <= 0) :
		sub_def.error("先頭のモンスターのHPが0です。<br>回復するか他のモンスターにしてください。")

	next_t = time.time() + Conf["nextplay"] #エポック秒

	FORM["c"] |= {"last_floor_isekai":in_isekai ,"special":"異世界","next_t":next_t,"turn":1}
	sub_def.set_cookie(FORM["c"])

	txt = cgi_py.battle_isekai_encount.battle_isekai_encount(FORM)
	txt += cgi_py.battle_normal_menu.battle_normal_menu(FORM)

	sub_def.header()
	print(txt)
	sub_def.footer()
