app.component('spritePicker', {
	templateUrl: 'js/directives/sprite-picker/sprite-picker.component.html',
	bindings: {
		sprite: '<',
		spriteSelect: '&'
	},
	restrict: 'E',
	controller: ['$scope', '$element', '$attrs', function($scope, $element, $attrs) {
		var _this = this;

		$scope.sprite = _this.sprite || '001';
		$scope.open = false;
		$scope.openPosition = [0, 0];
		$scope.spriteRange = new Array(807).fill(0).map((x, i) => {
			const s = (i + 1) + "";
			return s.padStart(3, "0");
		});

		$scope.spriteRange.push("800a");
		$scope.spriteRange.push("800b");
		$scope.spriteRange.push("800c");

		$scope.selectSprite = function(value) {
			$scope.sprite = value;
			$attrs.sprite = value;
			$scope.open = false;
			_this.spriteSelect({ sprite: value });
		};

		$scope.openEditor = function(event) {
			$scope.openPosition = [event.pageX, event.pageY];
			$scope.open = true;
		};
	}]
});
