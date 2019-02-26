

fetch('http://localhost:5000/data')
.then((resp) => {
  return resp.json()
})
.then( (data) => {
    data = JSON.parse(data)
    graph(data)
})


var margin,
  w, h,width,
  xScale, yScale,
  xAxis, yAxis, 
  context,waveGraph,
  zoom, 
  appendedYAxis,appendedXAxis;
const graph = (graphData) => {
  console.log('inside graph method', graphData)
  
  // select svg that will have graph. 
  waveGraph = d3.select('#waveGraph');
  // reset button. On click call resetted
  // which will revert back to orginal graph. 
  resetBtn = d3.select('#resetBtn')
      .on("click",resetted);
  
  margin = {top:20, right: 20, bottom: 30, left: 40};
  width = 960;
  w = width - margin.left - margin.right;
  h = +waveGraph.attr("height") - margin.top - margin.bottom;
  
  var parseDate = d3.timeParse("%m/%d/%Y %H:%M");
  
  // set range to be as width and high as graph. 
  xScale = d3.scaleLinear().range([0,w]);
  yScale = d3.scaleLinear().range([h,0]);

  // XAxis and YAxis ticks stuff
  xAxis = d3.axisBottom(xScale)
  .ticks(8).tickPadding(8);
  yAxis = d3.axisLeft(yScale)
  .ticks(8).tickPadding(8);
  
  // make the zoom var and when it is called
  // then it will call the function zoomed
  zoom = d3.zoom()
  .scaleExtent([1, Infinity])
  .translateExtent([[0, 0], [w, h]])
  .extent([[0, 0], [w, h]])
  .on("zoom", zoomed);
  
  // create the Wave line
  var WaveLine = d3.line()
  .curve(d3.curveMonotoneX) 
  .x((d) => { return xScale(d.xValue);})
  .y((d) => { return yScale(d.yValue);});

  
  
  waveGraph.append("def").append("clipPath")
  .attr("id", "clip")
  .append("rect")
  .attr("width", w)
  .attr("height",h);
  
  // focus
  mainG = waveGraph.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .attr("clip-path", "url(#clip)");
     
  
  // draw the graph.
  function draw(data) {
      // to get the domain lets loop though and add all values to the data.
      data.forEach(function(d) {
          d.yValue = +d.yValue;
          d.xValue = parseDate(d.xValue);
      });
      // set domain to be max and mins of values.
      xScale.domain([d3.min(data,(d)=> {
          return Math.min(d.yValue);
      }),
      d3.max(data, (d) => {
          return Math.max(d.yValue);
      })
      ]);
      yScale.domain([d3.min(graphData, (d) => {
          // take the lower of the lower value
          return Math.min(d.xValue) - 1;
      }),
      d3.max(graphData, (d) => {
          // take the higher of the higher value
          return Math.max(d.xValue) + 1;
      })
      ]);


      // draw the wave line onto the graph
      mainG.append("path")
          .datum(data)
          .attr("class", "line")
          .style('fill','none')
          .style('stroke','purple')
          .style('stroke-width', '1px')
          .attr("d", WaveLine(data));


      // add y axis 
      appendedYAxis = mainG.append('g')
      .attr('class', 'axis axis--y')
      .call(yAxis);

      // add x axis
      appendedXAxis = mainG.append('g')
      .attr('class', 'axis axis--x')
      .attr("transform", "translate(0," + h + ")")
      .call(xAxis);


      waveGraph.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .append("rect")
      .attr("class", "zoom")
      .attr("width", w)
      .attr("height", h)
      .call(zoom);

  }

  // first time we draw the graph!
  draw(graphData);

  function zoomed() {
      const t = d3.event.transform;
      var newXScale = t.rescaleX(xScale);
      var newYScale = t.rescaleY(yScale);
      //rescale x values and redraw the x axis then append the
      // x axis to the graph. Same for y axis
      appendedXAxis.call(xAxis.scale(newXScale));
      appendedYAxis.call(yAxis.scale(newYScale));
      
      const newWaveLine = d3.line()
          .curve(d3.curveMonotoneX)
          .x((d) => {return newXScale(d.xValue);})
          .y((d) => {return newYScale(d.yValue);});
      

      mainG.selectAll(".line")
          .attr("d", newWaveLine);
        
        console.log(zoom);
      
      // TO DO
      // fetch for the zoomed portion of the data

      // fetch('/data?x=t.x&y=t.y&k=t.k' )
          // .then()
          // .then(
          //     // replot with updated data
          // )
      
  }

     
  
  // this resets the graph to the normal size. By zooming out on the 
  // svg graph. 
  function resetted(){
      waveGraph.transition()
      .duration(750)
      .call(zoom.transform,d3.zoomIdentity);
  }
};

// logs the amount of time it takes to load the page.
window.onload = function () {
  var loadTime = window.performance.timing.domContentLoadedEventEnd-window.performance.timing.navigationStart; 
  // timing is in milliseconds so divide by 1000 to get seconds. 
  console.log('Page load time is '+ (loadTime/1000));
}
