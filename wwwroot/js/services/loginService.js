app.service('LoginService', ['$http', '$rootScope', function($http, $rootScope) {
	return {
		login: function(username, password) {
			return $http({
				method: 'POST',
				transformResponse: function(data, headersGetter, status) {
					return data;
				},
				url: 'http://localhost:5000/api/auth',
				data: { username: username, password: password }
			});
		}
	}
}]);