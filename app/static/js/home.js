const ANIMATION_SPEED = 300;

function modelChanged() {
    var ddlModel = document.getElementById("id_model");
    var model = ddlModel.options[ddlModel.selectedIndex].value;
    var numSubnodes = document.getElementById("id_subnodes");
    var numInitWeight = document.getElementById("id_initial_weight");
    var numForgetCoef = document.getElementById("id_forget_coef");
    var numProbability = document.getElementById("id_probability");
    if(model == 'bollobas-riordan' || model == 'new-model') {
        $('#subnodes-group').show(ANIMATION_SPEED);
        numSubnodes.required = true;
        $('#initial_weight-group').show(ANIMATION_SPEED);
        numInitWeight.required = true;
    } else {
        $('#subnodes-group').hide(ANIMATION_SPEED);
        numSubnodes.required = false;
        $('#initial_weight-group').hide(ANIMATION_SPEED);
        numInitWeight.required = false;
    }
    if(model == 'new-model') {
        $('#forget_coef-group').show(ANIMATION_SPEED);
        numForgetCoef.required = true;
    } else {
        $('#forget_coef-group').hide(ANIMATION_SPEED);
        numForgetCoef.required = false;
    }
    if(model == 'erdos-renyi') {
        $('#probability-group').show(ANIMATION_SPEED);
        numProbability.required = true;
    } else {
        $('#probability-group').hide(ANIMATION_SPEED);
        numProbability.required = false;
    }
}

function launchSpinner(id) {
    $('#'+id).show();
}

function handleName(initials) {
    $("#img-"+initials)
        .mouseenter(function() {
            $("#name-"+initials).animate({
                opacity: 1
            }, {
                duration: ANIMATION_SPEED
            });
        })
        .mouseleave(function() {
            $("#name-"+initials).animate({
                opacity: 0
            }, {
                duration: ANIMATION_SPEED
            });
        });
}

$(function() {
    modelChanged();
    $('#form-build').validator().on('submit', function (e) {
        if (!e.isDefaultPrevented()) {
            launchSpinner('build');
        }
    });
    handleName('is');
    handleName('tr');
});