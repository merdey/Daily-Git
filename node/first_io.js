var fs = require('fs');
var filename = process.argv[2];
var buffer = fs.readFileSync(filename);
var str = buffer.toString()
var lines = str.split('\n');
console.log(lines.length - 1);
