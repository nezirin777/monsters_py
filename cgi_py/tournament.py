class tournaments() :
	def __init__(self):
		import sub_def
		# メンバ
		u_list = sub_def.open_user_list()
		self.U_count = min(len(u_list),64)
		self.Fighter = [{"name":name,"key":u["key"]} for name,u in list(u_list.items())[:self.U_count]]
		self.new_F = []
		self.present = []

		self.b_data = {
			"第一回戦" : { "menber" : 32 , "hosei":16 , "medal":1},
			"第二回戦" : { "menber" : 16, "hosei":8 , "medal":2},
			"第三回戦" : { "menber" : 8 , "hosei":4 , "medal":3},
			"第四回戦" : { "menber" : 4 , "hosei":3 , "medal":5},
			"準決勝" : { "menber" : 2 , "hosei":2 , "medal":7},
			"決勝戦" : { "menber" : 1 , "hosei":1 , "medal":10}
		}

	def medal_get(self) :
		import sub_def
		for pre in self.present :
			user = sub_def.open_user(pre["target"])
			user["medal"] += pre["medal"]
			sub_def.save_user(user,pre["target"])

	def medal_fight(self,v) :
		import random

		winner,loser = "",""
		txt,mes2 = "",""

		if (len(self.Fighter) <= 1) :
			winner = self.Fighter[0]
			self.Fighter.remove(self.Fighter[0])
			txt = f"""相手不在につき {winner["name"]} さんの勝利です\n"""
		else :
			sensyu = random.sample(self.Fighter,2)
			sensyu.sort(key=lambda x: x['key'],reverse=True)

			(hp1,atk1) = (v["hosei"],v["hosei"]+random.randint(1,10))
			(hp2,atk2) = (1,1+random.randint(1,10))

			hp2 -= max(0,int(atk1 - atk2))
			hp1 -= max(0,int(atk2 - atk1))

			(winner,loser) = (sensyu[0],sensyu[1]) if (hp1 >= hp2) else (sensyu[1],sensyu[0])

			txt = f"""{sensyu[0]["name"]} vs {sensyu[1]["name"]} は {winner["name"]} さんが勝利しました\n"""
			mes2 = f"""{loser["name"]}さんにはメダル{v["medal"]}枚が与えられました\n"""

			self.present.append({"medal":v["medal"],"target":loser["name"]})

			self.Fighter.remove(sensyu[0])
			self.Fighter.remove(sensyu[1])

		self.new_F.append(winner)

		return  f"""<div class="medal_battle_result">{txt}</div>{mes2}\n"""

	def t_battle(self) :
		import random
		import sub_def
		import conf

		Conf = conf.Conf

		#結果表示月日用
		time = sub_def.open_tournament_time()
		sub_def.timesyori()

		html = f"""<div class="medal_battle_title">{time}のメダル獲得杯の結果！</div>\n"""

		if (self.U_count <= 1) :
			html += f"""<div>規定人数未満につき中止になりました。</div>\n"""
		else :
			for key, v in self.b_data.items() :
				if (v["menber"] < len(self.Fighter)) :
					self.new_F = []
					mes = ""
					i = 1
					while self.Fighter :
						if (key != "決勝戦") :
							mes += f"""<div class="medal_battle_sub">第{i}試合</div>\n"""
						mes += self.medal_fight(v)
						i += 1

					self.Fighter = self.new_F
					html += f"""<div><div class="medal_battle_data">{key}</div>\n{mes}</div>\n"""

			#優勝者用に追加で呼び出し
			val = random.randint(13,15)
			self.present.append({"medal":val,"target":self.Fighter[0]["name"]})

			html += f"""<div class="red">優勝の{self.Fighter[0]["name"]}さんにはメダル{val}枚が与えられました</div>\n"""

		with open(Conf["datadir"]+"/tournament.log", mode='w',encoding='utf-8') as f:
			f.write(html)

		self.medal_get()
		sub_def.backup()

def tournament() :
	x = tournaments()
	x.t_battle()
