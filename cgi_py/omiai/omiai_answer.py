def omiai_answer_no(FORM) :
	import sub_def

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	omiai_list[target]["request"] = ""
	omiai_list[target]["cancel"] = f"{in_name}さんへの依頼はお断りされてしまったようです・・・"

	sub_def.save_omiai_list(omiai_list)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value={token}>
			<button>お見合い所に戻る</button>
		</form>
	"""
	sub_def.result(f"{target}さんからの申し込みをお断りしました。",html,FORM["token"])

def omiai_answer_ok(FORM) :
	import sub_def
	import conf
	import cgi_py

	Conf = conf.Conf

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	if(omiai_list[in_name]["request"]) :
		sub_def.error("あなたは他の人に申請中です。<br>この人とお見合いするには申請を取り下げる必要があります。")

	nameA = omiai_list[in_name]["name"]
	nameB = omiai_list[target]["name"]

	my_new_mons = cgi_py.haigou_check.haigou_sub(nameA,nameB,1)

	zukan = sub_def.open_zukan()
	if not(zukan[my_new_mons]["get"]) :
		my_new_mons = "？？？"

	html = f"""
		<div class="hai_title">お見合いをしますか？</div>

		<div class="hai_box">
			<div class="hai_box1">
				<div class="hai_1">自　分</div>
				<div class="hai_img"><img src="{Conf["imgpath"]}/{nameA}.gif"></div>
				<div class="hai_name">{nameA}</div>
			</div>
			<div class="hai_box1">
				<div class="hai_1">相　手</div>
				<div class="hai_img"><img src="{Conf["imgpath"]}/{nameB}.gif"></div>
				<div class="hai_name">{nameB}</div>
			</div>
		</div>

		<div class="hai_title">NEW MONSTER</div>

		<div class="hai_box3">
			<div class="hai_1">予　想</div>
			<div class="hai_img"><img src="{Conf["imgpath"]}/{my_new_mons}.gif"></div>
			<div class="hai_name">{my_new_mons}</div>
		</div>

		<form method="post">
			<button>お見合い OK!</button>
			<input type="hidden" name="mode" value="omiai_answer_result">
			<input type="hidden" name="target" value="{target}">
			<input type="hidden" name="token" value="{token}">
		</form>

		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value="{token}">
			<button>キャンセル</button>
		</form>
	"""

	sub_def.header()
	print(html)
	sub_def.footer()

def omiai_answer_result(FORM) :
	import sub_def
	import conf
	import cgi_py

	Conf = conf.Conf

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	#自分、相手への依頼を全キャンセル
	for name,omiai in omiai_list.items() :
		if(omiai["request"] == in_name) :
			omiai_list[name]["request"] = ""
			omiai_list[name]["cancel"] = f"{in_name}さんへの依頼はお断りされてしまったようです・・・"
		if(omiai["request"] == target) :
			omiai_list[name]["request"] = ""
			omiai_list[name]["cancel"] = f"{target}さんへの依頼はお断りされてしまったようです・・・"

	def omiai_get_monster(data,new_mons,user_name) :
		mlv = data["lv"] +10
		new_hai = data["hai"] +1
		hosei = max(int(new_hai /2) ,1)

		new_mob = sub_def.monster_select(new_mons,hosei,1,user_name)

		new_mob["lv"] = 1
		new_mob["mlv"] = mlv
		new_mob["hai"] = new_hai

		return new_mob

	my_data = omiai_list[in_name]
	target_data = omiai_list[target]

	my_new_mons_name = cgi_py.haigou_check.haigou_sub(my_data["name"],target_data["name"],1)
	target_new_mons_name = cgi_py.haigou_check.haigou_sub(target_data["name"],my_data["name"],1)

	my_new_mons = omiai_get_monster(my_data,my_new_mons_name,in_name)
	target_new_mons = omiai_get_monster(target_data,target_new_mons_name,target)

	my_data.update(my_new_mons)
	my_data["mes"] = f"{target}さんとのお見合いが成功しました。"
	my_data["baby"] = 1

	target_data.update(target_new_mons)
	target_data["mes"] = f"{in_name}さんとのお見合いが成功しました。"
	target_data["baby"] = 1

	sub_def.save_omiai_list(omiai_list)

	my_data = sub_def.slim_number(my_data)

	html = f"""
		<div class="hai_title">NEW MONSTER!</div>

		<div class="hen_box0">
			<div class="hen_box1">
				<div class="hen_text1">モンスター名</div>
				<div><img src="{Conf["imgpath"]}/{my_data["name"]}.gif"></div>
				<div class="hen_text2">{my_data["name"]}<br>{my_data["sex"]}<br>{my_data["sei"]}</div>
			</div>
		</div>

		<div class="hen_box2">
			<div class="hen_box3">
				<div class="hen_text1">Level</div>
				<div class="hen_text2">1 / {my_data["mlv"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">配合数</div>
				<div class="hen_text2">{my_data["hai"]}回</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">H P</div>
				<div class="hen_text2">{my_data["mhp"]} / {my_data["mhp"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">M P</div>
				<div class="hen_text2">{my_data["mmp"]} / {my_data["mmp"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">攻撃力</div>
				<div class="hen_text2">{my_data["atk"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">守備力</div>
				<div class="hen_text2">{my_data["def"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">素早さ</div>
				<div class="hen_text2">{my_data["agi"]}</div>
			</div>

			<div class="hen_box3">
				<div class="hen_text1">経験値</div>
				<div class="hen_text2">0 / {Conf["nextup"]}</div>
			</div>
		</div>

		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value={token}>
			<button>お見合い部屋に戻る</button>
		</form>
	"""

	sub_def.header()
	print(html)
	sub_def.my_page_button(token)
