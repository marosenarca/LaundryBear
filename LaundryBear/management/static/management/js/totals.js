$(document).ready(function() {
	updateTotal();
});

function updateServiceFee(total) {
	var fee = total * 0.1;
	$("#servicecharge").html(fee.toFixed(2));
	return fee;
}

function updateColumnTotals() {
	var cols = $("tbody tr td:last-child");
	var total = 0;
	$.each(cols, function(index, column) {
		total += +$(column).html();
	});
	var fee = updateServiceFee(total);
	total += fee;
	total += +$("#deliveryfee").html();
	$("#total").html(total.toFixed(2));
}

function updateRowTotals() {
	// calculate total per row
	var rows = $("tbody tr");
	$.each(rows, function(index, row) {
		var mult = $(row).data("pieces") / 7;
		var pricePerKg = $(row).data("price");
		$(row).find(".row-total").html((pricePerKg * mult).toFixed(2));
	});
}

function updateTotal() {
	updateRowTotals();
	updateColumnTotals();
}
