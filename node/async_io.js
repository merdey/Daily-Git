var fs = require('fs');
var filename = process.argv[2];
fs.readFile(filename, function(err, contents) {
    var lines = contents.toString().split('\n').length - 1;
    console.log(lines)
})
