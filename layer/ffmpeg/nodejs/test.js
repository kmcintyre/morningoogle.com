#!/usr/bin/env node
// Converts a saved Chrome dev tools recording with Screenshots to mp4
const fs = require('fs');
const path = require('path');
const spawn = require('child_process').spawn;
const FPS = 60;
const MICROSEC_PER_FRAME = Math.round(1000000 / FPS);
if (process.argv.length < 3) {
  console.log(`node ${path.relative('.', process.argv[1])} [DevToolsProfile]`);
  process.exit(1);
}
let traceFile = path.resolve(process.argv[2]);
console.log('tracefile:', traceFile)
let trace = JSON.parse(fs.readFileSync(traceFile))['traceEvents'];
console.log('trace:', typeof trace)
trace = trace.filter(event => event.name === "Screenshot").sort((a, b) => a.ts - b.ts);
if (trace.length === 0) {
  console.log('Trace was not recorded with Screenshots. Ensure Screenshots is checked before recording.')
  process.exit(1);
}
let { name } = path.parse(traceFile);
let ffmpeg = spawn("ffmpeg", [
  "-r", `${FPS}`,
  "-f", "image2pipe",
  "-i", "pipe:",
  "-vcodec", "libx264",
  "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
  `${name}.mp4`
], {
  stdio: ['pipe', 'inherit', 'inherit']
});
let buffer;
let target = trace[0].ts;
for (let i = 0; i < trace.length; i++) {
  let event = trace[i];
  // repeat last frame until caught up
  while (target < event.ts) {
    console.log('hey');
    ffmpeg.stdin.write(buffer);
    target += MICROSEC_PER_FRAME;
  }
  console.log('hey2');
  buffer = Buffer.from(event.args.snapshot, "base64");
  ffmpeg.stdin.write(buffer);
  target += MICROSEC_PER_FRAME;
}
ffmpeg.stdin.end();
