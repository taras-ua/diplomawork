const ANIMATION_SPEED = 300;

function modelChanged() {
    var ddlModel = document.getElementById("id_model");
    var model = ddlModel.options[ddlModel.selectedIndex].value;
    var numSubnodes = document.getElementById("id_subnodes");
    var numProbability = document.getElementById("id_probability");
    if(model == 'bollobas-riordan') {
        $('#subnodes-group').show(ANIMATION_SPEED);
        numSubnodes.required = true;
    } else {
        $('#subnodes-group').hide(ANIMATION_SPEED);
        numSubnodes.required = false;
    }
    if(model == 'simple') {
        $('#probability-group').show(ANIMATION_SPEED);
        numProbability.required = true;
    } else {
        $('#probability-group').hide(ANIMATION_SPEED);
        numProbability.required = false;
    }
}

$(function() {
   modelChanged();
});