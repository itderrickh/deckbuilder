app.service('DrawService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        calculate: function(data) {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/draw/' + data.deckSize + '/' + data.targets + '/' + data.drawn
            });
        }
    };
}]);