function full_screen(id) {
    let element = $(`#${id}`)
    element.height($("#SWAG-footer").offset().top - element.offset().top);

    $(window).resize(function () {
        element.height($("#SWAG-footer").offset().top - element.offset().top);
    })
}