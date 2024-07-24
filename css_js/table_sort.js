$(function() {

	$('.sortBtnA').on('click', function() {
		var rel = $(this).attr('rel');
		$('.list').html(
			$('#tuika_mob_list .table_m_box').sort(function(a, b) {
				var valueA = $(a).find('.'+rel).text();
				var valueB = $(b).find('.'+rel).text();
				if (valueA < valueB) {
					return 1;
				} else {
					return -1;
				}
			})
		);
	});

	$('.sortBtnB').on('click', function() {
		var rel = $(this).attr('rel');
		$('.list').html(
			$('#tuika_mob_list .table_m_box').sort(function(a, b) {
				var valueA = $(a).find('.'+rel).text();
				var valueB = $(b).find('.'+rel).text();
				if (valueA > valueB) {
					return 1;
				} else {
					return -1;
				}
			})
		);
	});

	$('.sortBtnC').on('click', function() {
		var rel = $(this).attr('rel');
		$('.list').html(
			$('#tuika_mob_list .table_m_box').sort(function(a, b) {
				var valueA = $(a).find('.'+rel).text();
				var valueB = $(b).find('.'+rel).text();
				if (Number(valueA) > Number(valueB)) {
					return 1;
				} else {
					return -1;
				}
			})
		);
	});

	$('.sortBtnD').on('click', function() {
		var rel = $(this).attr('rel');
		$('.list').html(
			$('#tuika_mob_list .table_m_box').sort(function(a, b) {
				var valueA = $(a).find('.'+rel).text();
				var valueB = $(b).find('.'+rel).text();
				if (Number(valueA) < Number(valueB)) {
					return 1;
				} else {
					return -1;
				}
			})
		);
	});


});
