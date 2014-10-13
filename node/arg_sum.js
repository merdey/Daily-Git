var sum = 0;

process.argv.forEach(function(item) {
    sum += +item ? +item : 0;
});

console.log(sum);
