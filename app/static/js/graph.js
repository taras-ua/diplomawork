function buildGraph(nodes, edges) {
    var container = document.getElementById('graph-canvas');
    var paths = '';
    for(i = 0; i < nodes.length; i++) {
        paths += nodes[i].id + '; ';
    }
    for(i = 0; i < edges.length; i++) {
        paths += edges[i].source + ' -> ' + edges[i].target;
        if(i != edges.length - 1) {
            paths += '; ';
        }
    }
    var data = {
        dot: 'dinetwork {node[shape=circle]; ' + paths + ' }'
    };
    var network = new vis.Network(container, data);
}