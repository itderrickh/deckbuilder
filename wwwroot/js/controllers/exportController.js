app.controller('ExportController', ['ExportService', '$timeout', '$window', function(exportService, $timeout, $window) {
    var exportCtrl = this;

    exportCtrl.deckText = '';
    exportCtrl.disableButton = true;
    exportCtrl.selectedDeck = {};
    exportCtrl.decks = [];
    exportCtrl.copyText = false;

    exportCtrl.onClip = function() {
        exportCtrl.copyText = true;

        $timeout(function() {
            exportCtrl.copyText = false;
        }, 3000);
    };

    exportCtrl.changeDeckText = function() {
        //Disable button
        exportCtrl.disableButton = true;

        //Load deck text
        exportService.getDeckList(exportCtrl.selectedDeck.id).then(function(response) {
            var text = response.data.text;

            exportCtrl.deckText = text;

            //Enable button
            if(exportCtrl.selectedDeck) {
                exportCtrl.disableButton = false;
            }
        });
    };

    exportCtrl.exportOfficial = function() {
        exportService.exportOfficial(exportCtrl.selectedDeck.id).then(function(response) {
            if(response.data.warnings.length > 0) {
                var output = '<ul>' + response.data.warnings.reduce(function(acc, item) {
                    return acc + "<li>" + item + "</li>"
                }, '') + '</ul>';
                swal("Warning!", output , "warning");
            }
            $window.open("http://localhost:5000/api/pdf/" + response.data.pdffile, '', 'height=650,width=840');
        });
    };

    exportService.getDecks().then(function(response) {
        exportCtrl.decks = response.data;
    });
}]);