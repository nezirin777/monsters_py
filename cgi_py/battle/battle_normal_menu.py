def battle_normal_menu (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	token = FORM["token"]

	battle = sub_def.open_battle()
	Tokugi_dat = sub_def.open_tokugi_dat()
	waza = sub_def.open_waza()

	txt1 = "".join([f"""<option value={i}>{mon["name2"]}</option>""" for i,mon in enumerate(battle["teki"][1:],1) if mon["hp"] != 0])
	txt2 = "".join([f"""<option value={name}>{name} ({toku["mp"]} MP)</option>"""  for name,toku in Tokugi_dat.items() if(waza[name]["get"] and waza[name]["type"] == 1)])
	txt3 = "".join([f"""<option value={name}>{name} ({toku["mp"]} MP)</option>"""  for name,toku in Tokugi_dat.items() if(waza[name]["get"] and waza[name]["type"] != 1)])
	txt4 = "".join([f"""<option value={i}>{pt["name"]}</option>""" for i,pt in enumerate(battle["party"])])

	party_v = sub_def.slim_number(battle["party"])

	html = "".join([
		f"""
			<div class="battle_pt_box1">
				<div class="battle_pt_name"><img src="{Conf["imgpath"]}/{pt["name"]}.gif"><br><span>{pt["name"]}</span></div>
				<div class="battle_pt_box2">
					<div class="battle_pt_1">レベル</div>
					<div class="battle_pt_2"><span>{pt["lv"]}</span></div>
					<div class="battle_pt_1">HP</div>
					<div class="battle_pt_2">{pt["hp"]}/{pt["mhp"]}</div>
					<div class="battle_pt_1">MP</div>
					<div class="battle_pt_2">{pt["mp"]}/{pt["mmp"]}</div>
					<div class="battle_pt_3">行動選択</div>
					<select name="hit{pt["no"]}" class="battle_pt_4">
						<option value="攻撃">攻撃</option>
						<option value="防御">防御する</option>
						<option value="回復">回復魔法使用</option>
					</select>
					<div class="battle_pt_3">攻撃相手</div>
					<select name="target{pt["no"]}" class="battle_pt_4">
						{txt1}
					</select>
					<div class="battle_pt_3">特技</div>
					<select name="toku{pt["no"]}" class="battle_pt_4">
						{txt2}
					</select>
					<div class="battle_pt_3">回復魔法相手</div>
					<select name="nakama{pt["no"]}" class="battle_pt_4">
						{txt4}
					</select>
					<div class="battle_pt_3">回復魔法</div>
					<select name="ktoku{pt["no"]}" class="battle_pt_4">
						<option value=0>使用しない</option>
						{txt3}
					</select>
				</div>
			</div>
		"""  for i, pt in enumerate(party_v) if ((battle["party"][i]["hp"] > 0))
	])

	txt = f"""
		<div class="battle_start">行動を選択して下さい！</div>
		<form method="post">
			<div class="battle_pt_box">{html}</div>
			<br>
			<input type="submit" name="monok" value="決定">
			<input type="hidden" name="mode" value="battle_fight">
			<input type="hidden" name="token" value="{token}">
	"""

	return txt
