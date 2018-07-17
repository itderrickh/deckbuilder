app.controller('LoginController', ['$location', '$rootScope', 'LoginService', 'tokenToUser', function($location, $rootScope, LoginService, tokenToUser) {
	var loginCtrl = this;

	loginCtrl.username = "";
	loginCtrl.password = "";
	loginCtrl.message = "";
	loginCtrl.submit = function() {
		LoginService.login(loginCtrl.username, loginCtrl.password).then(function(response) {
			var res = JSON.parse(response.data);
			$rootScope.token = res.access_token;
			localStorage.setItem('token', $rootScope.token);
			$rootScope.css = tokenToUser.get($rootScope.token).theme;
			$location.path('/decks');
		}, function() {
			loginCtrl.message = "Username or password was incorrect. Please try again";
		});
	};
}]);