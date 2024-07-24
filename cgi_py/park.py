def park (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	page = int(FORM.get("page",1))
	token = FORM["token"]
	sort_v = int(FORM.get("sort_v",0))

	party = sub_def.open_party()
	park = sub_def.open_park()
	vips = sub_def.open_vips()

	if (vips.get("パーク",0) == 0 or vips.get("パーク",0) == "" ) :
		sub_def.error("モンスターパークを所有していません。")

	#手持ちパーティ表示部
	waku =	int(vips["パーク"] * 5)
	azukari = len(park)

	txt = "".join([f"""<option value={pt["no"]}>{pt["no"]}: {pt["name"]} {pt["sex"]} LV-{pt["lv"]} 配合{pt["hai"]}回</option>"""
	for pt in party])

	html = f"""
		<div id="result">
			<span>モンスターパーク<br>モンスターを預けたりパーティに加えたりできます<br>預かり状況：{azukari}/{waku}体。</span>
		</div>

		<form name=form1 method="post">
			<select name="Mno" onClick="change_img()">
				<option value=0 hidden>預けるモンスターを選んでください</option>
				{txt}
			</select>
			<button>預ける</button>
			<input type="hidden" name="mode" value="park_1">
			<input type="hidden" name="token" value="{token}">
			<br>
			<IMG NAME="img1" SRC="{Conf["imgpath"]}/0.gif">
		</form>
		<form method="post">
			<input type="hidden" name="mode" value="my_page">
			<input type="hidden" name="token" value="{token}">
			<button>マイページへ</button>
		</form>
	"""

	#====================##====================##====================##====================#
	#パーク内モンスター表示


	if(len(park) == 0 or not any(park[0])) :
		html += f"""
			<HR>
			<div id="result">
				<span>パーク内にいるモンスター<br>
						現在預けているモンスターはいません。
				</span>
			</div>
		"""
		sub_def.header()
		sub_def.jscript(party,"","")
		print(html)
		sub_def.my_page_button(token)
	#預けてるモンスターがいなければここで終わり。

	if (sort_v == 1) :
		park.sort(key=lambda x: x["name"])
		for i,ppt in enumerate(park,1) :
			ppt["no"] = i
		sub_def.save_park(park)
	elif (sort_v == 2) :
		mlist = sub_def.open_monster_dat()
		tmp = []
		for name in mlist.keys() :
			for p in park :
				if (name == p["name"]) :
					tmp.append(p)
		park = tmp
		for i,ppt in enumerate(park,1) :
			ppt["no"] = i
		sub_def.save_park(park)

	p1 = (page - 1) * 10
	p2 = min(page * 10,waku)
	jump_count =  -(-len(park) // 10)

	park_v = sub_def.slim_number(park)

	temp = "".join([
		f"""
			<form method="post" class="park_jump_form">
				<input type="hidden" name="mode" value="park">
				<input type="hidden" name="page" value="{i}">
				<input type="hidden" name="token" value="{token}">
				<input type="submit" value="{str(i).rjust(2, '0')}区">
			</form>
		"""
		for i in range(1,jump_count+1)
	])
	jump_link = f"<div class='park_page'>{temp}</div>"


	txt = f"""
			<div class="park_ste">
				<div class="park_width">NO</div>
				<div class="park_mname">キャラ</div>
				<div class="park_width">配合</div>
				<div class="park_width">LV/<br>最大LV</div>
				<div class="park_width">HP/<br>最大HP</div>
				<div class="park_width">MP/<br>最大MP</div>
				<div class="park_width">攻撃力</div>
				<div class="park_width">守備力</div>
				<div class="park_width">素早さ</div>
			</div>
	"""

	txt += "".join([
			f"""
				<div  class="park_mob">
					<div class="park_width">{ppt["no"]}
						<form method="post">
							<input type="hidden" name="mob" value="{ppt["no"]}">
							<input type="hidden" name="mode" value="park_2">
							<input type="hidden" name="token" value="{token}">
							<button>連れていく</button>
						</form>
					</div>
					<div class="park_mname"><img src="{Conf["imgpath"]}/{ppt["name"]}.gif"><br>{ppt["name"]}<br>{ppt["sex"]}<br>【{ppt["sei"]}】</div>
					<div class="park_width">{ppt["hai"]}回</div>
					<div class="park_width">{ppt["lv"]}<br>{ppt["mlv"]}</div>
					<div class="park_width">{ppt["hp"]}<br>{ppt["mhp"]}</div>
					<div class="park_width">{ppt["mp"]}<br>{ppt["mmp"]}</div>
					<div class="park_width">{ppt["atk"]}</div>
					<div class="park_width">{ppt["def"]}</div>
					<div class="park_width">{ppt["agi"]}</div>
				</div>
			"""
			for ppt in park_v[p1:p2 :]
	])


	html += f"""
			<HR>
			<div id="result">
				<span>パーク内にいるモンスター<br>
						{page}区画目<br>
						No.{p1+1} ～ No.{p2}<br>
				</span>
			</div>
			<form method="post" class="park_jump_form">
				<input type="hidden" name="mode" value="park">
				<input type="hidden" name="page" value="1">
				<input type="hidden" name="sort_v" value="1">
				<input type="hidden" name="token" value="{token}">
				<input type="submit" value="名前でソート">
			</form>
			<form method="post" class="park_jump_form">
				<input type="hidden" name="mode" value="park">
				<input type="hidden" name="page" value="1">
				<input type="hidden" name="sort_v" value="2">
				<input type="hidden" name="token" value="{token}">
				<input type="submit" value="図鑑順でソート">
			</form>
			{jump_link}
			<div class="park_box">{txt}</div>
			{jump_link}
	"""

	sub_def.header()
	sub_def.jscript(party,"","")
	print(html)
	sub_def.my_page_button(token)

#====================##====================##====================##====================##====================#
#手持ちを預ける
def park_1 (FORM) :
	import sub_def

	#配列位置を合わせるため-1
	Mno	= int(FORM["Mno"]) -1
	token = FORM["token"]

	party = sub_def.open_party()
	park = sub_def.open_park()
	vips = sub_def.open_vips()

	waku = vips["パーク"] * 5

	if (len(party) == 1) :
		sub_def.error("パーティーがいなくなってしまいます。<br>預けることができません。")

	if (len(park) >= waku) :
		sub_def.error("パークがいっぱいで預けることができませんでした。")

	mes = f"""<span>{party[Mno]["name"]}</span>を預けました。"""

	park.append(party[Mno])
	del party[Mno]

	for i,pt in enumerate(party,1) :
		pt["no"] = i
	for i,ppt in enumerate(park,1) :
		ppt["no"] = i

	sub_def.save_park(park)
	sub_def.save_party(party)

	html = f"""
		<form method="post">
		<input type="hidden" name="mode" value="park">
		<input type="hidden" name="token" value="{token}">
		<button>パークに戻る</button>
		</form>
	"""

	sub_def.result(mes,html,FORM["token"])

#====================##====================##====================##====================##====================#
#パークから連れていく
def park_2 (FORM) :
	import sub_def

	#配列位置を合わせるため-1
	Mno	= int(FORM["mob"]) -1
	token = FORM["token"]

	party = sub_def.open_party()
	park = sub_def.open_park()

	mes = ""
	if (len(party) < 10) :
		party.append(park[Mno])
		mes = f"""<span>{park[Mno]["name"]}</span>をパーティに加えました。"""
		del park[Mno]
		for i,pt in enumerate(party,1) :
			pt["no"] = i
		for i,ppt in enumerate(park,1) :
			ppt["no"] = i
	else :
		sub_def.error("パーティがいっぱいで連れていくことができませんでした。")

	sub_def.save_party(party)
	sub_def.save_park(park)

	html = f"""
		<form method="post">
		<input type="hidden" name="mode" value="park">
		<input type="hidden" name="token" value="{token}">
		<button>パークに戻る</button>
		</form>
	"""

	sub_def.result(mes,html,FORM["token"])
