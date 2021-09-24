function revokeFriend(friend) {
    let form = document.createElement("form");
    form.action = "/friends/revoke/";
    form.method = "POST";
    let input = document.createElement("input");
    input.name = "requested_friend";
    input.value = friend;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

$(window).on("load", function () {
    $("button[id^='revoke-']").click(function () {
        revokeFriend(this.id.split('-')[1])
    });
})