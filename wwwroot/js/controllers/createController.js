app.controller('CreateController', ['CreateService', function(createService) {
    var createCtrl = this;
    createCtrl.searchField = "";
    createCtrl.name = '';
    createCtrl.largeUrl = '';
    createCtrl.count = {
        pokemon: 0,
        trainer: 0,
        energy: 0
    };

    createCtrl.searchData = {};
    createCtrl.deckData = [];

    createCtrl.newAdd = function(card) {
        createCtrl.deckData.push(card);
    };

    createCtrl.newRemove = function(card) {
        var index = createCtrl.deckData.indexOf(card);
        if(index > -1) {
            createCtrl.deckData.splice(index, 1);
        }
    };

    createCtrl.newSubmit = function() {
        var deck = [];
        for(var i = 0; i < createCtrl.deckData.length; i++) {
            deck.push(createCtrl.deckData[i]._source.Id);
        }
        
        createService.createDeck({
            'name': createCtrl.name,
            'deck': deck
        }).then(function(response) {
            swal(
                'Submitted!',
                'Your deck ' + createCtrl.name + ' has been submitted',
                'success'
            )
        });
    };

    createCtrl.form = {
        pokemon: { count: 0, name: '', setName: '', number: ''},
        trainer: { count: 0, name: '', setName: '', number: ''},
        energy: { count: 0, name: '', setName: '', number: ''}
    };

    createCtrl.cards = {
        pokemon: [],
        trainer: [],
        energy: []
    };

    createCtrl.search = function() {
        createService.search(createCtrl.searchField).then(function(response) {
            createCtrl.searchData = response.data;
        })
    };

    /*
    createCtrl.addCard = function(listName) {
        createCtrl.cards[listName].push(angular.copy(createCtrl.form[listName]));
        createCtrl.count[listName] += createCtrl.form[listName].count;
        createCtrl.form[listName] = { count: 0, name: '', setName: '', number: ''};
    };

    createCtrl.removeCard = function(listName, newCard) {
        var index = createCtrl.cards[listName].indexOf(newCard);
        if(index > -1) {
            createCtrl.count[listName] -= createCtrl.cards[listName][index].count;
            createCtrl.cards[listName].splice(index, 1);
        }
    };

    createCtrl.submitForm = function() {
        var count = createCtrl.count.pokemon + createCtrl.count.trainer + createCtrl.count.energy
        if(count < 60) {
            swal({
                title: 'Are you sure?',
                text: "The deck has less than 60 cards!",
                type: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, submit anyways!',
                cancelButtonText: 'No, cancel!',
                confirmButtonClass: 'btn btn-success',
                cancelButtonClass: 'btn btn-danger',
                buttonsStyling: false,
                reverseButtons: true
            }).then(function(result) {
                if (result.value) {
                    debugger;
                    var deck = createService.prepareDeck(createCtrl.cards);

                    createService.createDeck({
                        'name': createCtrl.name,
                        'deck': deck
                    }).then(function(response) {
                        swal(
                            'Submitted!',
                            'Your deck ' + createCtrl.name + ' has been submitted',
                            'success'
                        )
                    });

                }
            })
        } else {
            var deck = createService.prepareDeck(createCtrl.cards);

            createService.createDeck({
                'name': createCtrl.name,
                'deck': deck
            }).then(function(response) {
                alert('Completed');
            });
        }
    };*/
}]);