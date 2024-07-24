def seitenkan (FORM) :
	import sub_def

	#配列位置に合わせるため-1
	no	= int(FORM["no"]) -1
	token = FORM["token"]

	if(no < 0) :
		sub_def.error("対象が選択されていません。")

	user = sub_def.open_user()
	party = sub_def.open_party()

	if (user["money"] < party[no]["hai"] * 100) :
		sub_def.error("お金が足りません")

	html = f"""
		<form method="post">
			<button>変換する</button>
			<input type="hidden" name="mode" value="seitenkan_ok">
			<input type="hidden" name="no" value="{no}">
			<input type="hidden" name="token" value="{token}">
		</form>
	"""

	sub_def.result("性別変換しますか？",html,FORM["token"])

def seitenkan_ok (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	#-1された値のためそのまま
	no	= int(FORM["no"])

	user = sub_def.open_user()
	party = sub_def.open_party()
	pt = party[no]

	if (pt["sex"] == Conf["sex"][0]) :
		pt["sex"] = Conf["sex"][1]
	else :
		pt["sex"] = Conf["sex"][0]

	user["money"] -= pt["hai"] * 100

	sub_def.save_user(user)
	sub_def.save_party(party)

	sub_def.result("陰陽転換が完了しました","",FORM["token"])
