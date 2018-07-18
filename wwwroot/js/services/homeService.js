app.service('HomeService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        getEvents: function() {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/events'
            });
        },
        refreshEvents: function(id) {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/events/true'
            });
        }
    }
}]);