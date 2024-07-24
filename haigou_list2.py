#!D:\Python\Python312\python.exe

import sys

import sub_def
import conf
Conf = conf.Conf
sys.stdout.reconfigure(encoding='utf-8')


M_list = sub_def.open_monster_dat()

html = f"""
			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/ワンダーエッグ.gif"><br>ワンダーエッグ</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>？？？</span></div>
					<div class="table_m_cell_2"><span>？？？</span></div>
					<div class="table_m_cell_3">HP:10 MP:3 ATK:5 DEF:8 AGI:4 EXP:10 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>某精霊×某精霊(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:40 MP:60 ATK:40 DEF:40 AGI:80</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>相棒×たまご(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:50 MP:70 ATK:50 DEF:50 AGI:50</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>真りゅうおう×隠(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:80 MP:60 ATK:100 DEF:80 AGI:90</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>最強の鳥さん×↑(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:100 MP:100 ATK:100 DEF:100 AGI:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>アスラン×これでもラスボスでした。(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:50 MP:40 ATK:60 DEF:40 AGI:30</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><br><IMG src="">？？？</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">出現しない</div>
					<div class="table_m_cell_2"><span>天界獣×ギスヴァーグ(逆でもおｋ)</span></div>
					<div class="table_m_cell_3">HP:150 MP:150 ATK:150 DEF:150 AGI:150</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/ひのせいれい.gif"><IMG src="./img/かぜのせいれい.gif"><br>せいれい<br><IMG src="./img/ちのせいれい.gif"><IMG src="./img/みずのせいれい.gif"></div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">300階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">交換所のみ</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/ひかりのせいれい.gif"><br>ひかりのせいれい</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">300階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">ちのせいれい×みずのせいれい(逆でもok)</div>
					<div class="table_m_cell_3">HP:30 MP:30 ATK:30 DEF:30 AGI:30 EXP:400 MONEY:200</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/やみのせいれい.gif"><br>やみのせいれい</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">300階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">ひのせいれい×かぜのせいれい(逆でもok)</div>
					<div class="table_m_cell_3">HP:30 MP:30 ATK:30 DEF:30 AGI:30 EXP:400 MONEY:200</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/イイロ.gif"><br>イイロ</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">400階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">スライム系×ちのせいれい</div>
					<div class="table_m_cell_3">HP:5 MP:5 ATK:7 DEF:6 AGI:5 EXP:100 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/ピモ.gif"><br>ピモ</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">400階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">スライム系×ひのせいれい</div>
					<div class="table_m_cell_3">HP:6 MP:6 ATK:5 DEF:7 AGI:5 EXP:100 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/アルー.gif"><br>アルー</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">400階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">スライム系×みずのせいれい</div>
					<div class="table_m_cell_3">HP:7 MP:4 ATK:8 DEF:3 AGI:5 EXP:100 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/ドリーン.gif"><br>ドリーン</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">400階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">スライム系×かぜのせいれい</div>
					<div class="table_m_cell_3">HP:8 MP:4 ATK:4 DEF:5 AGI:5 EXP:100 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>

			<div class="table_m_box">
				<div class="table_m_cell_0"><IMG src="./img/パーラル.gif"><br>パーラル</div>
				<div class="table_m_box1">
					<div class="table_m_cell_1 ponpon">400階～</div>
					<div class="table_m_cell_1">通常部屋</div>
					<div class="table_m_cell_2">スライム系×やみのせいれい</div>
					<div class="table_m_cell_3">HP:9 MP:5 ATK:10 DEF:7 AGI:5 EXP:100 MONEY:100</div>
					<div class="table_m_cell_3 upday">2000/01/01</div>
				</div>
			</div>
	"""

m_list = {name:dat for name,dat in M_list.items() if(dat["room"]=="特殊") }

