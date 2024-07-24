def change(FORM) :
	import sub_def

	c_no = [0] * 11
	c_no[0]	= int(FORM.get("c_no1",0))
	c_no[1]	= int(FORM.get("c_no2",0))
	c_no[2]	= int(FORM.get("c_no3",0))
	c_no[3]	= int(FORM.get("c_no4",0))
	c_no[4]	= int(FORM.get("c_no5",0))
	c_no[5]	= int(FORM.get("c_no6",0))
	c_no[6]	= int(FORM.get("c_no7",0))
	c_no[7]	= int(FORM.get("c_no8",0))
	c_no[8]	= int(FORM.get("c_no9",0))
	c_no[9] = int(FORM.get("c_no10",0))
	c_no[10] = int(0) #10体埋まってるときに0が必要

	party = sub_def.open_party()

	#0がある分-1
	if (len(party) != len(set(c_no))-1) :
		sub_def.error("並び替えの数値が重なってます")

	for pt,c in zip(party,c_no) :
		pt["no"] = c
	party.sort(key=lambda x: x["no"])

	if (party[0]["hp"] == 0) :
		sub_def.error("No.1は必ず生存中のモンスターを設定をしてください")

	sub_def.save_party(party)

	sub_def.result("並べ替えが完了しました","",FORM["token"])
