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

	// add to hidden formset
	var $formsetContainer = $("#price-formset-container");
	var currentFormsetIndex = $formsetContainer.children().length - 1;
	$formsetContainer.find("#id_price_set-" + currentFormsetIndex + "-service").val(servicePk);
	$formsetContainer.find("#id_price_set-" + currentFormsetIndex + "-price").val(price);

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
		$(this).closest("tr").remove();

		// add back into combobox and set as selected
		var optionTemplate = $("#option-template").html();
		var compiledOptionTemplate = optionTemplate.replace(/__value__/, pk).replace(/__selected__/, "true").replace(/__optionname__/g, optionName).replace(/__description__/, description);
		$("#service-input").children(":selected").prop("selected", false);
		var $option = $(compiledOptionTemplate);
		$("#service-input").append($option);

		// put price back
		$("#price-input").val(price);
		return false;
	});
	$tableBody.find("a.delete-service-button").last().click(function() {
		console.log("click");
		return false;
	});

	addServiceFormset($formsetContainer);

	// pop item off
	$selectedService.remove();
	// reset fields
	$serviceInput[0].selectedIndex = 0;
	$priceInput.val('');

	return false;
});

function addServiceFormset($formsetContainer) {
	var formCount = $formsetContainer.children().length;
	var template = $("#formset-form-template").html();
	var compiledTemplate = template.replace(/__prefix__/g, formCount);
	$formsetContainer.append(compiledTemplate);

	$("#id_price_set-TOTAL_FORMS").val(formCount + 1);
	return;
}
