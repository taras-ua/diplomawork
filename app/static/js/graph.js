function buildGraph(graph) {
    var container = document.getElementById('graph-canvas');
    var paths = '';
    for(var i = 0; i < graph.links.length; i++) {
        paths += graph.links[i].source + ' -> ' + graph.links[i].target;
        if(i != graph.links.length - 1) {
            paths += '; ';
        }
    }
    var data = {
        dot: 'dinetwork {node[shape=circle]; ' + paths + ' }'
    };
    var network = new vis.Network(container, data);
}