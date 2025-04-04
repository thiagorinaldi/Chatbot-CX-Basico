window.onload = InitPage;

function InitPage() {
    var room = document.getElementsByName('token')[0].value;

    //Envia a primeira mensagem no chat
    $.post("../intent/", { data: "oi", session: room },
        function (data, status) {
            SendMessage("Bot", data);
        }
    );
}

function SendMessage(sender, text) {
    var div_dialog = document.getElementsByClassName("direct-chat-messages");

    var direct_chat_msg = document.createElement('div');

    var direct_chat_info = document.createElement('div');
    direct_chat_info.setAttribute('class', 'direct-chat-info clearfix');

    var span_name = document.createElement('span');

    var span_time = document.createElement('span');

    var d = new Date();
    var hor = d.getHours();
    var min = d.getMinutes().toString().replace(/^(\d)$/, '0$1');

    span_time.textContent = hor + ":" + min;

    var avatar = document.createElement('img');
    var hr = document.createElement('hr');

    var direct_chat_text = document.createElement('div');
    direct_chat_text.setAttribute('class', 'direct-chat-text');

    direct_chat_text.innerHTML = text;

    switch (sender) {
        case 'Bot':
            span_time.setAttribute('class', 'direct-chat-timestamp pull-right');
            direct_chat_msg.setAttribute('class', 'direct-chat-msg');
            span_name.setAttribute('class', 'direct-chat-name pull-left');
            span_name.textContent = "Robo";

            hr.setAttribute('class', 'hrLeft');

            break;

        case 'User':
            span_time.setAttribute('class', 'direct-chat-timestamp pull-left-time-stamp');
            direct_chat_msg.setAttribute('class', 'direct-chat-msg right');
            span_name.setAttribute('class', 'direct-chat-name pull-right');
            hr.setAttribute('class', 'hrRight');
            span_name.textContent = "User";            
            direct_chat_text.textContent = document.getElementsByName('message')[0].value
            document.getElementsByName('message')[0].value = ""

            break;

        default:
            console.log('Sorry, we are out of ' + expr + '.');
    }

    //adicionando a barra de separação a cada mensagem do chat.
    //adicionando as horas no inicio do div_dialog
    //direct_chat_text.appendChild(span_time);
    direct_chat_info.appendChild(span_name);
    div_dialog[0].appendChild(span_time);  
    div_dialog[0].appendChild(direct_chat_msg);
    div_dialog[0].appendChild(hr);
    direct_chat_msg.appendChild(direct_chat_info);    
    direct_chat_msg.appendChild(direct_chat_text);

    var objDiv = document.getElementsByClassName("direct-chat-messages");
    objDiv[0].scrollTop = objDiv[0].scrollHeight;

    //Exibição do texto que o BOT está online
    document.getElementById("text-status").innerText = " ";
}

function runScript(e) {
    if (e.keyCode == 13) {
        Detect_Intent();
        return false;
    }

    if (e.keyCode == 10) {
        input_user = document.getElementsByName('message')[0].value;
        document.getElementsByName('message')[0].value = input_user + '\n';
        return false;
    }
}

function Detect_Intent() {
    var user_input = document.getElementsByName('message')[0].value;
    var room = document.getElementsByName('token')[0].value;

    if (user_input != "") {
        SendMessage("User", user_input);
        document.getElementsByName('message')[0].value = "";

        //Exibição do texto que o BOT está digitando
        document.getElementById("text-status").innerHTML = "digitando <img src='../static/assets/pointers.gif' width='40' />";

        $.post("../intent/",
            {
                data: user_input,
                session: room
            },
            function (data, status) {
                SendMessage("Bot", data);
            }
        );
    }
}

function Button_Intent(text) {
    document.getElementsByName('message')[0].value = text;
    Detect_Intent();
}