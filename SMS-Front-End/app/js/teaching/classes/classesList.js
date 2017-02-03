angular.module('classes')
    .controller('classesListController', function ($scope, $mdDialog, ClassesService, globalService) {

        var vm = this;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewClassDialog = openNewClassDialog;

        // To control the loading spinner.
        vm.dataIsReady = false;

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating classesListController controller.')
            vm.classesList = ClassesService.query({}, function () {
                vm.dataIsReady = true;
            }, function (error) {
                console.log('Any problem found when was retrieved the classes list.');
                console.log(error);
            })
        }

        /**
         * Open the floating dialog to create a new class.
         */
        function openNewClassDialog() {
            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newClassDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/teaching/classes/newClassDialog.html'
            }).then(function () {}, function () {});
        }


    });
