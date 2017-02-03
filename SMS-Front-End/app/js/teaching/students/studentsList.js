angular.module('students')
    .controller('studentsListController', function ($scope, $mdDialog, StudentsService, globalService) {

        var vm = this;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewStudentDialog = openNewStudentDialog;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsListController controller.')
            vm.studentsList = StudentsService.query({}, function () {
                vm.dataIsReady = true;
            }, function (error) {
                console.log('Any problem found when was retrieved the student list.');
                console.log(error);
            })
        }

        /**
         * Open the floating dialog to create a new class.
         */
        function openNewStudentDialog() {
            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newStudentDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/teaching/students/newStudentDialog.html'
            }).then(function () {}, function () {});
        }

    });