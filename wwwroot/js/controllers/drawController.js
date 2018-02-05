app.controller('DrawController', ['DrawService', function(drawService) {
    var drawCtrl = this;
    drawCtrl.result = 0;
    drawCtrl.form = {
        deckSize: 60,
        targets: 10,
        drawn: 7
    };

    drawCtrl.calculate = function() {
        drawService.calculate(drawCtrl.form).then(function(response) {
            drawCtrl.result = response.data.result;
        });
    }
}]);