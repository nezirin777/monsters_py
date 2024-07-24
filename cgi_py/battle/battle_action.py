
#========#
# 戦闘用 #
#========#
def pr(actor,target ,txt) :
	import sub_def
	import conf
	Conf = conf.Conf

	c = sub_def.get_cookie()
	turn = c["turn"]

	actor2 = sub_def.slim_number(actor)
	target2 = sub_def.slim_number(target)

	html = f"""
		<div class="battle_log_a">
			<div><img src="{Conf["imgpath"]}/{actor2["name"]}.gif"></div>
			<div class="sky_blue">{actor2["name"]}</div>
			<div>HP / MHP<br>{actor2["hp"]} / {actor2["mhp"]}</div>
			<div>MP / MMP<br>{actor2["mp"]} / {actor2["mmp"]}</div>
		</div>
	"""
	if (target) :
		html += f"""
			<div class="battle_R">{turn}<span>R</span></div>
			<div class="battle_log_b">
				<div><img src="{Conf["imgpath"]}/{target2["name"]}.gif"></div>
				<div class="red">{target2["name"]}</div>
				<div>HP / MHP<br>{target2["hp"]} / {target2["mhp"]}</div>
				<div>MP / MMP<br>{target2["mp"]} / {target2["mmp"]}</div>
			</div>
	"""

	html += f"""<div class="battle_log">{txt}</div>"""
	html2 = f"""<div class="battle_log_box">{html}</div>"""
	print(html2)

def kaifuku(target ,kairyou) :
	if (target["hp"] == 0) :
		m_log = "は既に力尽きていた"
	else :
		target["hp"] += int(target["mhp"] * kairyou)
		target["hp"] = min(target["hp"],target["mhp"])
		log2 = kairyou * 100

		m_log = f"""のHPが約{log2}%回復した"""

	return f"""<span class="sky_blue">{target["name"]}</span>{m_log}"""

def sosei(target,kairyou,luk) :
	if (target["hp"] != 0) :
		m_log = "は生きています"
	else :
		if (luk == 0) :
			m_log = "は生きかえらなかった"
		else :
			m_log = "は生きかえった"
			target["hp"] = int(target["mhp"] * kairyou)
			target["休み"] = 1

	return f"""<span class="sky_blue">{target["name"]}</span>{m_log}"""

#############################################################################
def teki_action (actor,battle,special,in_floor) :
	import random
	import sub_def

	lan = []
	if (battle["party"][0]["hp"] > 0) :
		lan = [0]
	elif(battle["party"][1:2]) :
		if (battle["party"][1]["hp"] > 0) :
			lan = [1]
		elif(battle["party"][2:3]) :
			if (battle["party"][2]["hp"] > 0) :
				lan = [2]

	if(in_floor > 500 or special == "異世界") :
		lan = []
		if (battle["party"][0]["hp"] > 0) :
			lan += [0,0,0,0,0,0]
		if(battle["party"][1:2]) :
			if (battle["party"][1]["hp"] > 0) :
				lan += [1,1,1]
		if(battle["party"][2:3]) :
			if (battle["party"][2]["hp"] > 0) :
				lan += [2]

	if(len(lan) == 0) :
		return battle

	target = battle["party"][random.choice(lan)]
	if (special in ("わたぼう","スライム")) :
		target = battle["party"][0]

	#防御状態ならdef2倍
	defe = target["def"]
	if (target["bt"]["hit"] == "防御") :
		defe *= 2

	atk_hosei = random.choice([1.0, 1.1, 1.2, 1.3])
	def_hosei = random.choice([0.9, 1.0, 1.1, 1.2])

	dmg = int((actor["atk"] * atk_hosei) - (defe * def_hosei))
	dmg = max(0,dmg)

	target["hp"] = max(0,target["hp"] - dmg)
	dmg2 = sub_def.slim_number(dmg)

	if (dmg == 0) :
		txt = f"""<span class="sky_blue">{target["name"]}</span>は<span class="red">{actor["name"]}</span>の攻撃をかわした！"""
	else :
		txt = f"""<span class="red">{actor["name"]}</span>は<span class="sky_blue">{target["name"]}</span>に<span class="red">{dmg2}</span>ポイントのダメージを与えた！"""

	pr(target,actor,txt)

	return battle

