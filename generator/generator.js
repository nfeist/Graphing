// if you want more data then change
// the value of n.
var n = 10;
var c = Math.random()*100;

// creates to column for a xValue and yValue
console.log("xValue,yValue");

for(var i=0 ; i<n ; i++){
    console.log(i + "," + c);
    c += (Math.random()*2)-1;
}