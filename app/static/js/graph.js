function buildGraph(nodes, edges) {
    var container = document.getElementById('graph-canvas');
    var visEdges = [];
    var visNodes = [];
    for(var j = 0; j < nodes.length; j++) {
        visNodes.push({
            id: nodes[j].id,
            label: nodes[j].id.toString()
        });
    }
    for(var i = 0; i < edges.length; i++) {
        visEdges.push({
            from: edges[i].source,
            to: edges[i].target,
            style:'arrow',
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