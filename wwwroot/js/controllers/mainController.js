app.controller('MainController', ['HomeService', function (homeService) {
    var mainCtrl = this;
    mainCtrl.events = [];

    homeService.getEvents().then(function (response) {
        var events = response.data;
        for (e in events) {
            events[e].date = new Date(events[e].date.replace("GMT", ""));
        }

        mainCtrl.events = events;
    });

    mainCtrl.eventSource = {
        url: "http://localhost:5000/api/events",
        className: 'gcal-event',
        currentTimezone: 'America/Chicago'
    };

    mainCtrl.eventClick = function (date, jsEvent, view) {
        date.date = date.date.replace("GMT", "");
        var formatDate = moment(date.date).format("dddd, MMMM Do YYYY @ hh:mm a");
        swal(
            date.title,
            formatDate,
            'info'
        );
    };
    mainCtrl.eventSources = [mainCtrl.events, mainCtrl.eventSource];

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
}]);