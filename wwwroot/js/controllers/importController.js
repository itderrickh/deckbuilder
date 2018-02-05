app.controller('ImportController', ['ImportService', function(importService) {
    var importCtrl = this;
    importCtrl.tab = 1;

    importCtrl.form = {
        deckName: '',
        deckList: '',
        deckUrl: ''
    };

    importCtrl.importDeck = function() {
        importService.importDeck(importCtrl.form.deckName, importCtrl.form.deckList).then(function(response) {
            swal(
                'Completed!',
                'Your deck ' + importCtrl.form.deckName + ' has been successfully imported.',
                'success'
            )
        })
    };

    importCtrl.importFromLimitless = function() {
        importService.importFromLimitless(importCtrl.form.deckName, importCtrl.form.deckUrl).then(function(response) {
            swal(
                'Completed!',
                'Your deck ' + importCtrl.form.deckName + ' has been successfully imported.',
                'success'
            )
        })
    };

    //Setup the form autosize
    autosize(document.querySelector('textarea'));
}]);