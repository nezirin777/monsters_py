def m_get (FORM) :
	import datetime

	import sub_def
	import conf

	Conf = conf.Conf

	token = FORM["token"]

	party = sub_def.open_party()
	battle = sub_def.open_battle()

	get_name = battle["teki"][0]["name"]
	Asex = battle["teki"][0]["sex"]

	#エポック秒に変換してからでないと比較できない
	if (float(FORM["c"]["next_t"]) + 30 < datetime.datetime.now().timestamp()) :
		sub_def.error("タイムオーバーのため さみしく帰っていった")

	new_mob = sub_def.monster_select(get_name)
	new_mob["sex"] = Asex

	if (len(party) < 10) :
		party.append(new_mob)
		for i,pt in enumerate(party,1) :
			pt["no"] = i

		sub_def.save_party(party)
		sub_def.result(f"<span>{get_name}</span>が仲間に加わりました","",FORM["token"])
	else :
		txt = ""
		for i,pt in enumerate(party,1) :
			txt += f"""<option value={i}>0{i}: {pt["name"]} {pt["sex"]} LV-{pt["lv"]} 配合{pt["hai"]}回</option>"""

		html = f"""
			<div class="mget_text">モンスターが一杯です。<br>誰を仲間から外しますか？</div>
			<form name=form1 method="post">
				<select name="Mno" onClick="change_img()">
					<option value=0 SELECTED>新しいモンスター : {get_name} {Asex}</option>
					{txt}
				</select>
				<button>仲間から外す</button>
				<input type="hidden" name="mode" value="m_bye">
				<input type="hidden" name="token" value="{token}">
				<br>
				<IMG NAME="img1" SRC="{Conf["imgpath"]}/{get_name}.gif">
			</form>
		"""

		sub_def.header()
		sub_def.jscript(party,get_name,"")
		print(html)
		sub_def.footer()

1
