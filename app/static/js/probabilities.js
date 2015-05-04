function buildPlot(x, y, init_degree) {
    var container = document.getElementById('plot-canvas');
    var visDots = [];
    for(var j = 0; j < x.length; j++) {
        visDots.push({
            x: init_degree + x[j],
            y: y[j]
        });
    }
    var options = {
        width: '100%',
        height: '100%',
        start: init_degree + x[0],
        end: init_degree + x[x.length - 1],
        min: init_degree + x[0],
        max: init_degree + x[x.length - 1],
        showMajorLabels: false,
        drawPoints: {
            style: 'circle'
        },
        dataAxis: {
            title: {
                left: {
                    text: 'Probability'
                }
            }
        }
    };
    var data = new vis.DataSet(visDots);
    var graph2d = new vis.Graph2d(container, data, options);
}