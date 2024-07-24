
def my_page2 (FORM) :
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM.get("name")

	user = sub_def.open_user(in_name)
	party = sub_def.open_party(in_name)

	user_v = sub_def.slim_number(user)
	pt_v = sub_def.slim_number(party)

	isekai = "hidden"
	if (user.get("isekai_limit")) :
		isekai = ""

	#PT部分
	pt_txt = "".join([
		f"""
			<div class="my_page_chara_{i}">
				<div class="my_page_st_1">{i}</div>
				<div class="my_page_st_2"><img src="{Conf["imgpath"]}/{pt["name"]}.gif">{pt["name"]}<br>-{pt["sex"]}-<br>{pt["sei"]}</div>
				<div class="my_page_charabox">
					<div class="my_page_st_3"><div class="my_page_st_title">LV<span>/最大LV</span></div><div class="my_page_st_val">{pt["lv"]}<span>/{pt["mlv"]}</span></div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">HP<span>/最大HP</span></div><div class="my_page_st_val">{pt["hp"]}<span>/{pt["mhp"]}</span></div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">MP<span>/最大MP</span></div><div class="my_page_st_val">{pt["mp"]}<span>/{pt["mmp"]}</span></div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">経験値<span>/次のLvまで</span></div><div class="my_page_st_val">{pt["exp"]}<span>/{pt["n_exp"]}</span></div></div>
					<div class="my_page_st_3"><div class="my_page_st_title">配合</div><div class="my_page_st_val">{pt["hai"]}回</div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">攻撃力</div><div class="my_page_st_val">{pt["atk"]}</div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">守備力</div><div class="my_page_st_val">{pt["def"]}</div></div>
					<div class="my_page_st_4"><div class="my_page_st_title">素早さ</div><div class="my_page_st_val">{pt["agi"]}</div></div>
				</div>
			</div>
		"""	for i ,pt in enumerate(pt_v,1)
	])

	#my_pageメニュー
	html = f"""
		<div class="my_page_topmenu">
			[ <a href="{Conf["top_url"]}">TOPへ</a> ]
			[ <a href="./html/manual.html" target="_blank">ぷれいまにゅある</a> ]
			[ <a href="./haigou_list.py" target="_blank">配合表</a> ]
			[ <a href="./haigou_list2.py" target="_blank">配合表2</a> ]
			[ <a href="{Conf["homepage"]}">{Conf["home_title"]}</a> ]
		</div>
		<div class="my_page_box">
			<div class="my_page_title">{user["name"]}さんのパーティー</div>
			<div class="my_page_user_st1">所持金<br>{user_v["money"]}G</div>
			<div class="my_page_user_st1">所持鍵<br>{user_v["key"]}階</div>
			<div class="my_page_user_st1 {isekai}" >異世界探索度<br>{user.get("isekai_key",0)-1}/{user.get("isekai_limit",0)}/{Conf["isekai_max_limit"]}</div>
			<div class="my_page_user_st1">メダル<br>{user_v["medal"]}個</div>
			<div class="my_page_user_st1 my_page_zukan">
				<a href="./login.py?mode=zukan&name={in_name}&type=スライム系">[魔物図鑑]</a>
				<br>{user["getm"]}
			</div>
		</div>
		<form method="post" class="form">
			<div class="my_page_pt">
			{pt_txt}
			</div>
		</form>
		<br>
		<form action="{Conf["top_url"]}" method="post">
			<button>TOPへ</button>
		</form>
	"""

	sub_def.header()
	print(html)
	sub_def.footer()
