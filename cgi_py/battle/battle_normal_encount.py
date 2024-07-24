
def battle_normal_encount (FORM) :
	import random
	import sub_def
	import conf

	Conf = conf.Conf

	in_floor = int(FORM["in_floor"])
	in_room = FORM["in_room"]

	#出現モンスターは500階まで設定、501階以上はルーブ。例：2100階時→100階のモンスターが選ばれるように。
	#kaisou = int(str(in_floor)[-3:])
	kaisou = in_floor
	hosei = in_floor

	while (kaisou > 500) :
		kaisou -= 500

	if (in_floor > 500) :
		hosei *= (in_floor / 500)

	#出現可能性のモンスターチェック
	#階層一致→タイプ一致
	M_list = sub_def.open_monster_dat()
	hit_monster = {name:mon for name,mon in M_list.items() if(mon["階層A"] <= kaisou <= mon["階層B"])}

	if(in_room == "通常") :
		aite_tmp = [name for name,mon in hit_monster.items() if(mon["room"] not in ("特殊" ,"？？？系"))]
	else :
		aite_tmp = [name for name,mon in hit_monster.items() if(in_room == mon["room"])]

	if (len(aite_tmp) < 1) :
		sub_def.error("対戦相手モンスターを選択できませんでした。")

	teki_kazu = random.choices([1,2,3], k = 1, weights = [3,2,1])[0]
	aite = random.choices(aite_tmp, k=teki_kazu)

	# name=最後に倒した敵(get用)、exp,money=倒した敵加算,down=全滅フラグ倒れた分加算
	teki = [{"name":"","exp":0,"money":0,"down":1}]
	teki += [sub_def.battle_mob_select(name,hosei,in_floor) for name in aite]

	#敵重複時名前修正
	if (teki_kazu == 2) :
		if (teki[1]["name"] == teki[2]["name"]) :
			teki[1]["name2"] += "_A"
			teki[2]["name2"] += "_B"
	elif (teki_kazu == 3) :
		if (teki[1]["name"] == teki[2]["name"] == teki[3]["name"]) :
			teki[1]["name2"] += "_A"
			teki[2]["name2"] += "_B"
			teki[3]["name2"] += "_C"
		elif (teki[1]["name"] != teki[2]["name"] == teki[3]["name"]) :
			teki[2]["name2"] += "_A"
			teki[3]["name2"] += "_B"
		elif (teki[1]["name"] == teki[3]["name"]) :
			teki[1]["name2"] += "_A"
			teki[3]["name2"] += "_B"
		elif (teki[1]["name"] == teki[2]["name"]) :
			teki[1]["name2"] += "_A"
			teki[2]["name2"] += "_B"
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
		<div class="battle_start">モンスターが現れた。</div>
		<div class="battle_teki_box">{html}</div>
	"""


	return txt
