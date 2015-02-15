function buildGraph(graph) {
    var width = $(window).width(),
        height = $(window).height();

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(200)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var marker = svg.append("marker")
        .attr("id", "markerArrow")
        .attr("markerWidth", "13")
        .attr("markerHeight", "13")
        .attr("refx", "2")
        .attr("refy", "6")
        .attr("orient", "auto");

    marker.append("path")
        .attr("d", "M2,2 L2,11 L10,6 L2,2")
        .style("fill", "#999");

    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("path")
        .attr("class", "link")
        .style("stroke-width", function(d) { return Math.sqrt(d.value); })
        .style("marker-end", "url(#markerArrow)");

    var node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .style("fill", function(d) { return color(d.group); })
        .call(force.drag);

    node.append("title")
        .text(function(d) { return d.name; });

    force.on("tick", function() {
        link.attr("d", function(d) {
            return "M " + d.source.x + " " + d.source.y + " L " + d.target.x + " " + d.target.y;
        });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });

}