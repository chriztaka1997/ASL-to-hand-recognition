navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

navigator.mediaDevices.getUserMedia({audio: true, video: true}, function(s){
	console.log("Success. Found a stream media!!!");
	var video = document.querySelector('video');
	video.srcObject = s
	video.play();
}, function(e){
	console.log(e);
});