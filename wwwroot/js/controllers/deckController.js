app.controller('DeckController', ['DeckService', function(deckService) {
    var deckCtrl = this;
    deckCtrl.selectedDeck = {};
    deckCtrl.decks = [];

    deckCtrl.sum = function(items, prop){
        return items.reduce( function(a, b){
            return a + b[prop];
        }, 0);
    };
    deckCtrl.deckData = { pokemon: [], trainers: [], energy: []};

    deckCtrl.loadDeck = function() {
        deckService.getDeck(deckCtrl.selectedDeck.id).then(function(response) {
            deckCtrl.deckData = { pokemon: [], trainers: [], energy: []};
            var data = response.data;
            var pokemon = data.filter(function(item) { return item.type == 'Pok\u00e9mon' });
            var trainers = data.filter(function(item) { return item.type == 'Trainer' });
            var energy = data.filter(function(item) { return item.type == 'Energy' });

            deckCtrl.deckData.pokemon = pokemon;
            deckCtrl.deckData.trainers = trainers;
            deckCtrl.deckData.energy = energy;
        });
    };

    deckService.getDecks().then(function(response) {
        deckCtrl.decks = response.data
    });
}]);