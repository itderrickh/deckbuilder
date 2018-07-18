app.service('RegisterService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        register: function(data) {
            return $http({
                method: 'POST',
				url: 'http://localhost:5000/api/register',
				data: data
            });
        }
    };
}]);