def m_bye (FORM) :
	import sub_def

	Mno = int(FORM["Mno"])

	party = sub_def.open_party()
	battle = sub_def.open_battle()

	get_name = battle["teki"][0]["name"]
	Asex = battle["teki"][0]["sex"]

	if (Mno == 0) :
		mes = f"""<span>{get_name}</span>はさみしそうにさっていった"""
	else :
		Mno -= 1	#配列位置に合わせるため-1
		by_name = party[Mno]["name"]
		del party[Mno]

		new_mob = sub_def.monster_select(get_name)
		new_mob["sex"] = Asex
		party.append(new_mob)

		for i,pt in enumerate(party,1) :
			pt["no"] = i

		mes = f"""<span>{get_name}</span>が加わり<span>{by_name}</span>はさっていった"""

	sub_def.save_party(party)

	sub_def.result(mes,"",FORM["token"])
