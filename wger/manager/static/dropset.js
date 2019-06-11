let setNumber = $('#id_sets').val();
let WeightVal = $('#weight-num').val();
let cycleNum = Number($('#cycle-num').val());
let id = $('input.form-control')[4].id;
let exerciseNo = id.replace(/^\D+|\D.*$/g, '');
let cyclesId = '';
let weightId = '';
let cycleClass = '';
let percentageSet = null;

let blockButton = () => {
    $('#hide-btn').css({"display": "none"});
    $('#grey-btn').css({"display": "block"});
    $('#warn-message-id').css({"display": "block"})
    
}
let showButton = () => {
    $('#hide-btn').css({"display": "block"});
    $('#grey-btn').css({"display": "none"});
    $('#warn-message-id').css({"display": "none"})
}

/**
 * Toggles the view for drop set calculation
 */
function revealSettings(){
    let setCheck = $("#set-check")[0];
    setCheck.checked ? $('.set-items').css({"display": "block"}) :
        $('.set-items').css({"display": "none"});
}

/**
 * Gets value of cycles from form
 * @param {number} value value of input value for cycles
 */
function setCycle(value) {
    cycleNum = Number(value)
    cycleNum <=0 ? blockButton() : showButton();
}

/**
 * Gets value of weight from form
 * @param {number} value value of input value for weight
 */
function setWeight(value) {
    WeightVal = value;
    WeightVal <=9 ? blockButton() : showButton();
}

/**
 * Calculates the drop sets
 */
function calcDrops() {
    let percentageSet = $('#percentage-change').val();
    if (cycleNum && WeightVal) {
        for (let i = 0; i <= setNumber; i++) {
            cyclesId = 'id_exercise' + exerciseNo + '-' + i + '-reps';
            weightId = 'id_exercise' + exerciseNo + '-' + i + '-weight';
            $('#' + weightId)[0].value = parseFloat(WeightVal).toFixed(0);
            $('#' + cyclesId)[0].value = cycleNum;
            WeightVal -= WeightVal * (percentageSet/100)
            cycleNum += 6
        }
    }
}
