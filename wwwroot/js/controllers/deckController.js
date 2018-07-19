app.controller('DeckController', ['DeckService', function(deckService) {
    var deckCtrl = this;
    deckCtrl.selectedDeck = {};
    deckCtrl.decks = [];
    deckCtrl.imageShow = false;

    deckCtrl.sum = function(items, prop){
        return items.reduce( function(a, b){
            return a + b[prop];
        }, 0);
    };
    deckCtrl.deckData = { pokemon: [], trainers: [], energy: []};

    deckCtrl.imageDeckList = function() {
        var megaList = [];//.concat(deckCtrl.deckData.pokemon,deckCtrl.deckData.trainers,deckCtrl.deckData.energy);

        for(var a = 0; a < deckCtrl.deckData.pokemon.length; a++) {
            for(var a1 = 0; a1 < deckCtrl.deckData.pokemon[a].count; a1++) {
                megaList.push(deckCtrl.deckData.pokemon[a]);
            }
        }

        for(var b = 0; b < deckCtrl.deckData.trainers.length; b++) {
            for(var b1 = 0; b1 < deckCtrl.deckData.trainers[b].count; b1++) {
                megaList.push(deckCtrl.deckData.trainers[b]);
            }
        }

        for(var c = 0; c < deckCtrl.deckData.energy.length; c++) {
            for(var c1 = 0; c1 < deckCtrl.deckData.energy[c].count; c1++) {
                megaList.push(deckCtrl.deckData.energy[c]);
            }
        }

        return megaList;
    };

    deckCtrl.getNumber = function(num) {
        return new Array(num);
    }

    deckCtrl.loadDeck = function(showImage) {
        deckCtrl.imageShow = showImage;
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