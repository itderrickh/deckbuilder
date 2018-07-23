app.controller('UploadController', ['$scope', 'UploadService', function($scope, UploadService) {
	var uploadCtrl = this;

	$scope.uploadFile = function(files) {
		uploadCtrl.file = new FormData();
		uploadCtrl.file.append("file", files[0]);
	};

	uploadCtrl.submit= function() {
		UploadService.upload(uploadCtrl.file).then(function(response) {
			console.log(response);
		});
	};
}]);