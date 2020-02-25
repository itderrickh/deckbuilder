app.controller('ImportController', ['ImportService', function(importService) {
    var importCtrl = this;
    importCtrl.tab = 1;
    importCtrl.sprites = ['001'];

    importCtrl.addSprite = function() {
        importCtrl.sprites.push('001');
    }

    importCtrl.selectSprite = function(index, sprites) {
        importCtrl.sprites[index] = sprites;
    };

    importCtrl.form = {
        deckName: '',
        deckList: '',
        deckUrl: ''
    };

    importCtrl.importDeck = function() {
        importService.importDeck(importCtrl.form.deckName, importCtrl.form.deckList, importCtrl.sprites).then(function(response) {
            swal(
                'Completed!',
                'Your deck ' + importCtrl.form.deckName + ' has been successfully imported.',
                'success'
            )
        })
    };

    importCtrl.importFromLimitless = function() {
        importService.importFromLimitless(importCtrl.form.deckName, importCtrl.form.deckUrl, importCtrl.sprites).then(function(response) {
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