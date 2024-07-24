function countdownTimer() {
	//const now = new Date(); //現在時刻を取得
	//const end = new Date(document.getElementById('b_count_txt').textContent); //戦闘可能時間
	//const diff = end.getTime() + 1000 - now.getTime(); //時間の差を取得（ミリ秒）

	//ミリ秒から単位を修正
	//const calcSec = Math.floor(diff / 1000) % 60;

	const now = new Date(); //現在時刻を取得
	const now_e = Math.floor( now.getTime() / 1000 );

	const end = document.getElementById('b_count_txt').textContent ; //戦闘可能時間
	const diff = Math.floor(end) - now_e;

	if (diff <= 0) {
		document.getElementById('b_count').textContent = '戦闘OK';
		$(".battle_go :submit").prop("disabled", false);
	} else {
		document.getElementById('b_count').textContent = "次の戦闘まで" + diff + "秒";
		setTimeout(countdownTimer, 1000);
	}
}

$(document).ready(function(){
	countdownTimer()
});
