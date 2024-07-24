def omiai_touroku(FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM["name"]
	#配列の位置合わせのため-1
	no	= int(FORM["haigou1"]) -1
	mes = FORM.get("mes","")
	token = FORM["token"]

	party = sub_def.open_party()
	omiai_list = sub_def.open_omiai_list()

	if (len(party) == 1) :
		sub_def.error("パーティーに1体しかいない場合お見合いに参加することはできません")

	if (party[no]["lv"] < Conf["haigoulevel"]) :
		sub_def.error("お見合い可能Lvに達していないため登録できません。")

	omiai_list[in_name] = party[no] |{"mes":mes ,"cancel":"", "request" :"", "baby":""}

	txt = f"""{party[no]["name"]}を登録しました。"""

	del party[no]
	for i,pt in enumerate(party,1) :
		pt["no"] = i

	sub_def.save_party(party)
	sub_def.save_omiai_list(omiai_list)

	html = f"""
		<form method="post">
		<input type="hidden" name="mode" value="omiai_room">
		<input type="hidden" name="token" value="{token}">
		<button>お見合い所に戻る</button>
		</form>
	"""
	sub_def.result(txt,html,FORM["token"])

def omiai_touroku_cancel(FORM) :
	import sub_def

	in_name = FORM["name"]
	target	= FORM["target"]
	mes = FORM.get("mes","")
	token = FORM["token"]

	party = sub_def.open_party()
	omiai_list = sub_def.open_omiai_list()

	omiai = omiai_list[in_name]

	if (omiai["request"]) :
		sub_def.error("他のユーザーに申請を出している場合登録をキャンセルできません。")

	for v in omiai_list.values() :
		if (v["request"] == target) :
			sub_def.error("あなたへのお見合い申請がある場合登録をキャンセルできません。")

	if (len(party) >= 10) :
		sub_def.error("パーティがいっぱいで連れていくことができませんでした。")

	del omiai["mes"] , omiai["cancel"] , omiai["request"] ,omiai["baby"]

	party.append(omiai)

	mes = f"""<span>{omiai["name"]}</span>をパーティに加えました。"""

	for i,pt in enumerate(party,1) :
		pt["no"] = i
	del omiai_list[in_name]

	sub_def.save_party(party)
	sub_def.save_omiai_list(omiai_list)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value="{token}">
			<button>お見合い所に戻る</button>
		</form>
	"""
	sub_def.result(mes,html,FORM["token"])
