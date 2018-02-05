app.service('ImportService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        importDeck: function(name, text) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/decks/import',
                data: { name: name, text: text },
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        importFromLimitless: function(name, url) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/decks/import/limitless',
                data: { name: name, url: url },
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        }
    }
}]);