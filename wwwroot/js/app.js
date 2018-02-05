var app = angular.module("DeckBuilderModule", ['ngRoute', 'ngclipboard']);

var tokenToUser = function(token) {
	var parts = token.split(".");
	return JSON.parse(atob(parts[1]));
};

app.factory('authHttpResponseInterceptor',['$q','$location',function($q,$location){
	return {
		response: function(response){
			if (response.status === 401) {
				console.log("Response 401");
			}
			return response || $q.when(response);
		},
		responseError: function(rejection) {
			if (rejection.status === 401) {
                var oldpath = $location.path();
				$location.path('/login');
			}
			return $q.reject(rejection);
		}
	}
}])
.config(['$httpProvider',function($httpProvider) {
	//Http Intercpetor to check auth failures for xhr requests
	$httpProvider.interceptors.push('authHttpResponseInterceptor');
}]);

app.run(function($rootScope, $location, $http) {
	$rootScope.BASE_URL = "http://localhost:5000/api/";
	$rootScope.token = localStorage.getItem('token');
	if($rootScope.token != null) {
		$rootScope.user = tokenToUser($rootScope.token);
	}
	
	$rootScope.$on('$routeChangeStart', function(event, next, current) {
		if(typeof(next.resolve) != 'undefined') {
			if($rootScope.token == null || !next.resolve($rootScope.token)) {
				$location.path('/login');
			}
		}
    });
});

app.config(function($routeProvider) {
    var resolve = function(token) {
		return typeof(token) != 'undefined' && token != '';
    };
    
    $routeProvider
    .when("/", {
        templateUrl : "./views/main.html",
        controller: "MainController",
        controllerAs: "mainCtrl"
    })
    .when("/decks", {
        templateUrl : "./views/decks.html",
        controller: "DeckController",
        controllerAs: "deckCtrl",
        resolve: resolve
    }).when("/create", {
        templateUrl : "./views/create.html",
        controller: "CreateController",
        controllerAs: "createCtrl",
        resolve: resolve
    }).when("/import", {
        templateUrl : "./views/import.html",
        controller: "ImportController",
        controllerAs: "importCtrl",
        resolve: resolve
    }).when("/export", {
        templateUrl : "./views/export.html",
        controller: "ExportController",
        controllerAs: "exportCtrl",
        resolve: resolve
    }).when("/login", {
        templateUrl : "./views/login.html",
        controller: "LoginController",
        controllerAs: "loginCtrl"
    }).when("/draw", {
        templateUrl : "./views/draw.html",
        controller: "DrawController",
        controllerAs: "drawCtrl"
    }).otherwise({
		redirectTo: "/login"
	});
});