
def csv_to_pickle(target_name) :
	import pickle
	import os
	import glob
	import pandas as pd

	import sub_def
	import conf

	Conf = conf.Conf

	def remove_glob(pathname, recursive=True):
		for p in glob.glob(pathname, recursive=recursive):
			if os.path.isfile(p):
				os.remove(p)

	def pickle_dump(obj, path):
		with open(path, mode='wb') as f:
			pickle.dump(obj,f)

	def open_csv_list(file) :
		return pd.read_csv(file, encoding="utf-8_sig",index_col="user").fillna("").to_dict(orient='index')

	def user_dat(in_name) :
		file = Conf["datadir"] + "/" + in_name +"/pickle"

		data  = sub_def.open_csv("waza.csv",in_name,0,1)
		data = {name:v for name,v in data.items() if(name not in ("" ,"-","0"))}
		pickle_dump(data,file + "/waza.pickle")

		data = sub_def.open_csv("zukan.csv",in_name,0,1)
		data = {name:v for name,v in data.items() if(name not in ("" ,"-","0"))}
		pickle_dump(data,file + "/zukan.pickle")

		data = sub_def.open_csv("room_key.csv",in_name,0,1)
		data = {name:v for name,v in data.items() if(name not in ("" ,"-","0"))}
		pickle_dump(data,file + "/room_key.pickle")

		data = sub_def.open_csv("park.csv",in_name)
		data = [v for v in data if(v["name"] not in ("" ,"-","0"))]
		pickle_dump(data,file + "/park.pickle")

		data = sub_def.open_csv("party.csv",in_name)
		data = [v for v in data if(v["name"] not in ("" ,"-","0"))]
		pickle_dump(data,file + "/party.pickle")

		data = sub_def.open_csv("user.csv",in_name,1)
		pickle_dump(data,file + "/user.pickle")

		data = sub_def.open_csv("vips.csv" ,in_name,1)
		pickle_dump(data,file + "/vips.pickle")


		remove_glob(file + "/*.csv")

	f = Conf["datadir"]
	if(target_name == "user_list") :
		pickle_dump(open_csv_list(f + "/user_list.csv") ,f + "/user_list.pickle")
		os.remove(f + "/user_list.csv")

	elif(target_name == "omiai_list") :
		pickle_dump(open_csv_list(f + "/omiai_list.csv") ,f + "/omiai_list.pickle")
		os.remove(f + "/omiai_list.csv")

	elif(target_name == "全員") :
		u_list = sub_def.open_user_list()
		for name,u in u_list.items() :
			with open(Conf["datadir"]+"/csv_to_pickle_log.txt", mode='a',encoding='utf-8') as f:
				f.write(f"{name} 変換開始\n")
				user_dat(name)
				f.write(f"{name} 変換完了\n")
	else :
		user_dat(target_name)
