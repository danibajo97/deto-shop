$(".remove-product").each(function() {
    var nameProduct = $(this)
        .parent()
        .parent()
        .parent()
        .find(".name")
        .html();
    var urlProduct = $(this)
        .parent()
        .parent()
        .parent()
        .find(".url")
        .html();
    $(this).on("click", function() {
        swal({
            title: "Are you sure?",
            icon: "warning",
            text: nameProduct + " will be removed from your cart",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                window.location = urlProduct;
            }
        });
    });
});

$(".remove-address").each(function() {
    var urlProduct = $(this)
        .parent()
        .parent()
        .parent()
        .find(".url")
        .html();
    $(this).on("click", function() {
        swal({
            title: "Are you sure?",
            icon: "warning",
            text: "This Address will be removed from your Address Book",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                window.location = urlProduct;
            }
        });
    });
});

$(".logout").each(function() {
    var urlProduct = $(this)
        .parent()
        .parent()
        .parent()
        .find(".url")
        .html();
    $(this).on("click", function() {
        swal({
            title: "Are you sure?",
            icon: "warning",
            text: "Are you sure that you wanna logout?",
            buttons: true,
            dangerMode: true,
        }).then((willDelete) => {
            if (willDelete) {
                window.location = urlProduct;
            }
        });
    });
});