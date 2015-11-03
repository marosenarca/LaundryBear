$("#set-service-button").on("click", function() {
	var $serviceInput = $("#service-input");
	var $priceInput = $("#price-input");
	var servicePk = $serviceInput.val();
	var price = $priceInput.val();

	// inputs are invalid, do nothing
	if (isNaN(servicePk) || price.length === 0) {
		return false;
	}

	var service = getService(servicePk);

	addServiceRow(service, price);
	var index = $("#price-formset-container").children().size() - 1;
	addToServiceFormset(service, price, index);

	// remove from options
	var serviceInput = $("#service-input")
	serviceInput.children("option[value=" + servicePk + "]").remove();
	serviceInput.val("null");
	$("#price-input").val("");

	return false;
});

// takes a service pk and returns a service object
function getService(pk) {
	var service = new Object();
	var $serviceOption = $("#service-input").children("option[value=" + pk + "]");
	service.description = $serviceOption.data("service-description");
	service.name = $serviceOption.data("service-name");
	service.pk = pk;
	return service;
}

function addServiceRow(service, price) {
	// grab the template
	var template = $("#table-row-template").html();

	// compile the template
	var compiledTemplate = template.replace(/__pk__/g, service.pk).replace(/__service-name__/g, service.name).replace(/__price__/g, price).replace(/__description__/g, service.description);

	// add to the table
	$("#service-table-body").append(compiledTemplate);
}

function addToServiceFormset(service, price, index) {
	$("#id_price_set-" + index + "-price").val(price);
	$("#id_price_set-" + index + "-service").val(service.pk);
	$("#id_price_set-" + index + "-DELETE").val(false);
}

$(function() {
	// load set opening time
	var hoursOpen = $("#id_hours_open").val();
	hoursOpen = hoursOpen.split(" - ");
	var openTime = hoursOpen[0];
	var closeTime = hoursOpen[1];
	$("#open-time").val(openTime);
	$("#close-time").val(closeTime);

	// load set days open
	var daysOpen = $("#id_days_open").val();
	daysOpen = daysOpen.split(", ");
	$.each(daysOpen, function(index, element) {
		$("#" + element.toLowerCase()).prop("checked", true);
	});

	// load services
});
