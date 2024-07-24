#100vips = 50メダル,10vips = 5メダル,1vips = 0.5メダル

def v_shop (FORM) :
	import sub_def

	token = FORM["token"]

	vips = sub_def.open_vips()
	zukan = sub_def.open_zukan()

	def mlist(vshop_list,type,val1,val2) :
		html = ""

		for name,li in vshop_list.items() :
			if (zukan[li["b_name"]]["get"]) :
				if (li["type"] == type) :
					price_v = sub_def.slim_number(li["price"] + li["price"] *  vips.get(name,0))
					html += f"""
						<div class="medal_box1">
							<input type="radio" name="m_name" value="{name}">
							<div class="medal_name">{name}</div>
							<div class="medal_val">{val1}{price_v}{val2}</div>
						</div>
					"""
		return html

	vshop_list = sub_def.open_vips_shop_dat()
	html1 = mlist(vshop_list,"メダル","メダル","枚")
	html2 = mlist(vshop_list,"G","","G")

	html = f"""
		<div class="medal_box">
			<form method="post">
				<div class="medal_box">{html1}</div>
				<div class="medal_box">{html2}</div>
				<button>交換する</button>
				<input type="hidden" name="mode" value="v_shop_ok">
				<input type="hidden" name="token" value="{token}">
			</form>
		</div>
	"""

	mes = f"交換したいモンスターを選んでください<br>交換回数に応じて値段が上がっていきます。<br>確認画面は出ないので注意。"
	sub_def.result(mes,html,FORM["token"])

def v_shop_ok(FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	if not(FORM.get("m_name")) :
		sub_def.error("対象が選択されていません。")

	token = FORM["token"]
	m_name = FORM["m_name"]

	vshop_list = sub_def.open_vips_shop_dat()
	user = sub_def.open_user()
	party = sub_def.open_party()
	vips = sub_def.open_vips()

	Aname = vshop_list[m_name]["b_name"]
	new_mob = sub_def.monster_select(Aname)

	if (len(party) >= 10) :
		sub_def.error("モンスターが一杯です！")

	if (m_name == "スライム+100") :
			new_mob["hai"] = 100
			new_mob["mlv"] = 100
	elif (m_name == "スライム+1000") :
			new_mob["hai"] = 1000
			new_mob["mlv"] = 1000

	new_mob["lv"] = 1
	party.append(new_mob)
	for i,pt in enumerate(party,1) :
		pt["no"] = i

	buy_count = vips.get(m_name,0)
	vips[m_name] = buy_count + 1

	price = vshop_list[m_name]["price"] + vshop_list[m_name]["price"] * buy_count

	if (vshop_list[m_name]["type"] == "メダル") :
		if (user["medal"] < price) :
			sub_def.error("メダルが足りません！")
		else :
			user["medal"] -= price
	else :
		if (user["money"] < price) :
			sub_def.error("お金が足りません！")
		else :
			user["money"] -= price

	sub_def.save_user(user)
	sub_def.save_party(party)
	sub_def.save_vips(vips)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="v_shop">
			<input type="hidden" name="token" value="{token}">
			<button>交換所に戻る</button>
		</form>
	"""

	sub_def.result(f"""<img src="{Conf["imgpath"]}/{Aname}.gif"><span>{m_name}</span>が仲間に加わりました""",html,FORM["token"])
