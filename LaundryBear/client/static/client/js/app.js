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

$('#logout_submit').click(function(){$('#logout_form').submit();});


$(document).ready(function() {
    $("#buttonForModal").click(function() {
      $("#myModal").reveal();
    });
  });

$(".reveal-modal-button").click(function() {
	var modalId = $(this).data("reveal-id");
	$("#" + modalId + " input").val(0);
});

$(".add-to-basket").click(function() {
	var pieces = $(this).siblings("input").val();
	pieces = parseFloat(pieces).toFixed(0);
	if (pieces.length === 0 || pieces == 0) {
		return false;
	}

	var servicename = $(this).data("servicename");
	var pk = $(this).data("pk")
	var pricePerKg = $(this).data("price-per-kilo");
	var price = pieces * pricePerKg / 7;
	price = parseFloat(price).toFixed(2);
	var template = $("#row-template").html();
	var compiledTemplate = template.replace(/__servicename__/, servicename).replace(/__pieces__/g, pieces).replace(/__price__/g, price).replace(/__pk__/, pk);

	$("#table-body").append(compiledTemplate);

	$(this).siblings("input").val(0);
	$(this).parent().foundation("reveal", "close");

	updateTotals();
});

function updateTotals() {
	var total = 0;
	$("#table-body").children().each(function(index, element) {
		total += +$(element).data("price").valueOf();
	});
	$("#total-price").html(total);
}

$("#table-body").on("click", ".alert", function(e) {
	$(e.target).closest("tr").remove();
	updateTotals();
	return false;
});

$("#table-body").on("click", ".info", function(e) {
	var revealId = $(e.target).data("reveal-id");
	var modal = $("#" + revealId);
	modal.foundation("reveal", "open");
	var items = $(e.target).data("pieces");
	modal.find("input").val(+items);

	$(e.target).closest("tr").remove();
	return false;
})
