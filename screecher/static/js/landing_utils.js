window.onload = function () {
    $(".timezone").each(function () {
        $(this).val(Intl.DateTimeFormat().resolvedOptions().timeZone)
    });

    $(".btn-screecher").click(function () {
        $("#login").toggle();
        $("#register").toggle();
    });
}