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
	serviceInput.children("option[value=" + servicePk + "]").prop("disabled", true);
	serviceInput.val("null");
	$("#price-input").val("");

	return false;
});

// takes a service pk and returns a service object
function getService(pk) {
	var service = new Object();
	var $serviceList = $("#services-list").children("i[data-pk=" + pk + "]");
	service.description = $serviceList.data("service-description");
	service.name = $serviceList.data("service-name");
	service.pk = pk;
	return service;
}

function addServiceRow(service, price) {
	// grab the template
	var template = $("#table-row-template").html();

	// compile the template
	var compiledTemplate = template.replace(/__pk__/g, service.pk).replace(/__service-name__/g, service.name).replace(/__price__/g, price).replace(/__description__/g, service.description);

	// add to the table
	$tableBody = $("#service-table-body");
	$tableBody.append(compiledTemplate);

	// attach some event listeners
	var latestRow = $tableBody.children().last();
	latestRow.find(".edit-service-button").on("click", function() {
		// renable option
		var $row = $(this).closest("tr");
		var pk = $row.data("service-pk");
		var serviceInput = $("#service-input");
		serviceInput.children("option[value=" + pk + "]").prop("disabled", false);

		// place service and price in input boxes
		serviceInput.val($row.data("service-pk"));
		$("#price-input").val($row.data("service-price"));

		// remove from table
		$row.remove();

		return false;
	});
	latestRow.find(".delete-service-button").on("click", function() {
		var $row = $(this).closest("tr");
		var pk = $row.data("service-pk");
		$("#service-input").children("option[value=" + pk + "]").prop("disabled", false);
		var $row = $(this).closest("tr");
		// mark as deleted
		var $formsetDiv = $("#price-formset-container").find("div[data-pk=\"" + pk + "\"]");
		console.log($formsetDiv);
		$formsetDiv.find("input[type=\"checkbox\"]").prop("checked", true);
		// remove from table
		$row.remove();
		return false;
	});
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
	loadServiceItems();
});

function loadServiceItems() {
	var $savedServices = $("#price-formset-container").children();
	$savedServices.each(function(index, element) {
		var pk = $(element).find("select").val();
		if (pk.length === 0) {
			return;
		}
		var service = getService(pk);
		var price = $(element).find("input[type=\"number\"]").val();
		addServiceRow(service, price);
	});
}
