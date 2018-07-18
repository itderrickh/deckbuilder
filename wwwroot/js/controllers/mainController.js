app.controller('MainController', ['HomeService', function(homeService) {
    var mainCtrl = this;
    mainCtrl.events = [];

    homeService.getEvents().then(function(response) {
        var events = response.data;
        for(e in events) {
            events[e].date = new Date(events[e].date.replace("GMT", ""));
        }

        mainCtrl.events = events;
    });
}]);