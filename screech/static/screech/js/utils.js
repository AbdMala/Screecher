function init_comment(screech_id) {
    $("#screech_area").focus().val($('#UserForScreech' + screech_id).text() + " ")
}

function init_rescreech(screech_id) {
    let user = $('#UserForScreech' + screech_id).text()
    let screech_text = $("#" + screech_id).find(".card-body").text()
    $("#screech_area").val(user + " screeched:\r\n\"" + screech_text + "\"")
    $("#submit").trigger("click")
}

window.onload = function () {
    $(".card").each(function () {
        let screech_id = this.id

        $(this).find(".btn-rescreech").click(function () {
            init_rescreech(screech_id)
        });

        $(this).find(".btn-comment").click(function () {
            init_comment(screech_id)
        });
    });
}