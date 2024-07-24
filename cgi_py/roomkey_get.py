def roomkey_get (FORM) :
	import sub_def

	get_key = FORM.get("get_key")

	if not(get_key) :
		sub_def.error("エラーが発生しました。<br>roomkey_get")

	room_key = sub_def.open_room_key()
	room_key[get_key]["get"] = 1
	sub_def.save_room_key(room_key)

	sub_def.result(f"""{get_key}の部屋の鍵を入手した！""","",FORM["token"])
