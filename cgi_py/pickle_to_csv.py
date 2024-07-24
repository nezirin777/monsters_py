def pickle_to_csv(target_name) :

	import sub_def
	import conf

	Conf = conf.Conf

	#-------------------------------------------------------------
	def user_dat(in_name) :

		sub_def.save_csv(sub_def.open_room_key(in_name),"room_key.csv" ,in_name)

		ppt = sub_def.open_park(in_name)
		if not(len(ppt)) :
			ppt = [{
			"no" :"-",
			"name" :"-",
			"lv" : "-",
			"mlv" :"-",
			"hai" :"-",
			"hp" : "-",
			"mhp" : "-",
			"mp" : "-",
			"mmp" : "-",
			"atk" : "-",
			"def" : "-",
			"agi" : "-",
			"exp" : "-",
			"n_exp" : "-",
			"sei" : "-",
			"sex" : "-"
		}]

		sub_def.save_csv(ppt,"park.csv",in_name)

		sub_def.save_csv(sub_def.open_party(in_name),"party.csv",in_name)

		sub_def.save_csv(sub_def.open_user(in_name),"user.csv",in_name)

		sub_def.save_csv(sub_def.open_vips(in_name),"vips.csv",in_name)

		sub_def.save_csv(sub_def.open_waza(in_name),"waza.csv",in_name)

		sub_def.save_csv(sub_def.open_zukan(in_name),"zukan.csv",in_name)

	#--------------------------------------------------------

	if(target_name == "user_list") :
		sub_def.save_csv(sub_def.open_user_list(),Conf["datadir"] + "/user_list.csv","","user")

	elif(target_name == "omiai_list") :
		sub_def.save_csv(sub_def.open_omiai_list(),Conf["datadir"] + "/omiai_list.csv","","user")

	elif(target_name == "全員") :
		u_list = sub_def.open_user_list()
		with open(Conf["datadir"]+"/pickle_to_csv_log.txt", mode='a',encoding='utf-8') as f:
			for name,u in u_list.items() :
				f.write(f"{name} 変換開始\n")
				user_dat(name)
				f.write(f"{name} 変換完了\n")
	else :
		user_dat(target_name)
