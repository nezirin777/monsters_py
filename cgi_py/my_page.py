def my_page (FORM) :
	import datetime

	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM.get("name")
	#in_pass = FORM.get("password")

	token = FORM.get("token")
	last_floor = int(FORM["c"].get("last_floor",1))
	last_room = FORM["c"].get("last_room","")
	last_floor_isekai = int(FORM["c"].get("last_floor_isekai",0))
	next_t = float(FORM["c"].get("next_t",0))

	u_list = sub_def.open_user_list()
	omiai_list = sub_def.open_omiai_list()
	user = sub_def.open_user(in_name)
	party = sub_def.open_party(in_name)
	vips = sub_def.open_vips(in_name)
	room_key = sub_def.open_room_key(in_name)
	waza   = sub_def.open_waza(in_name)

	#user_list更新
	bye = datetime.datetime.now() + datetime.timedelta(days=Conf["goodbye"])
	u_list[in_name] |= {
		"host":	sub_def.get_host(),
		"bye": bye.strftime("%Y-%m-%d"),
		"key" : user["key"],
		"money" : user["money"],
		"getm" : user["getm"],
		"m1_hai" : party[0]["hai"],
		"m1_lv" : party[0]["lv"],
		"m1_name" : party[0]["name"],
		"m2_hai" : party[1]["hai"] if(party[1:2]) else "",
		"m2_lv" : party[1]["lv"] if(party[1:2]) else "",
		"m2_name" : party[1]["name"] if(party[1:2]) else "",
		"m3_hai" : party[2]["hai"] if(party[2:3]) else "",
		"m3_lv" : party[2]["lv"] if(party[2:3]) else "",
		"m3_name" : party[2]["name"] if(party[2:3]) else "",
	}
	sub_def.save_user_list(u_list)

	isekai = "hidden"
	isekai_next = ""
	if (user.get("isekai_limit")) :
		isekai = ""
		isekai_next = min (user["isekai_key"] , user["isekai_limit"])

	park_get = "hidden"
	if (vips.get("パーク",0) != 0 and vips.get("パーク") != "") :
		park_get = ""

	user_v = sub_def.slim_number(user)
	pt_v = sub_def.slim_number(party)

	#PT部分
	c_txt = "".join([f"<option value={n}>{n}</option>" for n in range(1,len(party)+1)])
	pt_txt = "".join([
		f"""
			<div class="my_page_chara_{i}">
				<div class="my_page_st_1"><select name=c_no{i}><option value={i} hidden>{i}</option>{c_txt}</select></div>
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

	#鍵、技一覧
	txt1,txt2,txt3,txt4 = "","","",""
	for name ,r_key in room_key.items() :
		sel = "SELECTED" if (last_room == name) else ""
		if (r_key["get"]) :
			txt1 += f"""<div class="my_page_list_item">{name}の鍵</div>"""
			txt3 += f"""<option value={name}>{name}の部屋"""
			txt4 += f"""<option value={name} {sel}>{name}の部屋"""
		else :
			txt1 += f"""<div class="my_page_list_item">-</div>"""

	for name,wa in waza.items() :
		if not( wa["get"] ) : name = "-"
		txt2 += f"""<div class="my_page_list_item">{name}</div>"""

	#お見合い状況
	txt5 = ""
	if(omiai_list.get(in_name)):
		if(omiai_list[in_name]["baby"]) :
			txt5 = f"""<img src="{Conf["imgpath"]}/omiai_baby.png">"""
		else :
			for name,omiai in omiai_list.items() :
				if(in_name == omiai["request"]) :
					txt5 = f"""<img src="{Conf["imgpath"]}/omiai_irai.png">"""
					break

	yadoya ,kyoukai = 0 ,0
	hai,tenkan = "",""
	for i ,pt in enumerate(party,1) :
		if (pt["hp"] != 0) :
			yadoya += (pt["mhp"] - pt["hp"]) + (pt["mmp"] - pt["mp"])
		else :
			kyoukai += (pt["mhp"] + pt["mmp"]) * 2

		if (pt["lv"] >= Conf["haigoulevel"]) :
			hai +=	f"""<option value={i} >{i}:{pt["name"]} {pt["sex"]} LV-{pt["lv"]} 配合{pt["hai"]}回</option>"""

		if (pt["lv"] == 1) :
			tenkan += f"""<option value={i} >{pt["name"]} {pt["sex"]} {pt["hai"] * 100}G</option>"""

	yadoya_v = sub_def.slim_number(yadoya)
	kyoukai_v = sub_def.slim_number(kyoukai)

	event_txt = ""
	if(Conf["event_boost"]) :
		event_txt = "<div class=\"event_txt\">!!現在ブースト期間中!!</div>"

	#上部メニュー
	html = f"""
		<div class="my_page_topmenu">
			[ <a href="{Conf["top_url"]}">TOPへ</a> ]
			[ <a href="./html/manual.html" target="_blank">ぷれいまにゅある</a> ]
			[ <a href="./haigou_list.py" target="_blank">配合表</a> ]
			[ <a href="./haigou_list2.py" target="_blank">配合表2</a> ]
			[ <a href="{Conf["homepage"]}">{Conf["home_title"]}</a> ]
		</div>
		{event_txt}
		<div class="my_page_title">{user["name"]}さんのパーティー</div>
		<div class="my_page_box">
			<div class="my_page_user_st1">所持金<br>{user_v["money"]}G</div>
			<div class="my_page_user_st1">所持鍵<br>{user_v["key"]}階</div>
			<div class="my_page_user_st1 {isekai}" >異世界探索度<br>{user.get("isekai_key",0)-1}/{user.get("isekai_limit",0)}/{Conf["isekai_max_limit"]}</div>
			<div class="my_page_user_st1">メダル<br>{user_v["medal"]}個</div>
			<div class="my_page_user_st1 my_page_zukan">
				<a href="./login.py?mode=zukan&name={in_name}&type=スライム系">[魔物図鑑]</a>
				<br>{user["getm"]}
			</div>
		</div>
	"""

	#PT部分
	html += f"""
		<form method="post" class="form">
			<div class="my_page_pt">
			{pt_txt}
			</div>
			<div class="my_page_title">
				<button>並び替えOK</button>
				<input type="hidden" name="mode" value="change">
				<input type="hidden" name="token" value="{token}">
				No.1からNo.3迄のモンスターが戦闘を行います
			</div>
		</form>
	"""
	html += f"""
		<div class="my_page_keylist"><a href="javascript:bo('u2','u3')" class="menu">▼取得系統の鍵一覧▼</a>
			<div id="u2">{txt1}</div>
		</div>
		<div class="my_page_keylist"><a href="javascript:bo('u3','u2')" class="menu">▼取得特技一覧▼</a>
			<div id="u3">{txt2}</div>
		</div>
	"""

	#コメント+bbs+カウントダウン
	html += f"""
		<form method="post" class="form">
			<INPUT class="input" size="40" type="text" name="message" value="{user["mes"]}">
			<input type="hidden" name="mode" value="comment">
			<input type="hidden" name="token" value="{token}">
			<button>コメント変更</button>
		</form>
		<br>
		<object id="bbs" data="./bbs.py" type="text/html"></object>
		<div id="b_count_txt" hidden>{next_t}</div>
		<form id="b_count"><INPUT size="30" type="text"></INPUT></form>
	"""

	#戦闘+施設
	html += f"""
		<div class="my_page_menu_box">
			<div class="my_page_menu1">戦 闘</div>
			<div class="my_page_menu2">KEYやモンスターが入手出来ます。<br>KEYは一番深い階層を選択した時にしか出現しません。</div>
			<div class="my_page_menu3">【最 深 階】</div>
			<div class="my_page_menu4">
				<form method="post" class="form battle_go">
					<select name="in_room">
						<option value="通常">通常の部屋
						{txt3}
					</select>
					の地下
					<input type="number" min="1" max="{user["key"]}"  name="in_floor" value="{user["key"]}" size="7"></input>
					Fに
					<button disabled>戦闘に行く！</button>
					<input type="hidden" name="mode" value="battle_type">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="my_page_menu3">【前対戦階】</div>
			<div class="my_page_menu4">
				<form method="post" class="form battle_go">
					<select name="in_room">
						<option value="通常" room>通常の部屋
						{txt4}
					</select>
					の地下
					<input type="number" min="1" max="{user["key"]}" name="in_floor" value="{last_floor}" size="7"></input>
					Fに
					<button disabled>戦闘に行く！</button>
					<input type="hidden" name="mode" value="battle_type">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="my_page_menu3 {isekai}">異世界:最深階</div>
			<div class="my_page_menu4 {isekai}">
				<form method="post" class="form battle_go">
					異世界の地下
					<input type="number" min="1" max="{isekai_next}" name="in_isekai" value="{isekai_next}" size="7"></input>
					Fに
					<button disabled>探索に行く！</button>
					<input type="hidden" name="mode" value="battle_type2">
					<input type="hidden" name="max_floor" value="{user["key"]}" size="7"></input>
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>
			<div class="my_page_menu3 {isekai}">異世界:前探索階</div>
			<div class="my_page_menu4 {isekai}">
				<form method="post" class="form battle_go">
					異世界の地下
					<input type="number" min="1" max="{isekai_next}" name="in_isekai" value="{last_floor_isekai}" size="7"></input>
					Fに
					<button disabled>探索に行く！</button>
					<input type="hidden" name="mode" value="battle_type2">
					<input type="hidden" name="max_floor" value="{user["key"]}" size="7"></input>
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="my_page_menu1">施設色々</div>
			<div class="my_page_menu2"><span id="link_msg">説明がここに。</span></div>
			<div class="my_page_menu3">【お店へ】<br>{txt5}</div>
			<div class="my_page_menu4">
				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='モンスターに本を読ませて性格を変更させる事が出来ます。'">
						<button>本屋に入室</button>
						<input type="hidden" name ="mode" value="books">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='ｺﾞｰﾙﾄﾞを支払ってHP･MPを完全に回復させます。'">
						<button>宿 屋({yadoya_v}G)</button>
						<input type="hidden" name ="mode" value="yadoya">
						<input type="hidden" name="yadodai" value="{yadoya}">
						<input type="hidden" name="money" value="{user["money"]}">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='ｺﾞｰﾙﾄﾞを支払って死亡したモンスターを復活させます。'">
						<button>教 会({kyoukai_v}G)</button>
						<input type="hidden" name ="mode" value="kyoukai">
						<input type="hidden" name="kyoukaidai" value="{kyoukai}">
						<input type="hidden" name="money" value="{user["money"]}">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='メダルやGを使いモンスター等を交換できます。'">
						<button>交換所</button>
						<input type="hidden" name ="mode" value="medal_shop">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='モンスターを預けることが出来ます'">
						<button  {park_get}>モンスターパーク</button>
						<input type="hidden" name="mode" value="park">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='モンスターを購入できます'">
						<button>VIP交換所1</button>
						<input type="hidden" name="mode" value="v_shop">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='アイテム等を購入できます'">
						<button>VIP交換所2</button>
						<input type="hidden" name="mode" value="v_shop2">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='他のユーザーとお見合いができます'">
						<button>お見合い所</button>
						<input type="hidden" name="mode" value="omiai_room">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>

				<form method="post" class="form">
					<span onmouseover="link_msg.innerHTML='ユーザー名を変更できます'">
						<button>ユーザー名変更所</button>
						<input type="hidden" name="mode" value="name_change">
						<input type="hidden" name="token" value="{token}">
					</span>
				</form>
			</div>

			<div class="my_page_menu1">配　合</div>
			<div class="my_page_menu2">配合料金は配合させる2匹のモンスターの<br>【（レベル＋レベル）×10G】です。</div>
			<div class="my_page_menu3">【配合可能のみ表示】</div>
			<div class="my_page_menu4">
				<form name=form1 method="post" class="form">
					<select name=haigou1 onClick="change_img1()">
						<option value=0 hidden>選 択-ベース-</option>
						{hai}
					</select>
					<select name=haigou2 onClick="change_img2()">
						<option value=0 hidden>選 択-材 料- </option>
						{hai}
					</select>
					<br>
					<IMG name="img1" SRC="{Conf["imgpath"]}/0.gif">
					<IMG name="img2" SRC="{Conf["imgpath"]}/0.gif">
					<br>
					<button>配合する</button>
					<input type="hidden" name="mode" value="haigou_check">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="my_page_menu1">陰陽変換所</div>
			<div class="my_page_menu2">変換料金はモンスターの【配合回数×100G】です。</div>
			<div class="my_page_menu3">【変換可能のみ表示】</div>
			<div class="my_page_menu4">
				<form method="post" class="form">
					<select name=no>
						<option value="0" hidden>選 択</option>
						{tenkan}
					</select>
					<button>陰陽変換する</button><br>
					<input type="hidden" name="mode" value="seitenkan">
					<input type="hidden" name="token" value="{token}">
				</form>
			</div>

			<div class="my_page_menu1">設定変更</div>
			<div class="my_page_menu2">大きすぎる数値表記を調整します。</div>
			<div class="my_page_menu3"></div>
			<div class="my_page_menu4">
				<form method="post" class="form">
					<select name=no>
						<option value=0>選 択</option>
						<option value=0>調整なし</option>
						<option value=1>区切り文字だけ</option>
						<option value=2>k,M,G単位表記</option>
						<option value=3>万,億,兆単位表記</option>
					</select>
					<input type="submit" value="設定する"><br>
					<input type="hidden" name="mode" value="number_unit">
					<input type="hidden" name="token" value="{token}">
				</FORM>
			</div>

		</div>
	"""

	sub_def.header()
	sub_def.jscript(party,"",1)
	print(html)
	sub_def.my_page_button(FORM["token"])
