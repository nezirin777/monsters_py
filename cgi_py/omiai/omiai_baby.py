def omiai_baby_get(FORM) :
	import sub_def

	in_name = FORM["name"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()
	user = sub_def.open_user()
	party = sub_def.open_party()

	if (len(party) >= 10) :
		sub_def.error("パーティがいっぱいで連れていくことができませんでした。")

	nedan = omiai_list[in_name]["hai"] * 5000
	if not(user["money"] >= nedan) :
		sub_def.error("受け取るためのお金が足りません")

	user["money"] -= nedan
	new_mob = omiai_list[in_name]
	party.append(new_mob)

	del omiai_list[in_name]
	del new_mob["mes"] ,new_mob["cancel"] ,new_mob["request"] ,new_mob["baby"]
	if(new_mob.get("pass") ) :
		del new_mob["pass"]

	for i,pt in enumerate(party,1) :
		pt["no"] = i

	sub_def.save_user(user)
	sub_def.save_party(party)
	sub_def.save_omiai_list(omiai_list)

	mes = f"""<span>{new_mob["name"]}</span>をパーティに加えました。"""
	html = f"""
		<form method="post">
		<input type="hidden" name="mode" value="omiai_room">
		<input type="hidden" name="token" value="{token}">
		<button>お見合い所に戻る</button>
		</form>
	"""

	sub_def.result(mes,html,FORM["token"])
