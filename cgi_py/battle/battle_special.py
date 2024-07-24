
def battle_special_encount (FORM,target) :
	import sub_def
	import conf

	Conf = conf.Conf

	in_floor = int(FORM["in_floor"])

	hosei = in_floor + 30
	if (in_floor > 1000) :
		hosei *= (in_floor / 1000) * 1.3

	# name=最後に倒した敵(get用)、exp,money=倒した敵加算,down,=全滅フラグ倒れた分加算
	teki = [{"name":"","exp":0,"money":0,"down":1}]
	new_mob = sub_def.battle_mob_select(target,hosei,in_floor)
	teki.append(new_mob)

	party = sub_def.open_party()

	battle = {
		"party" : party[:1],
		"teki": teki
	}

	sub_def.save_battle(battle)
	teki_v = sub_def.slim_number(battle["teki"])

	if (target == "スライム") :
		txt = f"""
			スライムの不思議な城に迷い込んだ!<br>
			勝利すれば不思議な鍵が貰えます!<br>
		"""
	elif (target == "わたぼう") :
		txt = f"""
			わたぼうのメダル城に迷い込んだ!<br>
			勝利すればメダルが貰えます!<br>
		"""

	html = f"""
		<div class="battle_teki_box1">
			<div class="battle_teki_name"><img src="{Conf["imgpath"]}/{teki_v[1]["name"]}.gif"><br>
				<span>{teki_v[1]["name2"]}<br>-{teki_v[1]["sex"]}-</span>
			</div>
			<div class="battle_teki_hp"><span>HP/MHP</span><br>{teki_v[1]["hp"]}<br>/{teki_v[1]["mhp"]}</div>
		</div>
	"""

	txt = f"""
		<div class="battle_start">{txt}</div>
		<div class="battle_teki_box">{html}</div>
	"""

	return txt

def battle_special_menu (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	token = FORM["token"]

	#party = sub_def.open_party()
	battle = sub_def.open_battle()
	#Tokugi_dat = sub_def.open_tokugi_dat()
	#waza = sub_def.open_waza()

	#pt_num = 1
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
						<option value="攻撃" SELECTED>攻撃</option>
					</select>
					<div class="battle_pt_3">攻撃相手</div>
					<select name="target{pt["no"]}" class="battle_pt_4">
						<option value=1>{battle["teki"][1]["name2"]}
					</select>
					<div class="battle_pt_3">特技</div>
					<select name="toku{pt["no"]}" class="battle_pt_4">
						<option value="通常攻撃" SELECTED>通常攻撃
					</select>
				</div>
			</div>
		"""  for i, pt in enumerate(party_v) if ((battle["party"][i]["hp"] > 0))
	])

	txt = f"""
		<div class="battle_start">何を行うか決定して下さい！</div>
		<form method="post">
			<div class="battle_pt_box">{html}</div>

			<br>
			<input type="submit" name="monok" value="決定">
			<input type="hidden" name="mode" value="battle_fight">
			<input type="hidden" name="token" value={token}>
	"""

	return txt
