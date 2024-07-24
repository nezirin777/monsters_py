def kyoukai (FORM) :
	import sub_def

	kyoukaidai	= int(FORM["kyoukaidai"])
	money	= int(FORM["money"])
	token = FORM["token"]

	if ( money < kyoukaidai) :
		sub_def.error("お金が足りません")

	if (kyoukaidai == 0) :
		sub_def.error("現在お祈りする必要はありません")

	html = f"""
		<form method="post">
			<button>お祈りする</button>
			<input type="hidden" name="mode" value="kyoukai_ok">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	sub_def.result("お祈りしますか？",html,FORM["token"])

def kyoukai_ok (FORM) :
	import sub_def

	user = sub_def.open_user()
	party = sub_def.open_party()

	kyoukai = 0
	for pt in party :
		if (pt["hp"] == 0) :
			pt["hp"] = pt["mhp"]
			pt["mp"] = pt["mmp"]
			kyoukai += (pt["mhp"] + pt["mmp"]) * 2

	user["money"] -= int(kyoukai)

	sub_def.save_user(user)
	sub_def.save_party(party)

	sub_def.result("お祈りが天にとどきました","",FORM["token"])
