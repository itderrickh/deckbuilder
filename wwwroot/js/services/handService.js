app.service('HandService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        sampleHand: function(data) {
            return $http({
                method: 'GET',
				url: 'http://localhost:5000/api/decks/hand/' + data,
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
        }
    };
}]);