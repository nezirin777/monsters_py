
def name_change(FORM) :
	import sub_def

	in_name = FORM.get("name")
	token = FORM["token"]

	omiai_list = sub_def.open_omiai_list()

	if (omiai_list.get(in_name)) :
		sub_def.error("お見合い所を使用中はユーザー名の変更ができません。")

	html = f"""
		<div id="result">
			<span>ユーザー名を変更します<br>使用可能な文字は半角/全角英数字及び日本語です</span>
		</div>
		<br>
		<div class="my_page">
			<form method="post">
				<span>現在の名前</span>
				<input type="text" size="14" name="name" value="{in_name}" disabled><br>
				<span>新しい名前</span>
				<input type="text" size="14" name="new_name" value=""><br>
				<input type="hidden" name="mode" value="name_change_check">
				<input type="hidden" name="token" value="{token}">
				<button>確認する</button>
			</form>
		</div>
	"""

	sub_def.header()
	print(html)
	sub_def.my_page_button(token)

def name_change_check(FORM) :
	import os
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM["name"]
	new_name = FORM["new_name"]
	in_pass = FORM["password"]
	token = FORM["token"]

	if (new_name == "") :
		sub_def.error("新しい名前がありません")

	if (new_name == in_pass) :
		sub_def.error("新しい名前とパスワードは違うものにして下さい")

	if (len(new_name) > 20) :
		sub_def.error("新しい名前は20文字以下で入力して下さい。")

	val = ['　' , ' ' , '\\' , '/' , ';' , ':'  , ',' , '*' , '?' , '\'' , '<' , '>' , '|' , '"' , '~' , '$' , '&' , '`' , '^' ]
	for i in val :
		if (i in in_name) :
			sub_def.error(f"使用できない文字 {i} が含まれています","top")

	if (os.path.exists(Conf["datadir"]+ "/" + new_name)) :
		sub_def.error("その名前は既に登録されています","top")

	u_list = sub_def.open_user_list()

	for u_name in u_list :
		if(u_name.casefold() == new_name.casefold()) :
			sub_def.error("その名前では登録することができません。","top")

	html = f"""
		<div id="result">
			<span>ユーザー名を<span>{in_name}</span>から<br><span>{new_name}</span>へと変更します。<br>よろしいですか？</span>
		</div>
		<br>
		<div>
			<form method="post">
				<input type="hidden" name="mode" value="name_change_ok">
				<input type="hidden" name="new_name" value="{new_name}">
				<input type="hidden" name="token" value="{token}">
				<button>変更する</button>
			</form>
		</div>
	"""

	sub_def.header()
	print(html)
	sub_def.my_page_button(token)

def name_change_ok(FORM) :
	import os
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM["name"]
	new_name = FORM["new_name"]

	u_list = sub_def.open_user_list()

	u_list[new_name] = u_list[in_name]
	del u_list[in_name]
	sub_def.save_user_list(u_list)

	user = sub_def.open_user(in_name)
	user["name"] = new_name
	sub_def.save_user(user,in_name)

	FORM["c"] |= {"in_name":new_name}
	sub_def.set_cookie(FORM["c"])
	sub_def.set_session({"name":new_name,"password":FORM["password"],"token":FORM["token"]})

	os.rename(f"""{Conf["datadir"]}/{in_name}/""", f"""{Conf["datadir"]}/{new_name}/""")

	sub_def.result(f"""ユーザー名を<span>{in_name}</span>から<br><span>{new_name}</span>へと変更しました。""","",FORM["token"])
