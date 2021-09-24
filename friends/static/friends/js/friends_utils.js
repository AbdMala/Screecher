function removeFriend(friend) {
    let form = document.createElement("form");
    form.action = "/friends/remove/";
    form.method = "POST";
    let input = document.createElement("input");
    input.name = "friend";
    input.value = friend;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function acceptFriend(friend) {
    let form = document.createElement("form");
    form.action = "/friends/accept/";
    form.method = "POST";
    let input = document.createElement("input");
    input.name = "new_friend";
    input.value = friend;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

function declineFriend(friend) {
    let form = document.createElement("form");
    form.action = "/friends/decline/";
    form.method = "POST";
    let input = document.createElement("input");
    input.name = "new_friend";
    input.value = friend;
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}


function writeFriends(friends) {
    for (let [username, friend, profile_picture] of friends) {
        let li = document.createElement('li');
        li.className = "list-group-item";
        li.style.display = "flex"
        li.style.alignItems = "center"
        li.innerText = `${username}\n(${friend})`;

        let img = document.createElement('img')
        img.src = profile_picture
        img.style.height = "50px"
        img.style.width = "50px"
        img.style.borderRadius = "50%"
        img.style.border = "1px solid #343a40"
        img.style.marginRight = "5px"
        li.prepend(img)

        let btn = document.createElement('button')
        btn.type = "button"
        btn.className = "btn btn-danger"
        btn.style.marginLeft = "auto"
        btn.innerHTML = "<i class=\"fa fa-fw fa-trash\"></i>"
        btn.onclick = function () {
            removeFriend(username)
        }
        li.appendChild(btn)

        window.friendlist.append(li);
    }
}


$(window).on("load", function () {
    $("button[id^='accept-']").click(function () {
        acceptFriend(this.id.split('-')[1])
    });

    $("button[id^='decline-']").click(function () {
        declineFriend(this.id.split('-')[1])
    });
})