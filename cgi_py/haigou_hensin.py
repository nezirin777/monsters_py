def haigou_hensin (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	new_m	= FORM["s"]["new_mons"]

	if(new_m == "フィッシュル(制服)") :
		new_m = "フィッシュル"

	#配列位置に合わせ-1されたものを引き継いでいるのでそのままで大丈夫
	haigou1 = int(FORM["s"]["haigou1"])
	haigou2 = int(FORM["s"]["haigou2"])

	user = sub_def.open_user()
	party = sub_def.open_party()

	hai_A = party[haigou1]
	hai_B = party[haigou2]

	user["money"] -= ((hai_A["lv"] + hai_B["lv"]) * 10)
	sub_def.save_user(user)

	mlv = int(hai_A["lv"] + hai_B["lv"])
	new_hai = hai_A["hai"] + hai_B["hai"] +1
	hosei = max(int(new_hai /2) ,1)

	#番号が後ろの方から消さないとずれる
	del party[max(haigou1,haigou2)]
	del party[min(haigou1,haigou2)]

	new_mob = sub_def.monster_select(new_m,hosei,1)

	new_mob["name"]	= FORM["s"]["new_mons"]
	new_mob["hai"]	= new_hai
	new_mob["lv"]	= 1
	new_mob["mlv"]	= mlv
	party.append(new_mob)

	for i,pt in enumerate(party,1) :
		pt["no"] = i

	sub_def.save_party(party)

	waza = sub_def.open_waza()
	txt = ""
	for key,wa in waza.items() :
		name = key if(wa["get"]) else "-"
		txt += f"""<div class="hen_text3">{name}</div>"""

	html = f"""
		<div class="hai_title">NEW MONSTER!</div>

		<div class="hen_box0">
			<div class="hen_box1">
				<div class="hen_text1">モンスター名</div>
				<div><img src="{Conf["imgpath"]}/{new_mob["name"]}.gif"></div>
				<div class="hen_text2">{new_mob["name"]}<br>{new_mob["sex"]}<br>{new_mob["sei"]}</div>
			</div>
		</div>

		<div class="hen_box2">
			<div class="hen_box3">
				<div class="hen_text1">Level</div>
				<div class="hen_text2">1 / {new_mob["mlv"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">配合数</div>
				<div class="hen_text2">{new_mob["hai"]}回</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">H P</div>
				<div class="hen_text2">{new_mob["hp"]} / {new_mob["mhp"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">M P</div>
				<div class="hen_text2">{new_mob["mp"]} / {new_mob["mmp"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">攻撃力</div>
				<div class="hen_text2">{new_mob["atk"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">守備力</div>
				<div class="hen_text2">{new_mob["def"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">素早さ</div>
				<div class="hen_text2">{new_mob["agi"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">経験値</div>
				<div class="hen_text2">0 / {Conf["nextup"]}</div>
			</div>
		</div>

		<div class="hent_box1">
			<div class="hen_text1">習得特技</div>
			<div class="hent_box2">{txt}</div>
		</div>
	"""

	sub_def.header()
	print(html)
	sub_def.my_page_button(FORM["token"])