for name,target in m_list.items() :
	dis = "style=display:none" if target["説明B"]=="" else ""

	html += f"""
		<div class="table_m_box" id={target["m_type"]}>
			<div class="table_m_cell_0"><IMG src="./img/{name}.gif"><div>{name}</div></div>
			<div class="table_m_box1">
				<div class="table_m_cell_1 ponpon">{target["階層A"]}階～{target["階層B"]}階</div>
				<div class="table_m_cell_1">異世界</div>
				<div class="table_m_cell_2">{target["説明A"]}</div>
				<div class="table_m_cell_2" {dis}>{target["説明B"]}</div>
				<div class="table_m_cell_3">HP:{target["hp"]} MP:{target["mp"]} ATK:{target["atk"]} DEF:{target["def"]} AGI:{target["agi"]} EXP:{target["exp"]} MONEY:{target["money"]}</div>
				<div class="table_m_cell_3 upday">{target["date"]}</div>
				<div class="table_m_cell_3 pop" style=display:none>{target["階層A"]}</div>
				<div class="table_m_cell_3 no" style=display:none>{target["no"]}</div>
			</div>
		</div>
	"""

html2 = f"""
	<html>
	<head>
		<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=utf-8">
		<title>MONSTER'S 配合表2</title>
		<LINK REL="stylesheet" HREF="./css_js/html_style.css" TYPE="text/css">
		<script src="./css_js/jquery.min.js"></script>
		<script src="./css_js/table_sort.js"></script>
	</head>

	<BODY>
		<div class="haigou_title" id="top">
			MONSTER'S 改 {Conf["ver"]}
			<br>
			特殊モンスター配合表・出現階層
		</div>

		<div id="haigou_rightmenu">
			[<a href="#top">一番上へ</a>]
			<br>[<a href="#らき☆すた">らき☆すた</a>]
			<br>[<a href="#まどマギ">まどマギ</a>]
			<br>[<a href="#シンフォギア">シンフォギア</a>]
			<br>[<a href="#東方">東方</a>]
			<br>[<a href="#アイマス">アイマス</a>]
			<br>[<a href="#ボカロ">ボカロ</a>]
			<br>[<a href="#シュタゲ">シュタゲ</a>]
			<br>[<a href="#とある">とある</a>]
			<br>[<a href="#ミルキィ">ミルキィ</a>]
			<br>[<a href="#ボイロ">ボイロ</a>]
			<br>[<a href="#原神">原神</a>]
			<br>[<a href="#このすば">このすば</a>]
			<br>[<a href="#ドラクエ">ドラクエ</a>]
			<br>
			<br>
			<form action="{Conf["top_url"]}" method="post">
				<input type="hidden" name="mode" value="">
				<button>TOPへ</button>
			</form>
		</div>

		<br>
		<div class="haigou_txt">
			配合のみ、戦闘のみ、交換のみ等入手条件が限られるものもあります。<br>
			赤字はお見合い限定になります。<br>

			<br>
			モンスター名が伏せてある所はDiscord等でヒントを言うのはOKですが、<br>
			直接○○だった！っていうのは罰則があるわけでもないけど<font color=red>禁止にします。</font><br>
			試行錯誤してもらいたいだけなんで、自分勝手ですがよろしくお願いします。<br>

			<br>
			<button class="sortBtnC" rel="no">No順(デフォ)</button>

			<br>
			<button class="sortBtnA" rel="upday">実装が新しい順にソート</button>
			<button class="sortBtnB" rel="upday">実装が古い順にソート</button>

			<br>
			<button class="sortBtnC" rel="pop">出現階層が浅い順にソート</button>
			<button class="sortBtnD" rel="pop">出現階層が深い順にソート</button>

			<br>
			<ui>
				<li>2020/01/23 DQM2モンスター実装</li>
				<li>2021/06/03 DQMキャラバンハートモンスター実装</li>
			</ui>
		</div>

		<div class="table_m">
			<div class="table_m_box">
				<div class="table_m_title">モンスター名</div>
				<div class="table_m_box1">
					<div class="table_m_title ponpon">出現階層</div>
					<div class="table_m_title">出現系統</div>
					<div class="table_m_title">ベース</div>
					<div class="table_m_title">材料</div>
					<div class="table_m_title3">基礎ステータス 例ダークドレアム HP:45 MP:40 ATK:60 DEF:40 AGI:25 EXP:1500 MONEY:1500</div>
					<div class="table_m_title3 upday">実装日</div>
				</div>
			</div>
		</div>

		<div class="table_m" id="tuika_mob_list">
			<div class="list">
				{html}
			</div>
		</div>

"""

print("Content-Type: text/html; charset=utf-8\r\n\r\n")
print(html2)
sub_def.footer()
