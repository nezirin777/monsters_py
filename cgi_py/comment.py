def comment (FORM) :
	import urllib.parse
	import re #正規表現
	import sub_def

	in_name = FORM.get("name")
	mes = FORM.get("message" ,"")

	if not(2 <= len(mes) <= 50) :
		sub_def.error("2文字以上、50文字以下で入力して下さい。")

	mes = re.sub("[<, >,\r ,\n,]","-",urllib.parse.unquote(mes))

	u_list = sub_def.open_user_list()
	user = sub_def.open_user()

	u_list[in_name]["mes"] = mes
	user["mes"] = mes

	sub_def.save_user_list(u_list)
	sub_def.save_user(user)

	sub_def.result("メッセージは更新されました","",FORM["token"])
