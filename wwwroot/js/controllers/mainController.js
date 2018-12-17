app.controller('MainController', ['$rootScope', 'HomeService', function ($rootScope, homeService) {
    var mainCtrl = this;
    mainCtrl.events = [];
    mainCtrl.userEvents = [];

    homeService.getEvents().then(function (response) {
        var events = response.data;

        for (e in events) {
            events[e].date = new Date(events[e].date.replace("GMT", ""));
        }

        mainCtrl.events = events;
    });

    mainCtrl.eventSource = {
        url: "http://localhost:5000/api/2.0/events/user",
        className: 'gcal-event',
        currentTimezone: 'America/Chicago',
        headers: {
            'Authorization': 'JWT ' + $rootScope.token
        }
    };

    mainCtrl.eventClick = function (date, jsEvent, view) {
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

    mainCtrl.eventSources = [mainCtrl.userEvents, mainCtrl.eventSource];

    mainCtrl.uiConfig = {
        calendar: {
            height: 450,
            editable: false,
            header: {
                left: 'title',
                center: '',
                right: 'today prev,next'
            },
            eventClick: mainCtrl.eventClick
        }
    };

    mainCtrl.hideEvent = function(event) {
        homeService.hideEvent(event).then(function(res) {
            homeService.getEvents().then(function (response) {
                var events = response.data;

                for (e in events) {
                    events[e].date = new Date(events[e].date.replace("GMT", ""));
                }

                mainCtrl.events = events;

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

    mainCtrl.addEvent = function(event) {
        mainCtrl.userEvents.push(event);
        homeService.addEvent(event).then(function(res) {
            homeService.getEvents().then(function (response) {
                var events = response.data;

                for (e in events) {
                    events[e].date = new Date(events[e].date.replace("GMT", ""));
                }

                mainCtrl.events = events;

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