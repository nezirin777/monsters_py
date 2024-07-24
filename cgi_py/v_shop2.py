#100vips = 50メダル,10vips = 5メダル,1vips = 0.5メダル

def v_shop2 (FORM) :
	import sub_def

	token = FORM["token"]

	vips = sub_def.open_vips()
	vshop_list = sub_def.open_vips_shop2_dat()

	if (vips.get("パーク",0)) :
		del vshop_list["モンスターパーク"]
	else :
		del vshop_list["パーク拡大+5枠"]

	html = ""
	for name,li in vshop_list.items():
		html += f"""
			<div class="medal_box1">
				<div class="medal_name">{name}</div>
				<div class="medal_val">メダル{li["price"]}枚
					<form method="post">
						<button>交換する</button>
						<input type="hidden" name="mode" value="v_shop2_ok">
						<input type="hidden" name="token" value="{token}">
						<input type="hidden" name="m_name" value="{name}">
					</form>
				</div>
			</div>
		"""

	html = f"""<div class="medal_box">{html}</div>"""

	sub_def.result("交換したいアイテムを選んでください<br>確認画面は出ないので注意。",html,FORM["token"])

def v_shop2_ok(FORM) :
	import sub_def

	if not(FORM.get("m_name")) :
		sub_def.error("対象が選択されていません。")

	m_name = FORM["m_name"]
	token = FORM["token"]

	vips = sub_def.open_vips()
	user = sub_def.open_user()
	vshop_list = sub_def.open_vips_shop2_dat()

	price = vshop_list[m_name]["price"]

	if (user["medal"] < price) :
		sub_def.error("メダルが足りません！")

	user["medal"] -= price

	b_name = vshop_list[m_name]["b_name"]
	if(vips.get(b_name,0) == "") :
		vips[b_name] = 0
	vips[b_name] = int(vips.get(b_name,0)) + 1

	sub_def.save_user(user)
	sub_def.save_vips(vips)

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="v_shop2">
			<input type="hidden" name="token" value="{token}">
			<button>交換所に戻る</button>
		</form>
	"""

	sub_def.result(f"{m_name}を購入しました。",html,FORM["token"])
