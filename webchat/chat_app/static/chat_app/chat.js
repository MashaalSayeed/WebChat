let loc = window.location;
let endpoint = (loc.protocol == 'https:' ? 'wss://' : 'ws://') + loc.host + loc.pathname;

let socket = new ReconnectingWebSocket(endpoint);
let form = $('#message_form');
let input = $('#id_content');
let chat_history = $('#message_history');
let currentUser = $('#current_user').val();

socket.onmessage = function(e) {
    console.log('message', e);
    data = JSON.parse(e.data);

    if (data.username == current_user) {
        chat_history.append(`
        <div class="outgoing_msg">
            <div class="sent_msg">
                <p>${data.content}</p>
                <span class="time_date"> 11:01 AM | Today</span>
            </div>
        </div>`)
    } else {
        chat_history.append(`
        <div class="incoming_msg">
            <div class="incoming_msg_img">
                <img src="https://ptetutorials.com/images/user-profile.png" alt="...">
            </div>
            <div class="received_msg">
                <div class="received_withd_msg">
                    <p>${data.content}</p>
                    <span class="time_date"> 11:01 AM | Today</span>
                </div>
            </div>
        </div>`)
    }
}

socket.onopen = function(e) {
    console.log('Open', e);

    form.submit(function(event) {
        event.preventDefault();
        
        data = JSON.stringify({'content': input.val()})
        socket.send(data)
        form[0].reset()
    })
}

socket.onclose = function(e) {
    console.log('close', e);
}

socket.onerror = function(e) {
    console.log('error', e);
}