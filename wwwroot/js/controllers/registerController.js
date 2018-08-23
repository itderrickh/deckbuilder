app.controller('RegisterController', ['$timeout', '$location', '$rootScope', 'RegisterService', function($timeout, $location, $rootScope, RegisterService) {
	var regCtrl = this;

	regCtrl.username = "";
	regCtrl.password = "";
	regCtrl.playerId = "";
	regCtrl.passwordConfirm = "";
	regCtrl.zipCode = "";
	regCtrl.name = "";
	regCtrl.theme = "base";
	regCtrl.dob = new Date();
	regCtrl.message = "";

	regCtrl.changeTheme = function() {
		$rootScope.css = regCtrl.theme;
	};

	regCtrl.submit = function() {
		RegisterService.register({
			username: regCtrl.username,
			password: regCtrl.password,
			playerid: regCtrl.playerId,
			name: regCtrl.name,
			dateofbirth: regCtrl.dob,
			theme: regCtrl.theme,
			zipCode: regCtrl.zipCode
		}).then(function(response) {
			swal({
				title: 'Completed!',
				text: response.data.message,
				type: 'success',
				confirmButtonColor: '#3085d6',
				confirmButtonText: 'OK!'
			}).then(function(data) {
				// HACK: Fix this later
				$timeout(function() {
					$location.path('/login');
				}, 0);
			})
		}, function(res) {
			regCtrl.message = res.data.error;
		});
	};
}]);