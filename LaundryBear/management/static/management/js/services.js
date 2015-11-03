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
	var index = getNextIndex();
	addToServiceFormset(service, price, index);
	if ($("#price-formset-container").data("edit-pk") == "None") {
		addEmptyFormset();
	}

	$("#service-input").val("null");
	$("#price-input").val("");
	$("#price-formset-container").data("edit-pk", "None");

	return false;
});

function getNextIndex() {
	var $formsetContainer = $("#price-formset-container");
	var editPk = $formsetContainer.data("edit-pk");
	if (editPk != "None") {
		return $formsetContainer.find("div[data-pk=\"" + editPk + "\"]").data("item");
	}
	return $formsetContainer.children().size() - 1;
}

function addEmptyFormset() {
	var template = $("#formset-form-template").html();
	var $formsetContainer = $("#price-formset-container");
	var totalForms = $formsetContainer.children().size();
	var compiledTemplate = template.replace(/__prefix__/g, totalForms);
	$("#id_price_set-TOTAL_FORMS").val(totalForms + 1)
	$formsetContainer.append(compiledTemplate);
}

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
	// disable from option
	$("#service-input").find("option[value=\"" + service.pk + "\"]").prop("disabled", true);
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
		var $row = $(this).closest("tr");
		var pk = $row.data("service-pk");

		// renable option
		var serviceInput = $("#service-input");
		serviceInput.children("option[value=" + pk + "]").prop("disabled", false);

		// place service and price in input boxes to edit
		serviceInput.val($row.data("service-pk"));
		$("#price-input").val($row.data("service-price"));


		// set a var that we are editing
		$("#price-formset-container").data("edit-pk", pk);

		// remove from table
		$row.remove();

		return false;
	});
	latestRow.find(".delete-service-button").on("click", function() {
		var $row = $(this).closest("tr");
		var pk = $row.data("service-pk");

		// re-enable the option
		$("#service-input").children("option[value=" + pk + "]").prop("disabled", false);

		// mark as deleted
		var $formsetDiv = $("#price-formset-container").find("div[data-pk=\"" + pk + "\"]");
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

