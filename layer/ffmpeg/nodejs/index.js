const fs = require('fs');
const spawn = require('child_process').spawn;
//const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path;

const FPS = 60;
const MICROSEC_PER_FRAME = Math.round(1000000 / FPS);
const FILM = '/home/kebin70/filmstrip.mp4';

let event = JSON.parse(fs.readFileSync('/home/kebin70/trace.json'))['traceEvents'].filter(event => event.name === "Screenshot").sort((a, b) => a.ts - b.ts)

let ffmpeg = spawn("ffmpeg", [
  "-r", `${FPS}`,
  "-f", "image2pipe",
  "-i", "pipe:",
  "-vcodec", "libx264",
  `${FILM}`
], {
  stdio: ['pipe', 'inherit', 'inherit']
});
let target = event[0].ts;
for (let i = 0; i < event.length; i++) {
  try {
    while (target < event[i].ts) {
      ffmpeg.stdin.write(buffer);
      target += MICROSEC_PER_FRAME;
    }
    //console.log('here2', target)
    buffer = Buffer.from(event[i].args.snapshot, "base64");
    ffmpeg.stdin.write(buffer);
    target += MICROSEC_PER_FRAME;
  } catch (err) {
    console.log('error:', err);
  }
}
//ffmpeg.stdin.end();
console.log('done')
