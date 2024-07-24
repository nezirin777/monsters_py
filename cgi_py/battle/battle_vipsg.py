
def battle_vipsg_encount (FORM) :
	import random
	import sub_def
	import conf

	Conf = conf.Conf

	in_floor = int(FORM["in_floor"])
	#in_room = FORM["in_room"]
	user = sub_def.open_user()

	hosei = in_floor

	#kaisou = int(str(in_floor)[-3:])
	if (in_floor > 1000) :
		hosei *= (user["key"] / 1000) * (1+(user["key"]/20000))

	#出現可能性のモンスターチェック
	#階層一致→タイプ一致
	M_list = sub_def.open_monster_boss_dat()
	hit_monster = [name for name,mon in M_list.items() if(mon["type"] == "VIPSガールズ")]

	if (len(hit_monster) < 1) :
		sub_def.error("対戦相手モンスターを選択できませんでした。")

	hit_monster = random.sample(hit_monster, 3)

	# name=最後に倒した敵(get用)、exp,money=倒した敵加算,down=全滅フラグ倒れた分加算
	teki = [{"name":"","exp":0,"money":0,"down":1}]
	teki += [sub_def.battle_boss_select(name,hosei,in_floor) for name in hit_monster]

	party = sub_def.open_party()
	pt_num = min(len(party) ,3)

	battle = {
		"party" : party[:pt_num] ,
		"teki": teki
	}

	sub_def.save_battle(battle)
	teki_v = sub_def.slim_number(battle["teki"])

	html = "".join([f"""
		<div class="battle_teki_box1">
			<div class="battle_teki_name"><img src="{Conf["imgpath"]}/{mon["name"]}.gif"><br>
				<span>{mon["name2"]}<br>-{mon["sex"]}-</span>
			</div>
			<div class="battle_teki_hp"><span>HP/MHP</span><br>{mon["hp"]}<br>/{mon["mhp"]}</div>
		</div>
	""" for mon in teki_v[1:] ])

	txt = f"""
		<div class="battle_start">VIPSガールズが現れた。</div>
		<div class="battle_teki_box">{html}</div>
	"""

	return txt
