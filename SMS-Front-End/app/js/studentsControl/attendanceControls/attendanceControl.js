angular.module('attendanceControls')
    .controller('attendanceControlController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, TeachersService, AssociationsService, ImpartsService, toastService, globalService) {

        var vm = this;

        // vm.teacherId = $stateParams.teacherId;

        // vm.defaultAvatar = globalService.defaultAvatar;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating attendanceControlController controller.');
            vm.addButtonEnable = false;
            //loadData();
        }

        /*
        function loadData() {
        }*/




    })

    /** Configure date format in <md-datepicker> */
    .config(function ($mdDateLocaleProvider) {
        $mdDateLocaleProvider.formatDate = function (date) {

            // While don't find other better solution to set format DD-MM-YYYY like in Spain
            // and set default text: "Fecha de nacimiento" .
            if (date == undefined) {
                console.log('undefined')
                return 'Fecha Nacimiento'
            } else {
                return moment(date).format('DD-MM-YYYY');
            }
        };
    });