#################################################################################################
def mikata_action (actor,battle) :
	import random
	import sub_def

	def mikata_atk(txt) :
		if (actor["mp"] < zyumon["mp"]) :
			txt += f"""<span class="red">{zyumon["name"]}</span>を唱えようとした、<br>しかしMPが足りなかった！"""
		else :
			actor["mp"] -= int(zyumon["mp"])

			if (target["hp"] == 0) :
				txt += f"""<span class="red">{target["name"]}</span>に攻撃しようとしたが既に力尽きていた！<br>"""
			else :
				dmg = int((actor["atk"] * atk_hosei * zyumon["damage"]) - (target["def"] * def_hosei))
				dmg = max(0,dmg)
				target["hp"] -= min(target["hp"],dmg)
				dmg2 = sub_def.slim_number(dmg)


				if (kaisin == 2) :
					txt += "会心の一撃！<br>"

				if (dmg == 0) :
					txt += f"""しかし<span class="red">{target["name"]}</span>にダメージを与えることができなかった！"""
				else :
					txt += f"""<span class="yellow">{zyumon["name"]}</span>を繰り出し<br><span class="red">{target["name"]}</span>に<span class="red">{dmg2}</span>ポイントのダメージを与えた！"""
					if (target["hp"] == 0) :
						txt += f"""<br><span class="red">{target["name"]}</span>は倒れた"""
						battle["teki"][0]["name"] = target["name"] #起き上がり対象に
						battle["teki"][0]["sex"] = target["sex"]
						battle["teki"][0]["exp"] += target["exp"]
						battle["teki"][0]["money"] += target["money"]
						battle["teki"][0]["down"] += 1
		return txt

	def mikata_kaifuku(txt) :
		if (actor["mp"] < zyumon["mp"]) :
			txt += f"""<span class="red">{zyumon["name"]}</span>を唱えようとした、<br>しかしMPが足りなかった！"""
		else :
			actor["mp"] -= int(zyumon["mp"])
			if (zyumon["type"] == 2) :
				#(対象味方,回復量)
				m_log = kaifuku(battle["party"][bt["nakama"]],zyumon["damage"])
			else :
				luk = random.randint(0,1) if(zyumon["name"] == "ザオラル") else 1

				#(対象味方,回復量,ザオラル判定)
				m_log = sosei(battle["party"][bt["nakama"]],zyumon["damage"],luk)

			txt += f"""<span class="red">{zyumon["name"]}</span>を唱えた<br>{m_log}"""
		return txt

	bt = actor["bt"]

	Tokugi_dat = sub_def.open_tokugi_dat()
	Seikaku_dat = sub_def.open_seikaku_dat()

	target = battle["teki"][bt["target"]]
	txt = f"""<span class="sky_blue">{actor["name"]}</span>は"""

	atk_hosei = random.choice([1.0, 1.1, 1.2, 1.3])
	def_hosei = random.choice([0.9, 1.0, 1.1, 1.2])

	### 性格判定 ###
	# 2 = 会心 ( "ねっけつかん","いのちしらず","いっぴきおおかみ","れいせいちんちゃく","きれもの","こうかつ","ちょとつもうしん")
	# 0 = さぼり ( "きまぐれ","あわてもの","ひねくれもの","がんこもの","ゆうじゅうふだん","うっかりもの","のんきもの","おひとよし","おくびょうもの","なまけもの","わがまま","うぬぼれや")
	#1/4確率で会心もしくはさぼり=3/4で通常攻撃 kaisin=2→会心 kaisin=0→さぼり
	kaisin = 1
	if (random.randint(0,3) == 0) :
		s = Seikaku_dat[actor["sei"]]["行動"]
		if (s == 2) :
			kaisin = 2
			atk_hosei *= 2
		elif (s == 0) :
			txt += "命令を聞かずに踊っている～♪"
			pr(actor,"",txt)
			return battle

	zyumon = {}
	if (bt["hit"] == "攻撃") :
		zyumon = { **{"name" : bt["toku"]} , **Tokugi_dat[bt["toku"]] }
		txt = mikata_atk(txt)

	elif (bt["hit"] == "回復" and bt["ktoku"] != "0") :
		zyumon = { **{"name" : bt["ktoku"]} , **Tokugi_dat[bt["ktoku"]] }
		txt = mikata_kaifuku(txt)

	elif (bt["hit"] == "防御") :
		zyumon["mp"] = 0
		txt += "防御している"

	if not(zyumon) :
		txt += "使用する魔法が選択されなかった！<br>"

	target = target if 'target' in locals() else 0

	pr(actor,target,txt)
	return battle
#################################################################################################
