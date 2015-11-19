$(document).ready(function() {
	total();
});

function total() {
	var rows = $("tbody tr");
	$.each(rows, function(index, row) {
		var mult = $(row).data("pieces") / 7;
		var pricePerKg = $(row).data("price");
		$(row).find(".row-total").html((pricePerKg * mult).toFixed(2));
	});
	var cols = $("tbody tr td:last-child");
	var total = 0;
	$.each(cols, function(index, column) {
		total += +$(column).html();
	});
	total = parseFloat(total).toFixed(2);
	$("#total").html(total);
}
