app.service('ExportService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        getDeckList: function(id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/cards/deck/export/' + id,
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        getDecks: function() {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/decks/',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        exportOfficial: function(id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/deck/exportpdf/' + id,
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        }
    }
}]);