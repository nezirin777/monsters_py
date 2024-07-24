#!D:\Python\Python312\python.exe

import cgi
import datetime
import secrets
import os
import re #正規表現

import cgi_py
import sub_def
import conf
Conf = conf.Conf

class Start_top() :
	def __init__(self) :
		self.u_list = sub_def.open_user_list()
		self.u_count = len(self.u_list)

		cookie = sub_def.get_cookie()
		in_name = cookie.get("in_name","")
		in_pass = cookie.get("in_pass","")

		self.login = f"""
			<div class="login">
				<form action="{Conf["cgi_url"]}" method="post" name="login">
					<span>ユーザー名</span>
					<input type="text" size="14" name="name" value="{in_name}"><br>
					<span>パスワード</span>
					<input type="password" size="14" name="password" value="{in_pass}"><br>
					<input type="hidden" name="mode" value="my_page">
					<input type="hidden" name="ref" value="top">
					<input type="hidden" name="token" value="{FORM["token"]}">
					<button>ログイン</button>
				</form>
			</div>
		"""

		if (os.path.exists("mente.mente")) :
			self.login = ("<div class=\"mente\">現在メンテ中です。<br>終了までお待ちください。</div>")

		self.hyouzi = Conf["maxshow"] +1

	def main_html(self,txt) :
		reg_txt = f"""[ <a href="./{Conf["reg_url"]}">新規登録</a> ]"""

		if(self.u_count >= Conf["sankaMAX"]) :
			reg_txt = """[<del title="参加者上限につき登録停止中">新規登録</del>]"""

		event_txt = ""
		if(Conf["event_boost"]) :
			event_txt = "<div class=\"event_txt\">!!現在ブースト期間中!!</div>"

		#上部
		html = f"""
			<div class="toptitle">
				MONSTER'S 改<span>{Conf["ver"]}</span>
				<div class="t_menu">
					{reg_txt}
					[ <a href="./html/manual.html" target="_blank">ぷれいまにゅある</a> ]
					[ <a href="./haigou_list.py" target="_blank">配合表</a> ]
					[ <a href="./haigou_list2.py" target="_blank">配合表2</a> ]
					[ <a href="./{Conf["kanri_url"]}" target="_blank">管理モード</a> ]
					[ <a href="{Conf["homepage"]}">{Conf["home_title"]}</a> ]
				</div>
			</div>

			<div class="t_txt">
				初めての方は上の<span>新規登録</span>から参加してください。<br>
				現在の参加数は<span>{self.u_count}/{Conf["sankaMAX"]}</span>人です!<br>
				戦闘間隔は<span>{Conf["nextplay"]}</span>秒、配合可能レベルは<span>{Conf["haigoulevel"]}</span>の設定です。<br>
				次のメダル獲得杯は<span>{t_time}</span>で出場権利は<span>64位</span>までの人です。
			</div>

			<div class="t_txt">
				何か問題等あればゲーム内一言掲示板か<br>
				[ <a href="https://discord.gg/yNg3ntSDgf">Discord</a> ] の#cgigame チャンネル、もしくは"ねじりん"まで連絡くださいませ。<br>
			</div>

			{event_txt}

			{txt}

			<div id="medaltime">次のメダル獲得杯まであと{t_count}日</div>

			<div>
				<form action="{Conf["cgi_url"]}" METHOD="GET">
					<button>前大会の結果</button>
					<input type="hidden" NAME="mode" VALUE="tournament_result">
				</form>
			</div>

			<div><object id="news" type="text/html" data="./html/news.html">エラー</object></div>
		"""
		return html

	def rank_html(self,rank,ptxt,a,b) :
		html = f"""
			<div class="rank_t">{rank}</div>
			{ptxt}
			<div class="rank_m">
				<div class=r_1>Rank</div>
				<div class=r_2>User</div>
				<div class=r_3>手持ち</div>
			</div>
		"""

		def user_mlist(u) :
			txt = ""
			for i in range (1,4) :
				if (u[f"m{i}_name"] != "") :
					txt += f"""
						<div class="r_m">
							<img src="{Conf["imgpath"]}/{u[f"m{i}_name"]}.gif"/><br>
							{u[f"m{i}_name"]}<br>
							Lv<span>{u[f"m{i}_lv"]}</span><br>
							配合<span>{u[f"m{i}_hai"]}</span>回
						</div>
					"""
			return txt

		for name,u in list(self.u_list.items())[a:b] :
			txt = user_mlist(u)
			delday = sub_def.getdelday(u["bye"])#削除日時計算
			html += f"""
				<div class="rank">
					<div class="r_1 r_u1">{u["rank"]}</div>
					<div class="r_ubox">
						<div class="r_2 r_u2">
							<div>
								ユーザー名:<A HREF="{Conf["cgi_url"]}?mode=my_page2&name={name}" target="_blank">{name}</A><br>
								最深部:地下<span>{u["key"]}</span>階<br>
								所持金:{u["money"]}G<br>
								図鑑:{u.get("getm",0)}<br>
								データ保存期間:あと<span>{delday}</span>日
							</div>
						</div>
						<div class="r_3 r_u3">
							{txt}
						</div>
						<div class="r_u4">コメント</div>
						<div class="r_u5">{u["mes"]}</div>
					</div>
				</div>
			"""

		return html

	def top_1(self) :
		rank = f"RANKING [1位～{Conf['maxshow']}位]"
		ptxt = ""
		if (self.u_count > Conf["maxshow"]) :
			ptxt = f"""
				<div>
					<form method="post">
						<button>{self.hyouzi}位以降</button>
						<input type="hidden" NAME="menu" VALUE=1>
					</form>
				</div>
			"""
		b = min (self.u_count,Conf["maxshow"])

		html = self.main_html(self.login)
		html += self.rank_html(rank,ptxt,0,b)
		html += "<br>" + ptxt

		return html

	def top_2(self) :
		rank = f"RANKING [{self.hyouzi}位～{self.u_count}位]"
		ptxt = f"""
			<div>
				<form method="post">
					<button>1位～{Conf['maxshow']}位</button>
					<input type="hidden" NAME="menu" VALUE=0>
				</form>
			</div>
		"""
		html = self.main_html(self.login)
		html += self.rank_html(rank,ptxt,Conf["maxshow"],self.u_count)
		html += "<br>" + ptxt

		return html


if __name__ == "__main__" :
	for ip in conf.noip :
		if (re.match(ip, os.environ['REMOTE_ADDR'])):
			sub_def.error("あなたのIPは禁止されています",99)

	#メダル杯開催確認
	t_time = sub_def.open_tournament_time()

	t_count = (datetime.datetime.strptime(t_time ,"%Y年%m月%d日") - datetime.datetime.now()).days
	if (int(t_count) < 0) :
		cgi_py.tournament.tournament()


	#フォームを辞書化
	form = cgi.FieldStorage()
	FORM = { key:form.getvalue(key) for key in form.keys() }

	token = secrets.token_hex(16)
	sub_def.set_session({"token":token})
	FORM["token"] = token

	x = Start_top()

	if (x.u_count) :
		if (int(FORM.get("menu",0)) == 0) :
			html = x.top_1()
		else :
			html = x.top_2()
	else :
		html = x.main_html("")
		html += """<div class="rank_t">現在登録ユーザーはいません。</div>"""

	sub_def.delete_check()

	sub_def.header()
	print(html)
	sub_def.footer()
