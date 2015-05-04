const ANIMATION_SPEED = 300;

function modelChanged() {
    var ddlModel = document.getElementById("id_model");
    var model = ddlModel.options[ddlModel.selectedIndex].value;
    var numSubnodes = document.getElementById("id_subnodes");
    var numProbability = document.getElementById("id_probability");
    if(model == 'bollobas-riordan' || model == 'new-model') {
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

function probabilityChanged() {
    var ddlProb = document.getElementById("id_spec");
    var prob = ddlProb.options[ddlProb.selectedIndex].value;
    var degreeVal = document.getElementById("id_degree");
    if(prob == 'degree') {
        $('#degree-group').show(ANIMATION_SPEED);
        degreeVal.required = true;
    } else {
        $('#degree-group').hide(ANIMATION_SPEED);
        degreeVal.required = false;
    }
}

function launchSpinner(id) {
    $('#'+id).show();
}

$(function() {
    modelChanged();
    probabilityChanged();
});