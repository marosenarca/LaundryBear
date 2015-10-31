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
	$tableBody.find("a.edit-service-button").last().click(function() {
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
	});
	$tableBody.find("a.delete-service-button").last().click(function() {
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
	});

	// pop item off
	$selectedService.remove();
	// reset fields
	$serviceInput[0].selectedIndex = 0;
	$priceInput.val('');

	return false;
});

$("#save-button").click(function() {
	var $addedServices = $("#service-table-body").children();
	$addedServices.each(function(index, element) {
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

	var timeString = ''

	$("#id_hours_open").val();
