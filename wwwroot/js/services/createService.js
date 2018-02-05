app.service('CreateService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        createDeck: function(data) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/deck/bulk',
                data: data,
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        prepareDeck: function(cards) {
            var deck = [];
            for(var p in cards.pokemon) {
                var pcard = cards.pokemon[p];
                pcard.type = 'Pok\u00e9mon';
                deck.push(pcard);
            }

            for(var t in cards.trainer) {
                var tcard = cards.trainer[t];
                tcard.type = 'Trainer Cards';
                deck.push(tcard);
            }

            for(var e in cards.energy) {
                var ecard = cards.energy[e];
                ecard.type = 'Energy';
                deck.push(ecard);
            }

            return deck;
        }
    }
}]);