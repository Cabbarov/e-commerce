$(".reply").click(function() {
    $('html,body').animate({
        scrollTop: $(".leave-comment").offset().top},
        'slow');
});
function reply_click(clicked_id)
  {
	  var id = clicked_id
	  var action = $('input[name="reply_id"]').attr("value")
	  $('input[name="reply_id"]').attr("value", value=id)
	  $('input[name="reply_id"]').children(input).focus();
  }