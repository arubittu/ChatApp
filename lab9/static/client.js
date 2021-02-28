const socket=io.connect("http://127.0.0.1:5000");
username=document.getElementsByTagName('h1')[0].innerHTML[2,-1];
    socket.on('connect',function(username){
        socket.emit('person',{username:`${username}`});

        let msg_input=document.getElementById('textfield');
        document.getElementById('form_msg').onsubmit=function(event){
            event.preventDefault();//dont fucking get/post
            let message=msg_input.value.trim();
            
            socket.emit('send_msg',{message:message,username:`${username}`});
        
            msg_input.value = '';
            msg_input.focus();
        }

    });

    socket.on('received_msg',function(data){
        console.log(data);
        let msg_toshow=data['message'];
        let name=data['username'];
        document.getElementById('chatspace').innerHTML+=`<p>${name}: ${msg_toshow}</p>`;

    });

    socket.on('person_connected',function(name){
        document.getElementById('chatspace').innerHTML+=`<p> ${name} has connected!</p>`;

    });

    socket.on('disconnect',function(){
        console.log('{{username}} has disconnected')
    });