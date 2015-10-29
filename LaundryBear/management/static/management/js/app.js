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
	var $tableBody = $("#service-table-body");
	var template = $("#table-row-template")[0];

	var servicePk = $serviceInput.val();
	var price = $priceInput.val();

	if (isNaN(servicePk) || price.length === 0) {
		return false;
	}

	// create a new row
	var $selectedService = $serviceInput.children(":selected");
	var $tableRow = $("tr", template.content).clone(true);
	$tableRow.data("service-pk", servicePk);
	$tableRow.children(".service-name").html($selectedService.html());
	$tableRow.children(".description").html($selectedService.data("description"));
	$tableRow.children(".price").html(price);

	// add to hidden formset
	var $formsetContainer = $("#price-formset-container");
	$formsetContainer.find("#id_price_set-0-service").val(servicePk);
	$formsetContainer.find("#id_price_set-0-price").val(price);

	$tableBody.append($tableRow);

	// pop item off
	$selectedService.remove();
	// reset fields
	$serviceInput[0].selectedIndex = 0;
	$priceInput.val('');

	return false;
});

function cloneServiceFormset() {

}
