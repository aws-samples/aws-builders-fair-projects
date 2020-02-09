var wsurl = "wss://abcdxyz.execute-api.ap-southeast-2.amazonaws.com/Prod"; //TODO: Put the CloudFormation Template Output value for S2SWebSocketURL 

$(document).ready(function() 
{ 
    WebSocketConnect();

    document.getElementById('btn-resetui').onclick = function() {
        $('#transcript').val('');
        transcription = '';
        document.getElementById("divtranscript").innerHTML = "";
        //document.getElementById("imgSignGrid").src = "";
    };
});

function WebSocketConnect() {
    
    
    if ("WebSocket" in window) {
       console.info("WS is supported by browser");
       
       // Let us open a web socket
       var ws = new WebSocket(wsurl);
        
       ws.onopen = function() {
        console.info("connection opened to WS");
          ws.send("Client is connected");          
          console.info("Client is connected");
       };
        
       ws.onmessage = function (evt) { 
        document.getElementById("divSpinner").style.visibility="hidden";
        //document.getElementById("imgSignGrid").src = "";        
          var received_msg = evt.data;
          console.info('msg recv from socket : ' + received_msg);
          updateMsgPanel( received_msg);
          
          //alert("Message is received...");
       };
        
       ws.onclose = function() { 
          
          // websocket is closed.
          console.info("connection closed to WS");
          alert("WS is closed. Refresh screen!!!");
          //alert("Connection is closed..."); 
       };
    } else {
      
       // The browser doesn't support WebSocket
       console.error("WS is not supported");
       alert("WebSocket NOT supported by your Browser!");
    }
}
function updateMsgPanel(messageData)
{
    //Message Format
    //isSign|confidence|Message
    //true|0.6358023881912231|Hello
    msgSplit = messageData.split("|");
    var sign = msgSplit[0];
    var conf = msgSplit[1];
    var msg = msgSplit[2]; 

    if(msg == undefined)
    {
        return;
    }

    var divnode = document.createElement("div");
    divnode.className = "alert alert-dark message"
    var spannode = document.createElement("span");
    var imageAction = document.createElement("img");
    imageAction.id="imgAction";
    var textnode;
    var linknode = document.createElement("a");
    if(sign == "true")
    {
        divnode.className = "alert alert-warning message"
        spannode.className = "badge badge-warning";
        spannode.innerText = "Auslan";                
        textnode = document.createTextNode( "  " + msg + " (Confidence: " + conf + ")");
    }
    else
    {
        divnode.className = "alert alert-dark message"
        spannode.className = "badge badge-dark";
        spannode.innerText = "English";        
        textnode = document.createTextNode( "  " + msg + " ( Amazon Transcribe )");         
    }
    
    divnode.appendChild(spannode);
    divnode.appendChild(textnode);   

    document.getElementById("divtranscript").appendChild(divnode);
}
