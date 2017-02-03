angular.module('teachers')
    .controller('teachersListController', function ($scope, $mdDialog, TeachersService, globalService) {

        var vm = this;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewTeacherDialog = openNewTeacherDialog;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating teachersListController controller.')
            vm.teachersList = TeachersService.query({}, function () {
                vm.dataIsReady = true;
            }, function (error) {
                console.log('Any problem found when was retrieved the teachers list.');
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
