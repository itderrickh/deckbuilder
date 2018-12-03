app.service('HomeService', ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies) {
    return {
        getEvents: function() {
            var cookieExists = $cookies.get('refreshDate');
            var refreshDate = moment($cookies.get('refreshDate'));
            var thirtyDaysAgo = moment().add(-30, 'days');

            if(cookieExists && refreshDate > thirtyDaysAgo) {
                return $http({
                    method: 'GET',
                    url: 'http://localhost:5000/api/events'
                });
            } else {
                $cookies.put('refreshDate', moment().format("MM-DD-YYYY"));
                return this.refreshEvents();
            }
        },
        refreshEvents: function() {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/events/true'
            });
        }
    }
}]);