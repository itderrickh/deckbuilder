app.controller('HomeController', ['$rootScope', 'HomeService', function ($rootScope, homeService) {
    var homeCtrl = this;
    homeCtrl.events = [];
    homeCtrl.userEvents = [];

    homeService.getEvents().then(function (response) {
        var events = response.data;

        for (e in events) {
            events[e].date = new Date(events[e].date.replace("GMT", ""));
        }

        homeCtrl.events = events;
    });

    homeCtrl.eventSource = {
        url: "http://localhost:5000/api/events/user",
        className: 'gcal-event',
        currentTimezone: 'America/Chicago',
        headers: {
            'Authorization': 'JWT ' + $rootScope.token
        }
    };

    homeCtrl.eventClick = function (date, jsEvent, view) {
        date.date = date.date.replace("GMT", "");
        var formatDate = moment(date.date).format("dddd, MMMM Do YYYY @ hh:mm a");
        var splitLoc = date.location.split(", ");
        var location = splitLoc[0] + ", " + splitLoc[1];

        var output = formatDate + '<br>' + location;
        swal(
            date.title,
            output,
            'info'
        );
    };

    homeCtrl.eventSources = [homeCtrl.userEvents, homeCtrl.eventSource];

    homeCtrl.uiConfig = {
        calendar: {
            height: 450,
            editable: false,
            header: {
                left: 'title',
                center: '',
                right: 'today prev,next'
            },
            eventClick: homeCtrl.eventClick
        }
    };

    homeCtrl.hideEvent = function(event) {
        homeService.hideEvent(event).then(function(res) {
            homeService.getEvents().then(function (response) {
                var events = response.data;

                for (e in events) {
                    events[e].date = new Date(events[e].date.replace("GMT", ""));
                }

                homeCtrl.events = events;

                new Noty({
                    theme: 'bootstrap-v4',
                    text: 'Event has been hidden',
                    type: 'info',
                    layout: 'bottomCenter',
                    timeout: 3000
                }).show();
            });
        });
    };

    homeCtrl.addEvent = function(event) {
        homeCtrl.userEvents.push(event);
        homeService.addEvent(event).then(function(res) {
            homeService.getEvents().then(function (response) {
                var events = response.data;

                for (e in events) {
                    events[e].date = new Date(events[e].date.replace("GMT", ""));
                }

                homeCtrl.events = events;

                new Noty({
                    theme: 'bootstrap-v4',
                    text: 'Event has been added to your calendar',
                    type: 'info',
                    layout: 'bottomCenter',
                    timeout: 3000
                }).show();
            });
        });
    };
}]);