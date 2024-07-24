def battle_isekai_encount (FORM) :
	import random
	import sub_def
	import conf

	Conf = conf.Conf

	in_isekai = int(FORM["in_isekai"])
	max_floor = int(FORM["max_floor"])

	hosei = (in_isekai + max_floor) * (max_floor / 1000)

	#出現可能性のモンスターチェック
	#階層一致→タイプ一致
	M_list = sub_def.open_monster_dat()

	hit_monster = {name:mon for name,mon in M_list.items() if(mon["room"] == "特殊")}
	aite = [name for name,mon in hit_monster.items() if(mon["階層A"] <= in_isekai <= mon["階層B"])]

	#きゅうべぇ判定,魔法少女出現部屋で戦闘PTに特殊モンスターがいれば出現
	if(21<= in_isekai <=30) :
		party = sub_def.open_party()
		s = min(len(party) ,3)

		for i in range(s) :
			name = party[i]["name"]
			if(M_list[name]["room"] == "特殊"):
				aite.append("キュゥべえ")

	if (len(aite) < 1) :
		sub_def.error("対戦相手モンスターを選択できませんでした。")

	# name=最後に倒した敵(get用)、exp,money=倒した敵加算,down=全滅フラグ倒れた分加算
	teki = [{"name":"","exp":0,"money":0,"down":1}]

	if (len(aite) == 1) :
		aite = random.sample(aite, 1)
	elif(len(aite) == 2) :
		aite = random.sample(aite, 2)
	else :
		aite = random.sample(aite, 3)

	for name in aite :
		new_mob = sub_def.battle_mob_select(name,hosei,max_floor)
		teki.append(new_mob)

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
		<div class="battle_start">異界の者たちが現れた。</div>
		<div class="battle_teki_box">{html}</div>
	"""

	return txt
