def tournament_result() :
	import os
	import sub_def
	import conf

	Conf = conf.Conf

	log = Conf["datadir"]+"/tournament.log"

	if not (os.path.exists(log)) :
		with open(log, mode='w',encoding="utf-8") as f:
			f.write("""<div class="medal_battle_title">まだ未開催です</div>""")

	with open(log, mode='r',encoding='utf-8') as f :
		html = f.read()

	sub_def.header()
	print(html)
	sub_def.footer()
