
def cgi_python() :
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

	def open_dat(file):
		return pd.read_csv(file, encoding="utf-8_sig",index_col="name").convert_dtypes().fillna("").sort_values("no").to_dict(orient='index')

	def pickle_dump(obj, path):
		with open(path, mode='wb') as f:
			pickle.dump(obj,f)

	def user_list() :
		u_list = pd.read_csv(Conf["datadir"] + "/all_user.csv", encoding="utf-8_sig",index_col="name").fillna("").to_dict(orient='index')
		for n ,v in list(u_list.items()) :
			u_list[n]["pass"] += "="
		pickle_dump(u_list,Conf["datadir"] + "/user_list.pickle")

		#os.remove(Conf["datadir"] + "/all_user.csv")

	def omiai_list() :
		omiai_list = pd.read_csv(Conf["datadir"] + "/all_omiai.csv", encoding="utf-8_sig",index_col="user").dropna(how='all').fillna("").convert_dtypes().to_dict(orient='index')
		for n ,v in list(omiai_list.items()) :
			omiai_list[n] |= {"no":"","cancel": "","request":"","baby":""}
			omiai_list[n]["pass"] += "="
		pickle_dump(omiai_list,Conf["datadir"] + "/omiai_list.pickle")

		#os.remove(Conf["datadir"] + "/all_omiai.csv")

	def user_dat(in_name) :
		file = Conf["datadir"] + "/" + in_name + "/pickle"
		os.makedirs(file, exist_ok=True)
		change_str = ["魂魄 妖夢" ,"西行寺 幽々子" ,"八雲 紫" ,"八雲 藍"]

		#============================================================#

		col_names = [  "no" ,"name", "type", "get"  ]
		data  = sub_def.open_csv("waza.csv",in_name,0,1,col_names)
		new_waza = {name:{ "no":v["no"], "type":v["type"], "get":0} for name,v in Tokugi_dat.items()}

		for name,v in data.items() :
			if(name not in ("" ,"-","0")) :
				new_waza[name]["get"] = v.get("get",0)
		pickle_dump(new_waza,file + "/waza.pickle")

		#============================================================#

		col_names = [  "no" ,"name", "type_zukan", "get" ,"abc" ]
		data = sub_def.open_csv("zukan.csv",in_name,0,1,col_names)
		new_zukan = {name: {"no":mon["no"],"m_type":mon["m_type"],"get":0} for name,mon in M_list.items()}

		for name,v in list(data.items()) :
			if(name not in ("" ,"-","0")) :
				for txt in change_str :
					if(name == txt) :
						n_name = name.replace(' ', '')
						data[n_name] = v
						del data[name]

		for name,v in new_zukan.items() :
			if(name not in ("" ,"-","0")) :
				new_zukan[name]["get"] = data.get(name,{"get":0}).get("get",0)

		get = len([1 for v in new_zukan.values() if(v.get("get") == 1)])

		mleng = len(new_zukan)
		s = get / mleng * 100
		get_txt = f"{get}／{mleng}匹 ({s:.2f}％)"

		pickle_dump(new_zukan,file + "/zukan.pickle")

		#============================================================#

		data = sub_def.open_csv("keyset.csv",in_name,0,0)
		new_d = {d["type"]:{"no":d["no"],"get":d["get"]} for d in data}
		data = {name:v for name,v in new_d.items() if(name not in ("" ,"-","0"))}
		pickle_dump(data,file + "/room_key.pickle")

		#============================================================#

		data = sub_def.open_csv("park.csv",in_name)
		data = [v for v in data if(v["name"] not in ("" ,"-","0"))]
		for i,pt in enumerate(data,1) :
			if(pt["name"] not in ("" ,"-","0")) :
				pt["no"] = i
				for txt in change_str :
					if(pt["name"] == txt) :
						pt["name"] = pt["name"].replace(' ', '')

		n_PPT=pd.DataFrame(data)
		mapper = {
			"no": 'no',
			"name": "name",
			"lv": "lv",
			"mlv":"mlv",
			"hai":"hai",
			"hp":"hp",
			"mhp":"mhp",
			"mp":"mp",
			"mmp":"mmp",
			"atk":"atk",
			"def":"def",
			"agi":"agi",
			"exp":"exp",
			"n_exp":"n_exp",
			"sei":"sei",
			"sex":"sex",
		}
		n_PPT = n_PPT[mapper.keys()].rename(columns=mapper)
		n_PPT = n_PPT.astype({"no" : "Int64"})
		n_PPT = n_PPT.to_dict(orient="records")
		pickle_dump(n_PPT,file + "/park.pickle")

		#============================================================#

		data = sub_def.open_csv("pt.csv",in_name)
		data = [v for v in data if(v["name"] not in ("" ,"-","0"))]

		for i,pt in enumerate(data,1) :
			if(pt["name"] not in ("" ,"-","0")) :
				pt["no"] = i

				for txt in change_str :
					if(pt["name"] == txt) :
						pt["name"] = pt["name"].replace(' ', '')

		n_PT=pd.DataFrame(data)
		mapper = {
			"no": 'no',
			"name": "name",
			"lv": "lv",
			"mlv":"mlv",
			"hai":"hai",
			"hp":"hp",
			"mhp":"mhp",
			"mp":"mp",
			"mmp":"mmp",
			"atk":"atk",
			"def":"def",
			"agi":"agi",
			"exp":"exp",
			"n_exp":"n_exp",
			"sei":"sei",
			"sex":"sex",
		}
		n_PT = n_PT[mapper.keys()].rename(columns=mapper)
		n_PT = n_PT.astype({"no" : "Int64"})
		n_PT = n_PT.to_dict(orient="records")

		pickle_dump(n_PT,file + "/party.pickle")
		#============================================================#

		data = sub_def.open_csv("user.csv",in_name,1)
		if (data.get("play2")) :
			del data["play1"]
			del data["play2"]
			del data["play3"]
			del data["turn"]
		data["isekai_limit"] = 0
		data["isekai_key"] = 1
		data["pass"] += "="
		data["getm"] = get_txt

		pickle_dump(data,file + "/user.pickle")
		#============================================================#

		data = sub_def.open_csv("vips.csv" ,in_name,1)
		vips = ["add" ,"account" ,"vips"]
		for v in vips :
			if (data.get(v)) :
				del data[v]
		pickle_dump(data,file + "/vips.pickle")
		#============================================================#

		#remove_glob(file + "/*.csv")

		return

	user_list()
	omiai_list()

	#.datを変換----------------------------------------------------------
	files = glob.glob("./dat/*.csv")
	os.makedirs("./dat/pickle", exist_ok=True)

	for f in files :
		fp = f.replace('csv', 'pickle')
		fpp = fp.replace('./dat', './dat/pickle')
		pickle_dump(open_dat(f),fpp)
	#---------------------------------------------------------------------

	M_list = sub_def.open_monster_dat()
	Tokugi_dat = sub_def.open_tokugi_dat()
	u_list = sub_def.open_user_list()

	for u in u_list.keys() :
		with open(Conf["datadir"]+"/cgi_to_py_log.txt", mode='a',encoding='utf-8') as f:
			f.write(f"{u} 変換開始\n")
			user_dat(u)
			f.write(f"{u} 変換完了\n")

	for u in u_list.keys() :
		file = Conf["datadir"] + "/" + u
		remove_glob(file + "/*.csv")
