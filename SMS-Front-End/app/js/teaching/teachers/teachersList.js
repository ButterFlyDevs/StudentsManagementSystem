angular.module('teachers')
    .controller('teachersListController', function ($scope, $mdDialog, TeachersService, globalService) {

        var vm = this;

        // References to functions.
        vm.openNewTeacherDialog = openNewTeacherDialog;

        vm.defaultAvatar = globalService.defaultAvatar;


        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating teachersListController controller.')

            vm.teachersList = TeachersService.query({}, function () {
                console.log(vm.teachersList)
            }, function () {
                console.log('Any problem found when was retrieved the teachers list.')
            })

        }

        function openNewTeacherDialog() {
            console.log('Open new Teacher Dialog')

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm},
                controller: 'newTeacherDialogController',
                controllerAs: 'vm',
                templateUrl: 'app/views/teaching/teachers/newTeacherDialog.html'
            })
                .then(function () {

                }, function () {

                });
        }


    });
