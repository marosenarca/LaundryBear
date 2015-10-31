$(document).foundation();

$(window).bind("load", function () {
   var footer = $("#footer");
   var pos = footer.position();
   var height = $(window).height();
   height = height - pos.top;
   height = height - footer.height();
   if (height > 0) {
       footer.css({
           'margin-top': height + 'px'
       });
   }
});

$(document).foundation({
    reveal : {
        multiple_opened:true
    }
});

$('#drop1 option').click(function(){
  var value = $(this).val();
  $('#selected').html(value);
});

$("dl.sub-nav dd").click(function(){
  $("dl.sub-nav dd.active").removeClass("active");
  $(this).addClass("active");
  $("#search").prop("name", $(this).children().html().toLowerCase());
  return false;
});

$("#set-service-button").click(function() {

	var $serviceInput = $("#service-input");
	var $priceInput = $("#price-input");
	var servicePk = $serviceInput.val();
	var price = $priceInput.val();

	if (isNaN(servicePk) || price.length === 0) {
		return false;
	}

	// create a new row
	var $selectedService = $serviceInput.children(":selected");
	var template = $("#table-row-template").html();
	var compiledTemplate = template.replace(/__service-name__/g, $selectedService.html()).replace(/__description__/g, $selectedService.data("service-description")).replace(/__price__/g, price).replace(/__pk__/g, servicePk);

	var $tableBody = $("#service-table-body");
	$tableBody.append(compiledTemplate);
	$tableBody.find("a.edit-service-button").last().click(editServiceHandler);
	$tableBody.find("a.delete-service-button").last().click(deleteServiceHandler);

	// pop item off
	$selectedService.remove();
	// reset fields
	$serviceInput[0].selectedIndex = 0;
	$priceInput.val('');

	return false;
});

$("#save-button").click(function() {
	var $addedServices = $("#service-table-body").children();
	var $formsetContainer = $("#price-formset-container");
	$addedServices.each(function(index, element) {
		var servicePk = $(element).data("service-pk");
		var price = $(element).data("service-price");
		$formsetContainer.find("#id_price_set-" + index + "-service").val(servicePk);
		$formsetContainer.find("#id_price_set-" + index + "-price").val(price);
		addServiceFormset($("price-formset-container"));
	});
	$(this).parent().submit();
});

function addServiceFormset($formsetContainer) {
	var formCount = $formsetContainer.children().length;
	var template = $("#formset-form-template").html();
	var compiledTemplate = template.replace(/__prefix__/g, formCount);
	$formsetContainer.append(compiledTemplate);

	$("#id_price_set-TOTAL_FORMS").val(formCount + 1);
	return;
}

$("#open-time, #close-time").on("change", function() {
	var openTime = $("#open-time").val();
	var closeTime = $("#close-time").val();

	if (openTime == 'null' || closeTime == 'null') {
		$("#id_hours_open").val('');
	}

	var timeString = openTime + ' - ' + closeTime;

	$("#id_hours_open").val(timeString);
});

$("#days-container input").on("change", function() {
	var checked = [];
	$("#days-container input").each(function(index, element) {
		var $element = $(element);
		if ($element.prop("checked")) {
			checked.push($element.next().html());
		}
	});
	var dayString = checked.join(', ');
	$("#id_days_open").val(dayString);
});

// load hours_open and days_open and services
{
	var hours_open = $("#id_hours_open").val();
	var hours_open_array = hours_open.split(" - ");
	$("#open-time").val(hours_open_array[0]);
	$("#close-time").val(hours_open_array[1]);

	var days_open = $("#id_days_open").val();
	var days_open_array = days_open.split(", ");
	$.each(days_open_array, function(index, day) {
		$("#" + day.toLowerCase()).prop("checked", true);
	});

	var $services = $("#price-formset-container").children();
	$.each($services, function(index, service) {
		var $service = $(service);
		var itemIndex = $service.data("item");
		var servicePk = $service.find("#id_price_set-" + itemIndex + "-service").val();
		if (servicePk.length === 0 ) {
			return;
		}
		var price = $service.find("#id_price_set-" + itemIndex + "-price").val();
		var $option = $("#service-input").find("option[value=" + servicePk + "]");
		var description = $option.data("service-description");
		var serviceName = $option.data("service-name");
		$option.remove();
		var template = $("#table-row-template").html();
		var compiledTemplate = template.replace(/__service-name__/g, serviceName).replace(/__description__/g, description).replace(/__price__/g, price).replace(/__pk__/g, servicePk);

		var $tableBody = $("#service-table-body");
		$tableBody.append(compiledTemplate);
		$tableBody.find("a.edit-service-button").last().click(editServiceHandler);
		$tableBody.find("a.delete-service-button").last().click(deleteServiceHandler);
	});
}

function editServiceHandler() {
	var $tr = $(this).closest("tr");
	var pk = $tr.data("service-pk");
	var optionName = $tr.data("service-name");
	var price = $tr.data("service-price");
	var description = $tr.data("service-description");
	// remove from table
	$tr.remove();

	// add back into combobox and set as selected
	var optionTemplate = $("#option-template").html();
	var compiledOptionTemplate = optionTemplate.replace(/__value__/, pk).replace(/__optionname__/g, optionName).replace(/__description__/, description);
	var $option = $(compiledOptionTemplate);
	$("#service-input").append($option);
	$("#service-input").val(pk);

	// put price back
	$("#price-input").val(price);
	return false;
}

function deleteServiceHandler() {
	var $tr = $(this).closest("tr");
	var pk = $tr.data("service-pk");
	var optionName = $tr.data("service-name");
	var description = $tr.data("service-description");
	// remove from table
	$tr.remove();
	// add back into combobox
	var optionTemplate = $("#option-template").html();
	var compiledOptionTemplate = optionTemplate.replace(/__value__/, pk).replace(/__optionname__/g, optionName).replace(/__description__/, description);
	var $option = $(compiledOptionTemplate);
	$("#service-input").val("null");
	$("#service-input").append($option);
	return false;
}

$('#logout_submit').click(function(){$('#logout_form').submit();});
