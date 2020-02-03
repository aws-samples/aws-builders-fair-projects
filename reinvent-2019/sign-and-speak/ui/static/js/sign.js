///AWS Account Settings
var app_credentials = { // TODO: Get the details from IAM User "s2sclientuser" 
    accessKeyId: '',//TODO: Update the accesskeyid..
    secretAccessKey: '' //TODO: Update this secretAccessKey
  };
var app_region = 'ap-southeast-2'; //TODO:  Set the region as required


var s3Bucket = "signs-data-cf";
var s3Key = "02_app/upload/RecordedSign.webm";

AWS.config.update({credentials: app_credentials, region: app_region});
var s3 = new AWS.S3();

var video;
var recorder;

var videoConstraints = {
    video: true ,
    audio: false
};

var initialized = false;

$(document).ready(function() 
{ 
    document.getElementById("imgSignGrid").style.visibility ="hidden";
    video = document.getElementById('videoplayer');
    s3 = new AWS.S3();

    document.getElementById('btn-start-recording').onclick = function() {
        this.disabled = true;
        showRecVideo();
        
    if(initialized == false) 
    {
        //Set Recorder for first time
        captureCamera(function(camera) {
            video.muted = true;
            video.volume = 0;
            video.srcObject = camera;
            recorder = RecordRTC(camera, {
                type: 'video'
            });    
            recorder.startRecording();
            // release camera on stopRecording
            recorder.camera = camera;
            document.getElementById('btn-stop-recording').disabled = false;            
        });

        initialized = true;
    }
    else
    {
        recorder.startRecording();
        document.getElementById('btn-stop-recording').disabled = false;  
    }
       
        
    };

    document.getElementById('btn-stop-recording').onclick = function() {
        this.disabled = true;
        
        recorder.stopRecording(stopRecordingCallback);
        document.getElementById('btn-start-recording').disabled = false;
    };
});

function captureCamera(callback) {    
    navigator.mediaDevices.getUserMedia(videoConstraints).then(function(camera) {    
       callback(camera);
   }).catch(function(error) {
       updateError('Unable to capture your camera. Please check console logs.');
       updateError(error);
   });
}
var vidblob = null;
function stopRecordingCallback() {
   vidblob = recorder.getBlob();
}

function uploadVideoToS3(videoToUpload, key)
{
    console.info("upload video to S3");
    
    document.getElementById("divSpinner").style.visibility="";
    
    try
    {
        var params = {   
        Body: videoToUpload,
        Bucket: s3Bucket,        
        Key: key,
        ServerSideEncryption: "AES256",        
       };

        s3.putObject(params, function(err, data) {            
            if (err) 
            updateError(err +  err.stack); // an error occurred            
        });    
    }
    catch(e)
    {
        updateError("error encountered  : " + e );
    }
}

$('#btn-send-sign').click(function () {
    uploadVideoToS3(vidblob,s3Key);
    document.getElementById("imgSignGrid").style.visibility ="";    
});




function showRecVideo()
{
    var vidplayer = document.getElementById("videoplayer");
    var secvidplayer = document.getElementById("sec-videoplayer");
    
    vidplayer.className = "";
    secvidplayer.className = "d-none";
}

function updateInfo(message)
{
    var node = document.createElement("li");                 
    node.className = "alert-info";
    var textnode = document.createTextNode("INFO : " + message);      
    node.appendChild(textnode);                              
    document.getElementById("messages").appendChild(node); 
}
function updateError(message)
{
    console.error(message);
    var node = document.createElement("li");                
    node.className = "alert-warning";
    var textnode = document.createTextNode("ERROR : " + message);
    node.appendChild(textnode);                              
    document.getElementById("messages").appendChild(node); 
}