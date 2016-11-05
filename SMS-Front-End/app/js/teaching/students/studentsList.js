angular.module('students')
    .controller('studentsListController', function ($scope, $mdDialog, StudentsService, globalService) {

        var vm = this;

        // References to functions.
        vm.openNewStudentDialog = openNewStudentDialog;


        vm.defaultAvatar = globalService.defaultAvatar;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsListController controller.')

            vm.studentsList = StudentsService.query({}, function () {
                console.log(vm.studentsList)
            }, function () {
                console.log('Any problem found when was retrieved the student list.')
            })

        }

        function openNewStudentDialog() {
            console.log('Open new Student Dialog')

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm},
                controller: 'newStudentDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/views/teaching/students/newStudentDialog.html'
            })
                .then(function () {

                }, function () {

                });
        }

    });
