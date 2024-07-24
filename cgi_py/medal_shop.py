
def medal_shop (FORM) :
	import sub_def

	token = FORM["token"]

	def mlist (Medal_lsit,type,val1,val2) :
		html = ""
		for name,list in Medal_lsit.items() :
			if(list["type"] == type) :
				s_price = sub_def.slim_number(list["price"])
				html += f"""
					<div class="medal_box1">
						<input type="radio" name="m_name" value="{name}">
						<div class="medal_name">{name}</div>
						<div class="medal_val">{val1}{s_price}{val2}</div>
					</div>
				"""
		return html

	Medal_lsit = sub_def.open_medal_shop_dat()
	html1 = mlist(Medal_lsit,"メダル","メダル","枚")
	html2 = mlist(Medal_lsit,"G","","G")

	html = f"""
		<form method="post">
			<div class="medal_box">{html1}</div>
			<div class="medal_box">{html2}</div>

			<button>交換する</button>
			<input type="hidden" name="mode" value="medal_shop_ok">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	sub_def.result("交換したいモンスターを選んでください<br>確認画面は出ないので注意。",html,FORM["token"])

def medal_shop_ok(FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	if not(FORM.get("m_name")) :
		sub_def.error("対象が選択されていません。")

	m_name = FORM["m_name"]

	Medal_lsit = sub_def.open_medal_shop_dat()
	user = sub_def.open_user()
	party = sub_def.open_party()

	price = Medal_lsit[m_name]["price"]

	if (len(party) >= 10) :
		sub_def.error("モンスターが一杯です！")

	new_mob = sub_def.monster_select(m_name)
	party.append(new_mob)

	for i,pt in enumerate(party,1) :
		pt["no"] = i

	if (Medal_lsit[m_name]["type"] == "メダル") :
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

	sub_def.result(f"""<img src="{Conf["imgpath"]}/{m_name}.gif"><span>{m_name}</span>が仲間に加わりました""","",FORM["token"])
