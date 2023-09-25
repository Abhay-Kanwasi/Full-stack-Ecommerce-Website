$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 15,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id : id
        },
        success: function (data) {
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.minus-cart').click(function () {
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2]
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id : id
        },
        success: function (data) {
            element.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount
        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr("pid").toString();
    console.log(id);

    $.ajax({
        type: "GET",
        url: "/removecart/",  // Updated URL
        data: {
            prod_id: id
        },
        success: function (data) {
            console.log("Delete")
            // Check if the response contains 'amount' and 'totalamount' properties
            if ('amount' in data && 'totalamount' in data) {
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                element.parentNode.parentNode.parentNode.parentNode.remove()
            } else {
                console.log("Unexpected response format:", data);
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("Error:", errorThrown);
        }
    });
});


