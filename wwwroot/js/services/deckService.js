app.service('DeckService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        getDecks: function() {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/decks/',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        getDeck: function(id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/cards/deck/' + id,
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        }
    }
}]);