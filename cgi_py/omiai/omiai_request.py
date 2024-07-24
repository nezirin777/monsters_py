def omiai_request(FORM) :
	import sub_def
	import conf
	import cgi_py

	Conf = conf.Conf

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	my_data , target_data = "" ,""

	#自モンスターを登録済みかチェック
	my_data = omiai_list.get(in_name,0)
	target_data = omiai_list.get(target,0)

	if not(my_data) :
		sub_def.error("あなたはまだ未登録です。<br>登録してから申請してください")

	#すでに申請がないかチェック
	if (my_data["request"]) :
		sub_def.error("申請できるのは1人までです。<br>他の人に申請したい場合は申請をキャンセルしてからどうぞ。")

	#申請相手から依頼が来てないかチェック
	if (target_data["request"] == in_name) :
		sub_def.error(f"{target}さんからはすでに依頼が来てます。")

	#性別チェック
	if (my_data["sex"] == target_data["sex"]) :
		sub_def.error("性別が同じ為お見合いができません。")

	nameA = my_data["name"]
	nameB = target_data["name"]

	my_new_mons = cgi_py.haigou_check.haigou_sub(nameA,nameB,1)

	zukan = sub_def.open_zukan()
	if not(zukan[my_new_mons]["get"]) :
		my_new_mons = "？？？"

	html = f"""
		<div class="hai_title">お見合い申請をしますか？</div>

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
			<button>申請する</button>
			<input type="hidden" name="mode" value="omiai_request_ok">
			<input type="hidden" name="target" value="{target}">
			<input type="hidden" name="token" value={token}>
		</form>

		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value={token}>
			<button>キャンセル</button>
		</form>
	"""

	sub_def.header()
	print(html)
	sub_def.footer()

def omiai_request_ok(FORM) :
	import sub_def

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	#自分に申請記録
	omiai_list[in_name]["request"] = target
	request_monster = omiai_list[target]["name"]

	sub_def.save_omiai_list(omiai_list)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value={token}>
			<button>お見合い所に戻る</button>
		</form>
	"""

	sub_def.result(f"<span>{target}さん</span>の<span>{request_monster}</span>にお見合いを申請しました。",html,FORM["token"])

def omiai_request_cancel(FORM) :
	import sub_def

	in_name = FORM["name"]
	target = FORM["target"]
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	omiai_list[in_name]["request"] = ""
	sub_def.save_omiai_list(omiai_list)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="omiai_room">
			<input type="hidden" name="token" value="{token}">
			<button>お見合い所に戻る</button>
		</form>
	"""

	sub_def.result(f"{target}さんへの申請を取り消しました。",html,FORM["token"])
