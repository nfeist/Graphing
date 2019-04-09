
function debounce(func, wait, immediate) {
  var timeout;

  // This is the function that is actually executed when
  // the DOM event is triggered.
  return function executedFunction() {
    // Store the context of this and any
    // parameters passed to executedFunction
    var context = this;
    var args = arguments;
      
    // The function to be called after 
    // the debounce time has elapsed
    var later = function() {
      // null timeout to indicate the debounce ended
      timeout = null;
      
      // Call function now if you did not on the leading end
      if (!immediate) func.apply(context, args);
    };

    // Determine if you should call the function
    // on the leading or trail end
    var callNow = immediate && !timeout;
  
    // This will reset the waiting every function execution.
    // This is the step that prevents the function from
    // being executed because it will never reach the 
    // inside of the previous setTimeout  
    clearTimeout(timeout);
  
    // Restart the debounce waiting period.
    // setTimeout returns a truthy value (it differs in web vs node)
    timeout = setTimeout(later, wait);
  
    // Call immediately if you're dong a leading
    // end execution
    if (callNow) func.apply(context, args);
  };
};


fetch('http://localhost:5000/data')
  .then((resp) => {
    return resp.json()
  })
  .then( (data) => {
      data = JSON.parse(data)
      // data.lttb 
      // data.min_max

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

  // removing everthing from the graph
  waveGraph.selectAll('*').remove();

  // reset button. On click call resetted
  // which will revert back to orginal graph. 
  resetBtn = d3.select('#resetBtn')
      .on("click",resetted);
  
  margin = {top:20, right: 20, bottom: 30, left: 40};
  width = 960;
  w = width - margin.left - margin.right;
  h = +waveGraph.attr("height") - margin.top - margin.bottom;
    
  // set range to be as width and high as graph. 
  xScale = d3.scaleLinear().range([0,w]);
  yScale = d3.scaleLinear().range([h,0]);

  newXScale = xScale;
  newYScale = yScale;

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
  .x((d) => { return xScale(d[0]);})
  .y((d) => { return yScale(d[1]);});

  
  
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
        d[1] = +d[1];
        d[0] = +d[0];
    });
    // set domain to be max and mins of values.
    xScale.domain([d3.min(data,(d)=> {
        return Math.min(d[0]);
    }),
    d3.max(data, (d) => {
        return Math.max(d[0])+ 1;
      })
    ]);
    yScale.domain([d3.min(graphData, (d) => {
        // take the lower of the lower value
        return Math.min(d[1]) - 1;
    }),
    d3.max(graphData, (d) => {
        // take the higher of the higher value
        return Math.max(d[1]) + 1;
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

  newdata = graphData;

  function redraw(data) {
    const newWaveLine = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => {return newXScale(d[0])})
      .y((d) => {return newYScale(d[1])});

    mainG.selectAll(".line")
        .attr("d", newWaveLine(data))
  }

  function fetchData(zoomReq) {  
    // fetch for the zoomed portion of the data
    fetch(zoomReq)
      .then( (resp) => { 
        return resp.json()
      })
      .then((nd) => {
        newdata = JSON.parse(nd)
        redraw(newdata);
      })
  }

  // debounce the zoom function to help performance time
  const debouncedDataFetch = debounce(fetchData, 50)

  function zoomed() {

    const t = d3.event.transform;
    const zoomLevel = d3.event.transform.k;
    newXScale = t.rescaleX(xScale);
    newYScale = t.rescaleY(yScale);
    //rescale x values and redraw the x axis then append the
    // x axis to the graph. Same for y axis
    appendedXAxis.call(xAxis.scale(newXScale));
    appendedYAxis.call(yAxis.scale(newYScale));

    var xmin = Math.floor(newXScale.domain()[0]);
    var xmax = Math.ceil(newXScale.domain()[1]);

    const newWaveLine = d3.line()
      .curve(d3.curveMonotoneX)
      .x((d) => {return newXScale(d[0])})
      .y((d) => {return newYScale(d[1])});

    mainG.selectAll(".line")
      .attr("d", newWaveLine(newdata))

    var zoomReq = 'http://localhost:5000/zoom_data?width='
      +w+'&zoom_level='+zoomLevel+'&x_min='+xmin+'&x_max='+xmax;

    // fetch for the zoomed portion of the data
    debouncedDataFetch(zoomReq)
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
