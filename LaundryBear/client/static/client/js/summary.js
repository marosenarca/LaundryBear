$(document).ready(function() {
	loadTable();
	updateTotals();
});

function loadTable() {
	var selectedServices = document.cookie.replace(/(?:(?:^|.*;\s*)selectedServices\s*\=\s*([^;]*).*$)|^.*$/, "$1");

	if (selectedServices.length === 0) {
		selectedServices = [];
	} else {
		selectedServices = JSON.parse(selectedServices);
	}
	$.each(selectedServices, function(index, service) {
		insertRow(service);
	});
}

function updateTotals() {
	var total = 0;
	$("#table-body").children().each(function(index, element) {
		total += +$(element).data("price").valueOf();
	});
	$("#subtotal").html(total.toFixed(2));
	total += +$("#deliveryfee").html();
    total += +$("#servicecharge").html();
	$("#total").html(total.toFixed(2));
}

function insertRow(service) {
	var template = $("#row-template").html();
	var compiledTemplate = template.replace(/__servicename__/, service.name).replace(/__pieces__/g, service.pieces).replace(/__price__/g, service.price).replace(/__pk__/, service.pk);


	$("#table-body").append(compiledTemplate);
}
