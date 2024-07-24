	//ボタンの多重クリック対策。クリックで押せなくする
	$(document).ready(function(){
		$("form").submit(function() {
			//var self = this;
			$(":submit").prop("disabled", true);
			setTimeout(function() {
				$(":submit").prop("disabled", false);
			}, 20000);
		});
	});

	//自動移動用スクリプト
	function post(path, params, method='post') {
		//使用例 post("index.php", {val:"hogehoge"});

		// The rest of this code assumes you are not using a library.
		// It can be made less wordy if you use one.
		const form = document.createElement('form');
		form.method = method;
		form.action = path;

		for (const key in params) {
			if (params.hasOwnProperty(key)) {
				const hiddenField = document.createElement('input');
				hiddenField.type = 'hidden';
				hiddenField.name = key;
				hiddenField.value = params[key];
				form.appendChild(hiddenField);
			}
		}

		document.body.appendChild(form);
		form.submit();
	}

	//ログインメニュー鍵、特技一覧開閉
	function bo(a,b) {
		document.getElementById(b).style.display ="none";
		const x = document.getElementById(a);
		if(x.style.display=="block"){
			x.style.display ="none";
		} else {
			x.style.display ="block";
		}
	}

	//プルダウン選択モンスター画像切り替え用
	function main(imgpath,pt,m_name) {
		pt = pt.split("/");
		pt[0] = m_name ? m_name : "0";

		Images = new Image();
		for (let i = 0; i <= pt.length-1; i++) {
			Images[i] = new Image();
			Images[i].src = imgpath + pt[i] + ".gif";
		}
	}

	function change_img1() {
		form1.img1.src = Images[ form1.haigou1.options[form1.haigou1.selectedIndex].value ].src;
	}
	function change_img2() {
		form1.img2.src = Images[ form1.haigou2.options[form1.haigou2.selectedIndex].value ].src;
	}

	//mget,park
	function change_img() {
		form1.img1.src = Images[form1.Mno.selectedIndex].src;
	}
