#!D:\Python\Python312\python.exe

import sys

import sub_def
import conf
Conf = conf.Conf
sys.stdout.reconfigure(encoding='utf-8')

M_types = ["スライム系","ドラゴン系","けもの系","とり系","しょくぶつ系","むし系","あくま系","ゾンビ系","ぶっしつ系","みず系","？？？系"]

#表示させないモンスター
M_del_list = ["アイぼう","かくれんぼう","じげんりゅう","ラーミア","ゾーマズデビル","マスタードラゴン"]

M_list = sub_def.open_monster_dat()

link = ""
for i , m_type in enumerate(M_types) :
	link += f"""[<a href="#{m_type}">{m_type}</a>]"""
	if (i==5) :
		link += "<br>"

html = ""
for m_type in M_types :
	html += f"""
		<div class="haigou_list_link" id={m_type}>{link}</div>
		<div class="haigou_box">
		<div class="menu_title_1">NO</div>
		<div class="menu_title_2">{m_type}</div>
		<div class="menu_title_3">ベース</div>
		<div class="menu_title_4">材　料</div>
		<div class="menu_title_5">出現階数</div>
		<div class="menu_title_1">戦闘入手</div>
		</div>
	"""
	m_list = {name:dat for name,dat in M_list.items() if(dat["m_type"]==m_type and name not in M_del_list) }

	for name,target in m_list.items() :
		(text_A ,text_B) = ("","")
		for x in range(1,4) :
			text_A += f"""<div class="haigou_menu_3B">{target[f"血統{x}"]}</div>""" if target[f"血統{x}"] else ""
			text_B += f"""<div class="haigou_menu_4B">{target[f"相手{x}"]}</div>""" if target[f"相手{x}"] else ""
		text_C = "OK" if target["get"] else "NO"

		html += f"""
			<div class="haigou_box">
				<div class="haigou_menu_1">{target["no"]}</div>
				<div class="haigou_menu_2">{name}</div>
				<div class="haigou_menu_3">{text_A}</div>
				<div class="haigou_menu_4">{text_B}</div>
				<div class="haigou_menu_5">{target["階層A"]}階～{target["階層B"]}階</div>
				<div class="haigou_menu_1">{text_C}</div>
			</div>
		"""
		del M_list[name]

html2 = f"""
	<html>
	<head>
		<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
		<title>MONSTER'S 配合表</title>
		<LINK REL="stylesheet" HREF="./css_js/html_style.css" TYPE="text/css">
	</head>

	<BODY>
		<div class="haigou_title">
		<form action="{Conf["top_url"]}" method="post">
			<input type="hidden" name="mode" value="">
			<button>TOPへ</button>
		</form>
		</div>

		<div class="haigou_title">
			MONSTER'S 改 {Conf["ver"]}
			<br>
			配合表・出現階数
		</div>
		<div class="haigou_menu">{html}</div>

		<div class="haigou_title">
		<form action="{Conf["top_url"]}" method="post">
			<input type="hidden" name="mode" value="">
			<button>TOPへ</button>
		</form>
		</div>
"""

print("Content-Type: text/html; charset=utf-8\r\n\r\n")
print(html2)
sub_def.footer()
