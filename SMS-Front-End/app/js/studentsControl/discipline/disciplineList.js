angular.module('discipline')
    .controller('disciplineController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, $mdpTimePicker, toastService, DisciplineService, globalService) {

        var vm = this;

        console.log(vm.action);
        vm.dataIsReady = false;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewDisciplinaryNoteDialog = openNewDisciplinaryNoteDialog;

        vm.prueba = function prueba(){
            console.log('PRUEBA')
        }

        activate();


        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating discipline controller.');

            vm.disciplinaryNotes = DisciplineService.query({}, function () {
                vm.dataIsReady = true;
                console.log(vm.disciplinaryNotes);
            }, function (error) {
                console.log('Any problem found when was retrieved the disciplinary notes list.');
                console.log(error);
            });
        }

        /**
         * Open the floating dialog to create a new class.
         */
        function openNewDisciplinaryNoteDialog() {

            console.log('yeah')

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newDisciplinaryNoteDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/studentsControl/discipline/newDisciplinaryNoteDialog.html'
            }).then(function () {console.log('true')}, function () {console.log('fail')});
        }


    });