let setNumber = $('#id_sets').val();
let WeightVal = $('#weight-num').val();
let cycleNum = Number($('#cycle-num').val());
let id = $('input.form-control')[4].id;
let exerciseNo = id.replace(/^\D+|\D.*$/g, '');
let cyclesId = '';
let weightId = '';
let cycleClass = '';
let percentageSet = null;
let blockButton = () => $('#hide-btn').css({"display": "none"});
let showButton = () => $('#hide-btn').css({"display": "block"});

function setCycle(value) {
    cycleNum = Number(value)
    cycleNum <=0 ? blockButton() : showButton();
}
function setWeight(value) {
    WeightVal = value;
    WeightVal <=9 ? blockButton() : showButton();
}
function calcDrops() {
    percentageSet = $('#percentage-change').val();
    if (cycleNum && WeightVal) {
        for (let i = 0; i <= setNumber; i++) {
            cyclesId = 'id_exercise' + exerciseNo + '-' + i + '-reps';
            weightId = 'id_exercise' + exerciseNo + '-' + i + '-weight';
            document.getElementById(weightId).value = parseFloat(WeightVal).toFixed(0);
            document.getElementById(cyclesId).value = cycleNum;
            WeightVal -= WeightVal * (percentageSet/100)
            cycleNum += 6
        }
    }
}
