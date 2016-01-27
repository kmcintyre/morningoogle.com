function setDimensions() {
	var width = Math.min(document.documentElement.clientWidth,1024)
	var height = width * .75; 
	document.querySelector('video').setAttribute('width', width);
	document.querySelector('video').setAttribute('height', height)
}
function setVideoSource() {
	var d = new Date();
	var n = d.getUTCFullYear() + '-' + ("0" + (d.getUTCMonth() + 1)).slice(-2) + '-' + ("0" + d.getUTCDate()).slice(-2);
	document.querySelector('video').setAttribute('poster', '/preview/' + n + '.gif')
}
document.addEventListener("DOMContentLoaded", function(event) {
	setDimensions();
	setVideoSource()
});
var resizeTimer;
window.onresize = function(event) {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(function() {
	  setDimensions()            
  }, 100);
}