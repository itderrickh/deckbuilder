app.service('HomeService', ['$http', '$rootScope', '$cookies', function($http, $rootScope, $cookies) {
    return {
        getEvents: function() {
            var cookieExists = $cookies.get('refreshDate');
            var refreshDate = moment($cookies.get('refreshDate'));
            var sevenDaysAgo = moment().add(-7, 'days');

            if(cookieExists && refreshDate > sevenDaysAgo) {
                return $http({
                    method: 'GET',
                    url: 'http://localhost:5000/api/events/',
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
                url: 'http://localhost:5000/api/events/true',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                }
            });
        },
        hideEvent: function(event) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/events/hide',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                },
                data: { eventId: event.id }
            });
        },
        addEvent: function(event) {
            return $http({
                method: 'POST',
                url: 'http://localhost:5000/api/events/add',
                headers: {
                    'Authorization': 'JWT ' + $rootScope.token
                },
                data: { eventId: event.id }
            });
        }
    };
}]);