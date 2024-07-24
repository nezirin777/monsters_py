
def books (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	token = FORM["token"]

	party = sub_def.open_party()

	txt1 = ""
	txt2 = ""

	for pt in party :
		txt1 += f"""
			<div class="books_mbox1">
				<div class="books_no">{pt["no"]}</div>
				<div class="books_im"><img src="{Conf["imgpath"]}/{pt["name"]}.gif"></div>
				<div class="books_m">{pt["name"]}<br>-{pt["sex"]}-<br>{pt["sei"]}</div>
			</div>
		"""
		txt2 += f"""<option value={pt["no"]}>{pt["no"]}-{pt["name"]}</option>"""

	mes = f"""
			モンスターに本を読ませると性格が変わります。<br>
			現在の性格によっては変わらない場合もあります。<br>
			1冊1000G。
	"""

	html = f"""
		<div id="books_mbox">{txt1}</div>
		<form method="post">
			<div class="books_text3">モンスターを選択して下さい</div>
			<select name=Mno>{txt2}</select>
			<div class="books_text3">本を選択して下さい</div>
			<select name=Bname>
				<option value="ぼうけんたん">ぼうけんたん</option>
				<option value="こわいはなしのほん">こわいはなしのほん</option>
				<option value="やさしくなれるほん">やさしくなれるほん</option>
				<option value="ずるっこのほん">ずるっこのほん</option>
				<option value="あたまがさえるほん">あたまがさえるほん</option>
				<option value="ユーモアのほん">ユーモアのほん</option>
			</select>
			<br>
			<br>
			<button>本を読む</button>
			<input type="hidden" name="mode" value="book_read">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	sub_def.result(mes,html,FORM["token"])


def book_read (FORM) :
	import sub_def

	#実際の配列位置に合わせるため-1
	Mno	= int(FORM["Mno"]) -1
	Bname = FORM["Bname"]

	token = FORM["token"]

	user = sub_def.open_user()
	party = sub_def.open_party()
	Book_dat = sub_def.open_book_dat()
	seikaku = sub_def.open_seikaku_dat()

	if (user["money"] < 1000) :
		sub_def.error("お金が足りません")

	user["money"] -= 1000

	Msei = party[Mno]["sei"]
	Newsei = Msei

	yuuki	 = 	min(3, max(1 ,seikaku[Msei]["勇気"] + Book_dat[Bname]["勇気"]))
	yasasisa =	min(3, max(1 ,seikaku[Msei]["優しさ"] + Book_dat[Bname]["優しさ"]))
	tisei	 = 	min(3, max(1 ,seikaku[Msei]["知性"] + Book_dat[Bname]["知性"]))

	for name,v in seikaku.items() :
		if (v["勇気"] == yuuki and v["優しさ"] == yasasisa and v["知性"] == tisei) :
			Newsei = name
			break

	party[Mno]["sei"] = Newsei

	sub_def.save_user(user)
	sub_def.save_party(party)

	if (Msei == Newsei) :
		mes = "モンスターの性格は変わらなかった"
	else :
		mes = f"""性格が【{Msei}】から【{Newsei}】に変わった"""

	html = f"""
		<form method="post">
			<input type="hidden" name="mode" value="books">
			<input type="hidden" name="token" value="{token}">
			<button>本屋へ戻る</button>
		</form>
	"""

	sub_def.result(mes,html,FORM["token"])
