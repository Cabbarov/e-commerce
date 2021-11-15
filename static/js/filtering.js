$(document).ready(function () {
    $(".ajaxLoader").hide();
    $(".filters,#priceFilterBtn").on('click', function () {
        var _filterObj = {};
        var _minPrice = $('#maxPrice').attr('min');
        var _maxPrice = $('#maxPrice').val();
        _filterObj.minPrice=_minPrice;
        _filterObj.maxPrice=_maxPrice;
        $(".filters").each(function (index, ele) {
            var _filterVal = $(this).val();
            var _filterKey = $(this).data('filter');
            // console.log(_filterKey,_filterVal)
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
            });
        });
        console.log(_filterObj);
        $.ajax({
            url:'/products/filter-data',
            data:_filterObj,
            dataType:'json',
            beforeSend:function(){
                $(".ajaxLoader").show();
            },
            success:function(res){
                $("#filteredProducts").html(res.data);
                // $("#filteredProducts1").html(res.data);
                
                $(".ajaxLoader").hide();
            }
                
        });
    });
    $("#maxPrice").on('blur',function(){
    var _min=$(this).attr('min');
    var _max=$(this).attr('max');
    var _value=$(this).val();
    console.log(_value,_min,_max);
    if(_value < parseInt(_min) || _value > parseInt(_max)){
        alert('Values should be '+_min+'-'+_max);
        $(this).val(_min);
        $(this).focus();
        $("#rangeInput").val(_min);
        return false;
    }
});

});