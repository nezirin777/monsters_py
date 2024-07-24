def omiai_room(FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM["name"]
	page = int(FORM.get("page",1))
	token = FORM["token"]

	party = sub_def.open_party()
	omiai_list = sub_def.open_omiai_list()

	p2 = page * 10
	p1 = p2 - 9

	def omiai_monster(omiai,target,mode,val,mode2="",val2="") :
		omiai_v = sub_def.slim_number(omiai)
		html =""
		if (val2) :
			html = f"""
					<form method="post">
						<input type="hidden" name="target" value="{target}">
						<input type="hidden" name="mode" value="{mode2}">
						<input type="hidden" name="token" value="{token}">
						<button>{val2}</button>
					</form>
			"""

		txt = f"""
			<div class="omiai_monster_box">
				<div class="omiai_st_1"><div class="omiai_st_title">ユーザー</div><div class="omiai_st_val">{target}</div>
					<form method="post">
						<input type="hidden" name="target" value="{target}">
						<input type="hidden" name="mode" value="{mode}">
						<input type="hidden" name="token" value="{token}">
						<button>{val}</button>
					</form>
					{html}
				</div>
				<div class="omiai_st_2"><img src="{Conf["imgpath"]}/{omiai["name"]}.gif"><br>{omiai["name"]}<br>-{omiai["sex"]}-<br>{omiai["sei"]}</div>
				<div class="omiai_st_box">
					<div class="omiai_st_3"><div class="omiai_st_title">LV<span>/最大LV</span></div><div class="omiai_st_val">{omiai["lv"]}<span>/{omiai["mlv"]}</span></div></div>
					<div class="omiai_st_3"><div class="omiai_st_title">HP<span>/最大HP</span></div><div class="omiai_st_val">{omiai_v["hp"]}<span>/{omiai_v["mhp"]}</span></div></div>
					<div class="omiai_st_3"><div class="omiai_st_title">配合</div><div class="omiai_st_val">{omiai["hai"]}回</div></div>
					<div class="omiai_st_3"><div class="omiai_st_title">攻撃力</div><div class="omiai_st_val">{omiai_v["atk"]}</div></div>
				</div>
				<div class="omiai_st_1"><div class="omiai_st_title">希望モンスター</div><div class="omiai_st_val">{omiai["mes"]}</div></div>
			</div>
		"""
		return txt

	request_user , mes , cancel , txt2 , txt3 , txt4 , txt5 ,txt6 = "","","","","","","",""
	#自分の登録モンスターチェック
	#ベイビーがいるか確認
	if(omiai_list.get(in_name)) :
		omiai = omiai_list[in_name]

		if not(omiai["baby"]) :
			txt2 = omiai_monster(omiai,in_name,"omiai_touroku_cancel","登録解除")
			request_user = omiai["request"]
			cancel = omiai["cancel"]
		else :
			txt6 = omiai_monster(omiai,in_name,"omiai_baby_get","受け取る")
			mes = omiai["mes"]

		#自分に来ている申請確認
		for name,v in omiai_list.items() :
			if (v["request"] == in_name) :
				txt3 += omiai_monster(v,name,"omiai_answer_ok","受け入れる","omiai_answer_no","お断りする")

		#自分が出している申請確認
		if(omiai_list.get(request_user)) :
			txt4 = omiai_monster(omiai_list[request_user],request_user,"omiai_request_cancel","申請キャンセル")

	#お見合い所に登録されているモンスターチェック
	#自分じゃない、依頼してない、されてない、誕生モンスターじゃない

	for name,v in list(omiai_list.items())[p1-1:p2-1] :
		if (name not in(in_name,request_user) and v["request"] != in_name and v["baby"] == "") :
			txt5 += omiai_monster(v,name,"omiai_request","申し込む")

	#以下出力
	html = f"""
		<div id="result">
			<span>お見合い所にモンスターを登録することができます<br>Lv{Conf["haigoulevel"]}以上必要です<br>登録できるのは1体だけです</span>
		</div>
	"""

	if not(txt2) :
		#登録可能モンスター表示
		txt = ""
		for i,pt in enumerate(party,1) :
			if (pt["lv"] >= Conf["haigoulevel"]) :
				txt += f"""<option value={i}>0{i}: {pt["name"]} {pt["sex"]} LV-{pt["lv"]} 配合{pt["hai"]}回</option>"""

		# name=haigou1は画像切り替えスクリプトを共通使用してるために変更しない。
		html += f"""
			<form name=form1 method="post">
				<select name="haigou1" onClick="change_img1()">
					<option value=0 SELECTED>登録するモンスターを選んでください</option>
					{txt}
				</select>
				<br>
				<IMG NAME="img1" SRC="{Conf["imgpath"]}/0.gif">
				<br>
				<input type="text" name="mes" size=30 value="" placeholder="希望相手モンスターを入力">
				<br>
				<button>登録する</button>
				<input type="hidden" name="mode" value="omiai_touroku">
				<input type="hidden" name="token" value="{token}">
				<br>
			</form>
			<form method="post">
				<input type="hidden" name="mode" value="my_page">
				<input type="hidden" name="token" value="{token}">
				<button>マイページへ</button>
			</form>
		"""
	else  :
		html += f"""
			<HR>
			<div id="result">
				<span>あなたが登録しているモンスター</span>
			</div>
			<div class="omiai_pt">{txt2}</div>
		"""

	if (txt3) :
		html += f"""
			<div id="result">
				<span>あなたとお見合いを望んでる相手</span>
			</div>
			<div class="omiai_pt">{txt3}</div>
		"""

	if (txt4) :
		html += f"""
			<div id="result">
				<span>あなたがお見合い依頼している相手</span>
			</div>
			<div class="omiai_pt">{txt4}</div>
		"""
	elif (cancel) :
			html += f"""
				<div id="result">
					<span>あなたがお見合い依頼している相手</span>
				</div>
				<div class="omiai_mes">{cancel}</div>
			"""

	if (txt5) :
		page_p = page - 1
		page_n = page + 1
		tex_p = ""
		if (page_p) :
			tex_p += f"""
			<form method="post">
				<input type="hidden" name="mode" value="omiai_room">
				<input type="hidden" name="page" value="{page_p}">
				<input type="hidden" name="token" value="{token}">
				<button>前の区画</button>
			</form>
			"""

		if (p2+2 <= len(omiai_list)) :
			tex_p += f"""
			<form method="post">
				<input type="hidden" name="mode" value="omiai_room">
				<input type="hidden" name="page" value="{page_n}">
				<input type="hidden" name="token" value="{token}">
				<button>次の区画</button>
			</form>
			"""

		html += f"""
			<HR>
			<div id="result">
				<span>お見合い所に登録されているモンスター<br>
						{page}ページ目
				</span>
			</div>
			<div class="park_page">{tex_p}</div>
			<div class="omiai_pt">{txt5}</div>
			<div class="park_page">{tex_p}</div>
		"""
	else  :
		html += f"""
			<HR>
			<div id="result">
				<span>お見合い所に登録されているモンスター<br>他に登録されてるモンスターはいないようです･･･</span>
			</div>
		"""

	if (txt6) :
		html = f"""
			<HR>
			<div id="result">
				<span>{mes}<br>受け取るには配合回数×5000Gが必要です</span>
			</div>
			<div class="omiai_pt">{txt6}</div>
		"""

	sub_def.header()
	sub_def.jscript(party,"","")
	print(html)
	sub_def.my_page_button(FORM["token"])
