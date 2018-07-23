app.service('UploadService', ['$http', '$rootScope', function($http, $rootScope) {
    return {
        upload: function(data) {
            return $http({
                method: 'POST',
				url: 'http://localhost:5000/api/sets/upload',
				data: data,
                headers: { 'Content-Type': undefined },
                transformRequest: angular.identity
            });
        }
    };
}]);