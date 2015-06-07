var currentGraph;
var currentDistribution;

function saveGraph(nodes, edges, directed) {
    currentGraph = {
        nodes: nodes,
        edges: edges,
        directed: directed
    }
}

function saveDistribution(degrees, fractions, degree_by_node, subnodes) {
    currentDistribution = {
        degrees: degrees,
        fractions: fractions,
        degreebynode: degree_by_node,
        subnodes: subnodes
    }
}

function buildDistribution() {
    $('#degree-canvas').find('button').hide();
    const lambda = 2.3;
    var x = currentDistribution.degrees;
    var y = currentDistribution.fractions;
    var container = document.getElementById('degree-canvas');
    var items = [];
    var allMultiplied = 1;
    for(var i = 0; i < x.length; i++) {
        allMultiplied *= Math.pow(x[i], lambda);
    }
    var combinationsOfFractions = 0;
    for(var j = 0; j < x.length; j++) {
        if(x[j] >= currentDistribution.subnodes) {
            combinationsOfFractions += allMultiplied / Math.pow(x[j], lambda);
        }
    }
    var c_constant = allMultiplied / combinationsOfFractions;
    for(var k = 0; k < x.length; k++) {
        items.push({
            x: x[k],
            y: y[k],
            group: 0
        });
        if(x[k] >= currentDistribution.subnodes) {
            items.push({
                x: x[k],
                y: c_constant / Math.pow(x[k], lambda),
                group: 1
            });
        }
    }
    var options = {
        width: '100%',
        height: '100%',
        start: x[0],
        end: x[x.length - 1],
        min: x[0],
        max: x[x.length - 1],
        showMajorLabels: false,
        dataAxis: {
            title: {
                left: {
                    text: 'Probability'
                }
            }
        }
    };
    var optionsApprox = {
        drawPoints: {
            style: 'circle'
        }
    };
    var optionsReal = {
        style: 'bar'
    };
    var groups = new vis.DataSet();
    groups.add({
        id: 0,
        content: 'Real data',
        options: optionsReal
    });
    groups.add({
        id: 1,
        content: 'Approximate data',
        options: optionsApprox
    });
    var data = new vis.DataSet(items);
    var graph2d = new vis.Graph2d(container, data, groups, options);
}

function buildGraph() {
    $('#graph-canvas').find('button').hide();
    var nodes = currentGraph.nodes;
    var edges = currentGraph.edges;
    var directed = currentGraph.directed;
    var container = document.getElementById('graph-canvas');
    var visEdges = [];
    var visNodes = [];
    for(var j = 0; j < nodes.length; j++) {
        var notDead = (currentDistribution.degreebynode[nodes[j].id] > 0);
        visNodes.push({
            id: nodes[j].id,
            label: nodes[j].id.toString(),
            color: {
                border: notDead ? '#2B7CE9' : '#DE5050',
                background: notDead ? '#86B3FB' : '#FF9191',
                highlight: {
                    border: notDead ? '#5292E9' : '#F22929',
                    background: notDead ? '#C8DEFF' : '#FCC7C7'
                }
            }
        });
    }
    for(var i = 0; i < edges.length; i++) {
        visEdges.push({
            from: edges[i].source,
            to: edges[i].target,
            style: directed > 0 ? 'arrow' : 'line',
            length: edges[i].source == edges[i].target ? 50 : visNodes.length * 30
        });
    }
    var data = {
        nodes: visNodes,
        edges: visEdges
    };
    var options = {
        width: '100%',
        height: '100%'
    };
    var network = new vis.Network(container, data, options);
}