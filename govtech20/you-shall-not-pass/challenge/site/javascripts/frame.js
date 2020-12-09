window.addEventListener("message", receiveMessage, false);

function receiveMessage(event) {
    // verify sender is trusted
    if (
        !/^http:\/\/yhi8bpzolrog3yw17fe0wlwrnwllnhic.alttablabs.sg/.test(
            event.origin
        )
    ) {
        return;
    }

    // display message
    msg = event.data;
    if (msg == "off") {
        document.body.style.color = "#95A799";
    } else if (msg == "on") {
        document.body.style.color = "black";
    } else if (
        !msg.includes(" ") &&
        !msg.includes("'") &&
        !msg.includes("&") &&
        !msg.includes("|") &&
        !msg.includes("%") &&
        !msg.includes("@") &&
        !msg.includes("!") &&
        !msg.includes("#") &&
        !msg.includes("^")
    ) {
        var broadcastList = document.getElementById("broadcastList");
        var newBroadCast = document.createElement("div");
        newBroadCast.innerHTML =
            '<li class="list-group-item d-flex justify-content-between lh-condensed"><h6 class="my-0">' +
            msg +
            "</h6></li>";
        while (newBroadCast.firstChild) {
            broadcastList.appendChild(newBroadCast.firstChild);
        }
    }
}
