
#LVup処理---------------------------------------------------------------------------
def Lv_up(pt0) :
	import random

	pt0["lv"] += 1
	pt0["exp"] -= pt0["n_exp"]

	x = 1
	if (pt0["lv"] <= 100) :
		x = 1.15
	elif (pt0["lv"] <= 200) :
		x = 1.0075
	elif (pt0["lv"] <= 300) :
		x = 1.0045
	elif (pt0["lv"] <= 400) :
		x = 1.0003
	elif (pt0["lv"] <= 500) :
		x = 1.0025
	elif (pt0["lv"] <= 600) :
		x = 1.0020
	elif (pt0["lv"] <= 700) :
		x = 1.0017
	elif (pt0["lv"] <= 800) :
		x = 1.0014
	elif (pt0["lv"] <= 900) :
		x = 1.0012
	elif (pt0["lv"] <= 1000) :
		x = 1.0010
	else :
		pt0["n_exp"] = 999999

	pt0["n_exp"] = min(int(pt0["n_exp"] * x), pt0["lv"]*1000 ,999999)

	lan = random.choice([0.8 ,0.9 ,1.0 ,1.1, 1.2])
	hp = int(lan * pt0["mhp"] / pt0["lv"])

	lan = random.choice([0.7 ,0.8, 0.9, 1.0, 1.1])
	mp = int(lan * pt0["mmp"] / pt0["lv"])

	lan = random.choice([0.8 ,0.9 ,1.0 ,1.1 ,1.2])
	atk = int(lan * pt0["atk"] / pt0["lv"])

	lan = random.choice([0.7 ,0.8, 0.9, 1.0, 1.1])
	defn = int(lan * pt0["def"] / pt0["lv"])

	lan = random.choice([0.7 ,0.8, 0.9, 1.0, 1.1])
	agi = int(lan * pt0["agi"] / pt0["lv"])

	hosei = (pt0["hai"] * 0.1)

	pt0["mhp"] += int(hp + hosei)
	pt0["mmp"] += int(mp + hosei)
	pt0["atk"] += int(atk + hosei)
	pt0["def"] += int(defn + hosei)
	pt0["agi"] += int(agi + hosei)

	return pt0

def Lv_Max(pt0) :
	pt0["lv"]  = pt0["mlv"]
	pt0["mhp"] = pt0["hai"] + 15
	pt0["mmp"] = pt0["hai"] + 14
	pt0["atk"] = pt0["hai"] + 25
	pt0["def"] = pt0["hai"] + 24
	pt0["agi"] = pt0["hai"] + 24
	pt0["exp"]   = 0
	pt0["n_exp"] = 0
	pt0["hp"] = min(pt0["hp"] ,pt0["mhp"])
	pt0["mp"] = min(pt0["mp"] ,pt0["mmp"])
	return pt0
#LVup出力処理---------------------------------------------------------------------------
def pr_Lv_up(pt0,pt) :
	import sub_def

	up_hp = sub_def.slim_number(pt0["mhp"] - pt["mhp"])
	up_mp = sub_def.slim_number(pt0["mmp"] - pt["mmp"])
	up_atk = sub_def.slim_number(pt0["atk"] - pt["atk"])
	up_def = sub_def.slim_number(pt0["def"] - pt["def"])
	up_agi = sub_def.slim_number(pt0["agi"] - pt["agi"])

	html = f"""
		<div class="battle_log_Lvup">
			<span class="yellow">レベルアップ！</span><br>
			<span class="sky_blue">{pt["name"]}</span>は<span class="red">Lv{pt["lv"]}からLv{pt0["lv"]}</span>になった！<br>
			最大HPが<span class="sky_blue">{up_hp}</span>上昇した。<br>
			最大MPが<span class="sky_blue">{up_mp}</span>上昇した。<br>
			攻撃力が<span class="sky_blue">{up_atk}</span>上昇した。<br>
			守備力が<span class="sky_blue">{up_def}</span>上昇した。<br>
			素早さが<span class="sky_blue">{up_agi}</span>上昇した。<br>
		</div>
	"""
	print(html)

def pr_Lv_Max(pt0,pt) :
	html = f"""
		<div class="battle_log_Lvup">
			<span class="yellow">レベルアップ！</span><br>
			<span class="sky_blue">{pt["name"]}</span>はLv{pt["lv"]}からLv{pt0["lv"]}になった！<br>
			<span class="red">成長の限界に達した。</span><br>
			年老いた為、<span class="sky_blue">{pt["name"]}</span>の力は激減した。
		</div>
	"""

	print(html)

