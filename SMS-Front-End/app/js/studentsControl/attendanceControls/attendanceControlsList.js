angular.module('attendanceControls')
    .controller('attendanceControlsListController', function ($scope, $mdDialog, globalService, attendanceControlsService) {

        var vm = this;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewTeacherDialog = openNewTeacherDialog;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating attendanceControlsListController controller.')
            vm.acList = attendanceControlsService.query({}, function () {
                vm.dataIsReady = true;
                console.log(vm.acList);
            }, function (error) {
                console.log('Any problem found when was retrieved the attendance controls list.');
                console.log(error);
            })
        }

        /**
         * Open the floating dialog to create a new class.
         */
        function openNewTeacherDialog() {
            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newTeacherDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/teaching/teachers/newTeacherDialog.html'
            }).then(function () {}, function () {});
        }

    });
