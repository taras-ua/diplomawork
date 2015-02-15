const ANIMATION_SPEED = 100;

function modelChanged() {
    var ddlModel = document.getElementById("id_model");
    var model = ddlModel.options[ddlModel.selectedIndex].value;
    var numSubnodes = document.getElementById("id_subnodes");
    if(model == 'bollobas-riordan') {
        $('#subnodes-group').show(ANIMATION_SPEED);
        numSubnodes.required = true;
    } else {
        $('#subnodes-group').hide(ANIMATION_SPEED);
        numSubnodes.required = false;
    }
}