
def haigou_sub (base,aite,flg=0) :
	#お見合いにも使用。
	import sub_def

	Aname,Bname = base ,aite

	if(Aname == "フィッシュル(制服)") :
		Aname = "フィッシュル"
	if(Bname == "フィッシュル(制服)") :
		Bname = "フィッシュル"

	M_list = sub_def.open_monster_dat()

	Atype = M_list[Aname]["m_type"]
	Btype = M_list[Bname]["m_type"]

	(newmons1,newmons2,newmons3,newmons4) = ( "" ,"" ,"" , "")

	for name,mon in M_list.items() :
		for n in range(1,4) :
			monA = mon[f"血統{n}"]
			monB = mon[f"相手{n}"]
			if (Atype == monA and Btype == monB) :#系統×系統
				newmons1 = name
			if ( (Atype == monA and Bname == monB) or (Aname == monA and Btype == monB) ) :#系統×個体 or 個体×系統
				newmons2 = name
			if (Aname == monA and Bname == monB) :#個体×個体
				newmons3 = name
			if (flg and Aname == mon[f"お見合いA{n}"] and Bname == mon[f"お見合いB{n}"]) :#個体×個体 お見合い用
				newmons4 = name

	return newmons4 or newmons3 or newmons2 or newmons1 or base

def haigou_check (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	#配列位置に合わせるため-1
	haigou1 = int(FORM["haigou1"]) -1
	haigou2 = int(FORM["haigou2"]) -1

	token = FORM["token"]

	if (haigou1 < 0 or haigou2 < 0) :
		sub_def.error("正しく設定されていません-1")
	if (haigou1 == haigou2) :
		sub_def.error("正しく設定されていません-2")

	user = sub_def.open_user()
	party = sub_def.open_party()
	zukan = sub_def.open_zukan()

	hai_A = party[haigou1]
	hai_B = party[haigou2]

	if (hai_A["sex"] == hai_B["sex"]) :
		sub_def.error("陰陽が同じで配合出来ません")

	if (hai_A["lv"] < Conf["haigoulevel"]) :
		sub_def.error(f"""<img src={Conf["imgpath"]}/{hai_A["name"]}.gif>のレベルが{Conf["haigoulevel"]}に達していません""")
	if (hai_B["lv"] < Conf["haigoulevel"]) :
		sub_def.error(f"""<img src={Conf["imgpath"]}/{hai_B["name"]}.gif>のレベルが{Conf["haigoulevel"]}に達していません""")

	money = ((hai_A["lv"] + hai_B["lv"]) * 10)

	if (user["money"] < money) :
		sub_def.error("お金が足りません")

	new_mons = haigou_sub(hai_A["name"],hai_B["name"])

	new_mons_name = ([new_mons for name,zu in zukan.items() if (new_mons == name and zu["get"])] or ["？？？"])[0]

	html = f"""
		<div class="hai_title">モンスターを合成しますか？</div>

		<div class="hai_box">
			<div class="hai_box1">
				<div class="hai_1">自　分</div>
				<div class="hai_img"><img src="{Conf["imgpath"]}/{hai_A["name"]}.gif"></div>
				<div class="hai_name">{hai_A["name"]}</div>
			</div>
			<div class="hai_box1">
				<div class="hai_1">相　手</div>
				<div class="hai_img"><img src="{Conf["imgpath"]}/{hai_B["name"]}.gif"></div>
				<div class="hai_name">{hai_B["name"]}</div>
			</div>
		</div>

		<div class="hai_title">NEW MONSTER</div>

		<div class="hai_box3">
			<div class="hai_1">結　果</div>
			<div class="hai_img"><img src="{Conf["imgpath"]}/{new_mons_name}.gif"></div>
			<div class="hai_name">{new_mons_name}</div>
		</div>

		<form method="post">
			<button>配合 OK!</button>
			<input type="hidden" name="mode" value="haigou_hensin">
			<input type="hidden" name="token" value="{token}">
		</form>

		<form method="post">
			<input type="hidden" name="token" value="{token}">
			<input type="hidden" name="mode" value="my_page">
			<button>キャンセル</button>
		</form>
	"""

	sub_def.set_session({"name":FORM["name"],"password":FORM["password"],"token":token,"new_mons":new_mons,"haigou1":haigou1,"haigou2":haigou2})

	sub_def.header()
	print(html)
	sub_def.footer()
