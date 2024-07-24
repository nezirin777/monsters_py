def yadoya(FORM) :
	import sub_def

	yadodai	= int(FORM["yadodai"])
	money	= int(FORM["money"])
	token = FORM["token"]

	if not(yadodai) :
		sub_def.error("現在宿泊する必要はありません")
	if (money < yadodai) :
		sub_def.error("お金が足りません")

	html = f"""
		<form method="post">
			<button>宿泊する</button>
			<input type="hidden" name="mode" value="yadoya_ok">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	sub_def.result("宿泊しますか？",html,FORM["token"])

def yadoya_ok(FORM) :
	import sub_def

	user = sub_def.open_user()
	party = sub_def.open_party()

	yadodai = 0
	for pt in party :
		if (pt["hp"] != 0) :
			yadodai += pt["mhp"] - pt["hp"] + pt["mmp"] - pt["mp"]
			pt["hp"] = pt["mhp"]
			pt["mp"] = pt["mmp"]

	user["money"] -= int(yadodai)

	sub_def.save_user(user)
	sub_def.save_party(party)

	sub_def.result("HP・MPが全回復しました","",FORM["token"])
