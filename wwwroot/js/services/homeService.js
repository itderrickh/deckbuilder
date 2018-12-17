app.service('HomeService', ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies) {
    return {
        getEvents: function() {
            var cookieExists = $cookies.get('refreshDate');
            var refreshDate = moment($cookies.get('refreshDate'));
            var thirtyDaysAgo = moment().add(-30, 'days');

            if(cookieExists && refreshDate > thirtyDaysAgo) {
                return $http({
                    method: 'GET',
                    url: 'http://localhost:5000/api/2.0/events/',
                    headers: {
                        'Authorization': 'JWT ' + $rootScope.token
                    }
                });
            } else {
                $cookies.put('refreshDate', moment().format("MM-DD-YYYY"));
                return this.refreshEvents();
            }
        },
        refreshEvents: function() {
            return $http({
                method: 'GET',
                url: 'http://localhost:5000/api/2.0/events/true',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        hideEvent: function(event) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/2.0/events/hide',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                },
                data: { eventId: event.id }
            });
        },
        addEvent: function(event) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/2.0/events/add',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                },
                data: { eventId: event.id }
            });
        }
    };
}]);