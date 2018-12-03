app.controller('HandController', ['HandService', function(handService) {
    var handCtrl = this;
	handCtrl.sampleHand = [];
	handCtrl.selectedDeck = {};
	handCtrl.decks = [];

    handCtrl.getSample = function() {
        handCtrl.sampleHand = [];
        handService.sampleHand(handCtrl.selectedDeck.id).then(function(response) {
            handCtrl.sampleHand = response.data;
        });
	};

	handService.getDecks().then(function(response) {
        handCtrl.decks = response.data;
    });
}]);