def zukan (FORM) :
	import secrets
	import sub_def
	import conf

	Conf = conf.Conf

	in_name = FORM["name"]
	m_type = FORM["type"]

	zukan = sub_def.open_zukan(in_name)
	user  = sub_def.open_user(in_name)
	M_list = sub_def.open_monster_dat()

	FORM["s"] = sub_def.get_session()
	ccc = sub_def.get_cookie()

	ref = ccc.get("in_name","") == in_name

	def mon_list1(m_type) :
		zukan_list = {name:zu for name,zu in zukan.items() if (m_type == zu["m_type"])}
		html2 = ""
		for name,li in zukan_list.items() :
			m_type = li["m_type"]
			title = ""
			if not(li["get"]) :
				m_type = ""
				name = "？？？"
			else :
				mon = M_list[name]
				for n in range(1,3) :
					if(mon[f"血統{n}"] and ref) :
						title += mon[f"血統{n}"] + "×" + mon[f"相手{n}"] +"&#13;&#10;"

			html2 += f"""
				<div class="zukan">
					<div class="zukan_no">{li["no"]}</div>
					<div class="zukan_img {m_type}" data-html="true" title="{title}" tabindex="0"><img src="{Conf["imgpath"]}/{name}.gif"></div>
					<div class="zukan_name">{name}</div>
				</div>
			"""
		return html2

	url = f"""href={Conf["cgi_url"]}?mode=zukan&name={in_name}&type="""
	html = f"""
		<div id="zukan_title">
			<div>
				<span class="fsize">{in_name}の魔物図鑑</span><br>入手したモンスターは{user["getm"]}
			</div>
		</div>

		<div id="zukan_link">
			[<a {url}スライム系>スライム系</a>]
			[<a {url}ドラゴン系>ドラゴン系</a>]
			[<a {url}けもの系>けもの系</a>]
			[<a {url}とり系>とり系</a>]
			[<a {url}しょくぶつ系>しょくぶつ系</a>]
			[<a {url}むし系>むし系</a>]
			[<a {url}あくま系>あくま系</a>]
			[<a {url}ゾンビ系>ゾンビ系</a>]
			[<a {url}ぶっしつ系>ぶっしつ系</a>]
			[<a {url}みず系>みず系</a>]
			[<a {url}？？？系>？？？系</a>]
			<br>
			[<a {url}せいれい系>せいれい系</a>]
			[<a {url}らき☆すた>らき☆すた</a>]
			[<a {url}まどマギ>まどマギ</a>]
			[<a {url}シンフォギア>シンフォギア</a>]
			[<a {url}東方>東方</a>]
			[<a {url}アイマス>アイマス</a>]
			[<a {url}ボカロ>ボカロ</a>]
			[<a {url}シュタゲ>シュタゲ</a>]
			[<a {url}とある>とある</a>]
			<br>
			[<a {url}ミルキィ>ミルキィ</a>]
			[<a {url}ボイロ>ボイロ</a>]
			[<a {url}原神>原神</a>]
			[<a {url}このすば>このすば</a>]
			[<a {url}ドラクエ>ドラクエ</a>]
		</div>

		<div id="zukan_type">{m_type}</div>
	"""

	sub_def.header()
	html2 = mon_list1(m_type)
	print(f"""{html}<div id="zukan_box">{html2}</div>""")

	if (ref) :
		token = FORM["s"]["token"]
		sub_def.my_page_button(token)
	else :
		html = f"""
			<form METHOD="GET">
				<input type="hidden" name="mode" value="my_page2">
				<input type="hidden" name="name" value="{in_name}">
				<button>ユーザーページへ</button>
			</form>
			<form action="{Conf["top_url"]}" method="post">
				<button>TOPへ</button>
			</form>
		"""
		print(html)
		sub_def.footer()