#LVupチェック---------------------------------------------------------------------------
def Lv_up_check(pt0,pt) :
	while(pt0["exp"] >= pt0["n_exp"]) :
		pt0 = Lv_up(pt0)
		#成長限界判定
		if (pt0["lv"] >= pt0["mlv"]) :
			pt0 = Lv_Max(pt0)
			pr_Lv_Max(pt0,pt)
			break
	else :
		if (pt0["lv"] > pt["lv"]) :
			pr_Lv_up(pt0,pt)
	return pt0

#鍵獲得処理---------------------------------------------------------------------------
def key_get(in_floor) :
	import random
	import sub_def
	import conf
	Conf = conf.Conf

	user = sub_def.open_user()
	if (in_floor == user["key"]) :
		key_sets = {0:0,1:"普通の鍵+1", 3:"幸せの鍵+3" ,10:"幸運の鍵+10" ,30:"天運の鍵+30" ,50:"希望の鍵+50" ,100:"奇跡の鍵+100"}
		w = [10 ,50 ,15 ,12 ,7 ,4 ,2]
		if (Conf["event_boost"]) :
			w = [1 ,51 ,17 ,14 ,8 ,5 ,4]

		get,txt = random.choices(list(key_sets.items()),weights=w)[0]

		if (get != 0) :
			user["key"] += get
			html = f"""<div class="battle_keyget"><span class="yellow">{txt}</span>を拾った！ラッキー♪</div>"""

			sub_def.save_user(user)
			print(html)

