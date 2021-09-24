window.onload = function () {
    $('.ReplyBtn').click(function () {
        let form = $('#Form' + this.id.slice(8))
        form.attr('action', '/message/outbox/')
        form.submit()
    });

    $('.ReadBtn').click(function () {
        let form = $('#Form' + this.id.slice(7))
        form.attr('action', '/message/read/')
        form.submit()
    });

    $('.RemoveBtn').click(function () {
        let form = $('#Form' + this.id.slice(9))
        form.attr('action', '/message/ignore/')
        form.submit()
    });
}