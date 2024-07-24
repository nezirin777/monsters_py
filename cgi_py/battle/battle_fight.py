def battle_fight (FORM) :
	import time

	import sub_def
	import conf
	import cgi_py

	Conf = conf.Conf

	in_floor  = int(FORM["c"].get("last_floor",0))
	if(in_floor == 0) :
		sub_def.error("階層選択がおかしいです？")

	special = FORM["c"]["special"]
	turn = int(FORM["c"]["turn"])

	next_t = time.time() + Conf["nextplay"] #エポック秒
	FORM["c"] |= {"next_t":next_t,"turn":turn+1}
	sub_def.set_cookie(FORM["c"])

	#user = sub_def.open_user()
	#party = sub_def.open_party()
	battle = sub_def.open_battle()

	pt_num = min(len(battle["party"]),3)
	if (special in ("わたぼう","スライム")) :
		pt_num = 1

	bt = [
		{"hit":FORM.get("hit1",0),"target":int(FORM.get("target1",0)),"toku":FORM.get("toku1",0),"nakama":int(FORM.get("nakama1",0)),"ktoku":FORM.get("ktoku1",0)},
		{"hit":FORM.get("hit2",0),"target":int(FORM.get("target2",0)),"toku":FORM.get("toku2",0),"nakama":int(FORM.get("nakama2",0)),"ktoku":FORM.get("ktoku2",0)},
		{"hit":FORM.get("hit3",0),"target":int(FORM.get("target3",0)),"toku":FORM.get("toku3",0),"nakama":int(FORM.get("nakama3",0)),"ktoku":FORM.get("ktoku3",0)},
	]

	#選択コマンドをパーティデータに入れる
	for pt,b in zip(battle["party"],bt) :
		pt["bt"] = b

	#行動順決定
	BT = battle["party"] + battle["teki"][1:]
	BT.sort(key=lambda x: x["agi"],reverse=True)

	sub_def.header()

	#行動開始/battle_action内
	for bt in BT :
		if(bt.get("no")) :
			bt["休み"] = 0

	for bt in BT :
		if(bt["hp"] > 0 and bt.get("休み",0) == 0)  :
			if(bt.get("no")) :
				battle = cgi_py.battle_action.mikata_action(bt,battle)
			else :
				battle = cgi_py.battle_action.teki_action(bt,battle,special,in_floor)

	for i,pt in enumerate(battle["party"]) :
		del battle["party"][i]["bt"]
		del battle["party"][i]["休み"]

	sub_def.save_battle(battle)

	#行動後戦闘継続処理--
	if (battle["teki"][0]["down"] == len(battle["teki"])) :
		cgi_py.battle_sub.battle_end("勝利した",1,special)
		if (special == 0) :
			cgi_py.battle_sub.key_get(in_floor)
			cgi_py.battle_sub.mon_get(FORM)
		elif (special == "スライム") : #スライム城
			cgi_py.battle_sub.battle_roomkey_get(FORM["token"])
		elif (special == "わたぼう") : #わたぼう城
			cgi_py.battle_sub.battle_medal_get(in_floor)
		elif (special == "vipsg") :
			cgi_py.battle_sub.battle_isekai_limit_get()
		elif (special == "異世界") :
			cgi_py.battle_sub.battle_isekai_key_get(int(FORM["c"].get("last_floor_isekai",0)))
			cgi_py.battle_sub.mon_get(FORM)
		sub_def.my_page_button(FORM["token"])

	elif (pt_num == len([1 for pt in battle["party"] if(pt["hp"] == 0)])) :
		cgi_py.battle_sub.battle_end("負けた",0,special)
		if(special == 0 or special == "異世界") :
			cgi_py.battle_sub.haisen()
		sub_def.my_page_button(FORM["token"])

	elif (turn >= Conf["maxround"]) :
		cgi_py.battle_sub.battle_end("引き分けた",0.5,special)
		sub_def.my_page_button(FORM["token"])


	if (special != "わたぼう" and special != "スライム") :
		txt = cgi_py.battle_normal_menu.battle_normal_menu(FORM)
		print(txt)
		sub_def.footer()
	else :
		txt = cgi_py.battle_special.battle_special_menu(FORM)
		print(txt)
		sub_def.footer()
