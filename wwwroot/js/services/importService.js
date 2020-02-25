app.service('ImportService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        importDeck: function(name, text, sprites) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/decks/import',
                data: { name: name, text: text, sprites: sprites },
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        importFromLimitless: function(name, url, sprites) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/decks/import/limitless',
                data: { name: name, url: url, sprites: sprites },
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        }
    }
}]);