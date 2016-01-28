function setDimensions() {
	var width = Math.min(document.documentElement.clientWidth-10,1024)
	var height = width * .75; 
	document.querySelector('video').setAttribute('width', width);
	document.querySelector('video').setAttribute('height', height)
}
function setVideoSource(video_date) {
	document.querySelector('video').setAttribute('poster', '/preview/' + video_date + '.gif')
	document.querySelector('source[type="video/mp4"]').setAttribute('src', 'video/' + video_date + '.mp4');
	document.querySelector('source[type="video/ogg"]').setAttribute('src', 'ogv/' + video_date + '.ogv');
	document.querySelector('video').load()
}
document.addEventListener("DOMContentLoaded", function(event) {
	setDimensions();
	if (!document.location.hash) {
		var d = new Date();
		var n = d.getUTCFullYear() + '-' + ("0" + (d.getUTCMonth() + 1)).slice(-2) + '-' + ("0" + d.getUTCDate()).slice(-2);
		setVideoSource(n)
	} else {
		setVideoSource(document.location.hash.substring(1))
	}
});
var resizeTimer;
window.onresize = function(event) {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function() {
	  setDimensions()            
  }, 100);
}