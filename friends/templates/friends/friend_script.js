/**
 * Friendscript v1.0
 */

(function (friends) {
    var check = document.getElementById("tokens").value
    if (document.domain === '{{own_domain}}' && check !== null) {
        writeFriends(friends);
    }
})