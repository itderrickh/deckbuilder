var app = angular.module("DeckBuilderModule", ['ngRoute', 'ngclipboard', 'ui.calendar', 'ngCookies']);

app.service('tokenToUser', [function() {
    this.get = function (token) {
        var parts = token.split(".");
        return JSON.parse(atob(parts[1]));
    };
}]);

app.factory('authHttpResponseInterceptor', ['$q', '$location', '$rootScope', function ($q, $location, $rootScope) {
    return {
        response: function (response) {
            if (response.status === 401) {
                console.log("Response 401");
            }
            return response || $q.when(response);
        },
        responseError: function (rejection) {
            if (rejection.status === 401) {
                var oldpath = $location.path();

                new Noty({
                    theme: 'bootstrap-v4',
                    text: 'Authorization has expired or is invalid. Please log-in to continue.',
                    type: 'error',
                    layout: 'bottomCenter',
                    timeout: 3000
                }).show();

                if(rejection.data && rejection.data.description === "Signature has expired") {
                    $rootScope.token = null;
                    $rootScope.user = null;
                    $rootScope.css = "base";
                    localStorage.removeItem('token');
                }

                $location.path('/login');
            } else {
                new Noty({
                    theme: 'bootstrap-v4',
                    text: rejection.data.error,
                    type: 'error',
                    layout: 'bottomCenter',
                    timeout: 3000
                }).show();
            }
            return $q.reject(rejection);
        }
    }
}]);

app.config(['$httpProvider', function ($httpProvider) {
    //Http Intercpetor to check auth failures for xhr requests
    $httpProvider.interceptors.push('authHttpResponseInterceptor');
    $httpProvider.interceptors.push(['$rootScope', function ($rootScope) {
        var activeRequests = 0;

        return {
            request: function (config) {
                $rootScope.pendingRequest = true;

                activeRequests++;

                return config;
            },
            response: function (response) {
                activeRequests--;

                if(activeRequests === 0) {
                    $rootScope.pendingRequest = false;
                }

                return response;
            }
        }
    }]);
}]);

app.directive('ngRightClick', ['$parse', function($parse) {
    return function(scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function(event) {
            scope.$apply(function() {
                event.preventDefault();
                fn(scope, {$event:event});
            });
        });
    };
}]);

app.run(['$rootScope', '$location', '$http', 'tokenToUser', function ($rootScope, $location, $http, tokenToUser) {
    $rootScope.css = "base";
    $rootScope.BASE_URL = "http://localhost:5000/api/";
    $rootScope.token = localStorage.getItem('token');
    if ($rootScope.token !== null) {
        $rootScope.user = tokenToUser.get($rootScope.token);
        $rootScope.css = $rootScope.user.theme;
    }

    $rootScope.$on('$routeChangeStart', function (event, next, current) {
        if (typeof (next.resolve) !== 'undefined') {
            if (next.resolve.logout) {
                next.resolve.logout($rootScope);
                $location.path('/login');
            } else if ($rootScope.token === null || !next.resolve($rootScope.token)) {
                $location.path('/login');
            }
        }
    });
}]);

app.config(['$routeProvider', function ($routeProvider) {
    var resolve = function (token) {
        return typeof (token) !== 'undefined' && token !== '';
    };

    $routeProvider
        .when("/", {
            templateUrl: "./views/main.html",
            controller: "MainController",
            controllerAs: "mainCtrl"
        })
        .when("/register", {
            templateUrl: "./views/register.html",
            controller: "RegisterController",
            controllerAs: "regCtrl"
        })
        .when("/decks", {
            templateUrl: "./views/decks.html",
            controller: "DeckController",
            controllerAs: "deckCtrl",
            resolve: resolve
        }).when("/create", {
            templateUrl: "./views/create.html",
            controller: "CreateController",
            controllerAs: "createCtrl",
            resolve: resolve
        }).when("/import", {
            templateUrl: "./views/import.html",
            controller: "ImportController",
            controllerAs: "importCtrl",
            resolve: resolve
        }).when("/hand", {
            templateUrl: "./views/hand.html",
            controller: "HandController",
            controllerAs: "handCtrl",
            resolve: resolve
        }).when("/export", {
            templateUrl: "./views/export.html",
            controller: "ExportController",
            controllerAs: "exportCtrl",
            resolve: resolve
        }).when("/login", {
            templateUrl: "./views/login.html",
            controller: "LoginController",
            controllerAs: "loginCtrl"
        }).when("/draw", {
            templateUrl: "./views/draw.html",
            controller: "DrawController",
            controllerAs: "drawCtrl"
        }).when("/upload", {
            templateUrl: "./views/upload.html",
            controller: "UploadController",
            controllerAs: "uploadCtrl",
            resolve: resolve
        }).when("/logout", {
            resolve: {
                logout: function ($rootScope) {
                    $rootScope.token = null;
                    $rootScope.user = null;
                    $rootScope.css = "base";
                    localStorage.removeItem('token');
                    return true;
                }
            }
        }).otherwise({
            redirectTo: "/login"
        });
}]);