#部屋鍵獲得処理---------------------------------------------------------------------------
def battle_roomkey_get(token) :
	import sub_def
	#import conf

	#Conf = conf.Conf

	room_key = sub_def.open_room_key()

	txt = ""

	for name,r_key in room_key.items() :
		if (r_key["get"] == 0) :
			txt += f"""<option value={name}>{name}の部屋の鍵"""

	html = f"""
		<div class="battle_roomkey_get">
			どのKEYを取得しますか？
		</div>
		<form method="post">
			<select name=get_key>
				{txt}
			</select>
			<button>取得する</button>
			<input type="hidden" name="mode" value="roomkey_get">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	print(html)

#異世界鍵獲得処理---------------------------------------------------------------------------
def battle_isekai_limit_get() :
	import sub_def

	user = sub_def.open_user()
	txt = ""
	if (user.get("isekai_limit",0)) :
		user["isekai_limit"] += 10
		txt = "異世界をより深く探索できるようになった!"
	else :
		user["isekai_limit"] = 10
		txt = "異世界への扉の鍵をGetした!"
	sub_def.save_user(user)

	html = f"""
		<div class="battle_keyget"><span class="yellow">{txt}</span></div>
	"""
	print(html)

def battle_isekai_key_get(in_isekai) :
	import sub_def

	user = sub_def.open_user()

	html = ""
	if(in_isekai == user["isekai_key"]) :
		if(user["isekai_limit"] == user["isekai_key"]) :
			html = f"""
				<div class="battle_keyget"><span class="yellow">探索限界に到達した。</span></div>
			"""
		else :
			html = f"""
				<div class="battle_keyget"><span class="yellow">次の階層の鍵を手に入れた。</span></div>
			"""

		user["isekai_key"] += 1
		sub_def.save_user(user)

	print(html)


#メダル獲得処理---------------------------------------------------------------------------
def battle_medal_get(in_floor) :
	import sub_def
	import conf
	Conf = conf.Conf

	if (in_floor <= 500) :
		get = 3
	elif (501 <= in_floor <= 1000) :
		get = 5
	elif (1001 <= in_floor <= 10000) :
		get = 7
	else :
		get = 10

	if (Conf["event_boost"]) :
		if (in_floor <= 500) :
			get = 5
		elif (501 <= in_floor <= 1000) :
			get = 7
		elif (1001 <= in_floor <= 10000) :
			get = 10
		else :
			get = 15

	user = sub_def.open_user()
	user["medal"] += get
	sub_def.save_user(user)

	html = f"""
		<div class=\"battle_keyget\"><span class="yellow">メダルを{get}枚ゲットした！ラッキー♪</span></div>
	"""
	print(html)

#勝利時モンスター獲得処理---------------------------------------------------------------------------
def mon_get(FORM) :
	import random
	import sub_def
	import conf

	Conf = conf.Conf

	in_floor = int(FORM["c"]["last_floor"])
	token = FORM["token"]

	if (in_floor <= 150) :
		get = random.randint(1,3)
	elif (151 <= in_floor <= 200) :
		get = random.randint(1,4)
	else :
		get = random.randint(1,5)

	if (get == 1) :
		M_list = sub_def.open_monster_dat()
		battle = sub_def.open_battle()
		get_name = battle["teki"][0]["name"]

		if(M_list[get_name]["room"] == "特殊") :
			get = random.randint(1,30)

		if (M_list[get_name]["get"] == 1 and get == 1) :
			html = f"""
				<div class="battle_monget">
					<img src="{Conf["imgpath"]}/{get_name}.gif"><br>
					<span class="red">{get_name}</span>が仲間になりたがっています。<br>
					仲間にしますか？
				</div>
				<form method="post">
					<button>仲間にする</button>
					<input type="hidden" name="mode" value="m_get">
					<input type="hidden" name="token" value="{token}">
				</form>
			"""
			print(html)

#敗戦処理---------------------------------------------------------------------------
def haisen() :
	import sub_def
	import random

	user = sub_def.open_user()

	if (10 >= user["key"]) :
		return

	w = [100]
	key_sets = {1:"不幸の鍵-1"}

	# w = 重み％
	if (11 <= user["key"] <= 100) :
		key_sets  = {1:"不幸の鍵-1" , 3:"不運な鍵-3" , 5:"呪いの鍵-5" , 10:"危険な鍵-10"}
		w = [50 ,30, 19 ,1]
	elif (101 <= user["key"] <=1000) :
		key_sets  = {1:"不幸の鍵-1" , 3:"不運な鍵-3" , 5:"呪いの鍵-5" , 10:"危険な鍵-10" ,50:"絶望の鍵-50" ,100:"絶対絶命の鍵-100"}
		w = [46 ,21, 16 ,11 , 5 , 1]
	elif (1001 <= user["key"]) :
		key_sets  = {1:"不幸の鍵-1" , 3:"不運な鍵-3" , 5:"呪いの鍵-5" , 10:"危険な鍵-10" ,50:"絶望の鍵-50" ,100:"絶対絶命の鍵-100",0:""}
		w = [46 ,20, 15 ,10 , 5 , 3, 1]

	get,txt = random.choices(list(key_sets.items()),weights=w)[0]

	if (get == 0) :
		get = int(user["key"] / 5)
		txt = f"終焉の鍵-{get}"

	user["key"] -= get
	sub_def.save_user(user)

	html = f"""
		<div class="battle_keyget"><span class="red">{txt}</span>を拾ってしまった！</div>
	"""
	print(html)

#戦闘後処理↓---------------
def battle_end(Fend,s,special) :
	#import time
	import sub_def
	import conf
	import cgi_py
	Conf = conf.Conf

	user = sub_def.open_user()
	party = sub_def.open_party()
	battle = sub_def.open_battle()

	pt_num = min(len(party) ,3)

	if (special in ("わたぼう","スライム")) :
		pt_num = 1

	exp = max(int(battle["teki"][0]["exp"] * s /pt_num) ,0)
	money = int(battle["teki"][0]["money"] * s)

	if (Conf["event_boost"]) :
		exp *= 2
		money *= 2

	exp2 = sub_def.slim_number(exp)
	money2 = sub_def.slim_number(money)

	html = f"""
		<div class="battle_log_Lvup">
			戦闘に<span class="red">{Fend}</span><br>
			<span class="sky_blue"">{money2}</span>Gを得た。<br>
			それぞれ<span class="sky_blue"">{exp2}</span>ポイントの経験値を得た。
		</div>
	"""
	print(html)

	if (s != 0) :
		user["money"] = min(user["money"] + money , 99999999999999) # 99兆
		for i,pt in enumerate(battle["party"]):
			if (pt["hp"] <= 0) :
				continue
			if (pt["lv"] != pt["mlv"]) :
				pt0 = pt.copy()	#ステ退避
				pt0["exp"] += exp
				pt0 = cgi_py.battle_sub.Lv_up_check(pt0,pt)
				battle["party"][i] = pt0.copy()	#ステ戻し

	for i,pt in enumerate(battle["party"]):
		party[i] = pt

	if (party[0]["hp"] == 0) :
		party[0]["hp"] = 1

	sub_def.save_user(user)
	sub_def.save_party(party)





1
