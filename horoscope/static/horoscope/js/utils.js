window.onload = function () {
    $('.progress-bar').each(function () {
        let val = $(this).attr('aria-valuenow') / $(this).attr('aria-valuemax')
        $(this).css('width', `${val * 100}%`)
    });
}