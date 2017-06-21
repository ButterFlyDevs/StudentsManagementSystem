angular.module('main')
    .service("toastService", function($mdToast) {

        console.log('Activating toastService service.');

        var service = {
            showToast: showToast
        };

         function showToast(message) {

             var toast = $mdToast.simple()
                .content(message)
                .position('bottom right')
                .hideDelay(3000)

            $mdToast.show(toast);

        };


        return service;



        }

        );
