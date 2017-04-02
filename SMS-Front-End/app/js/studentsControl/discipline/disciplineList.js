angular.module('discipline')
    .controller('disciplineController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, $mdpTimePicker, toastService, DisciplineService, globalService) {

        var vm = this;

        vm.dataIsReady = false;

        vm.defaultAvatar = globalService.defaultAvatar;
        vm.openNewDisciplinaryNoteDialog = openNewDisciplinaryNoteDialog;

        vm.modificationStatus = true;
        vm.updateButtonEnable = false; // To control when the update button could be enabled.

        //@param mode Option to configure: create, update, delete
        vm.openNewItemDialog = function openNewItemDialog(type, mode, item) {

            vm.mode = mode;
            vm.type = type;
            vm.item = item;
            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newDisciplinaryNoteOptionDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/studentsControl/discipline/newDisciplinaryNoteOption.html'
            }).then(function () {}, function () {});
        };




        vm.prueba = function prueba(){
            console.log('PRUEBA')
        };

        activate();


        ///////////////////////////////////////////////////////////////////ªª
        function activate() {
            console.log('Activating discipline controller.');

            vm.disciplinaryNotes = DisciplineService.query({}, function () {
                vm.dataIsReady = true;
                console.log(vm.disciplinaryNotes);
            }, function (error) {
                console.log('Any problem found when was retrieved the disciplinary notes list.', error);
            });
        }

        vm.modValues = function modValues(){
            vm.modificationStatus = !vm.modificationStatus;
        };

        vm.cancelModValues = function cancelModValues(){
            // Do all fields not editables.
            vm.modificationStatus = !vm.modificationStatus;
            // Back to previous state without new request:
            vm.dnSchema = angular.copy(vm.dnSchemaOriginalCopy);
        };



        function deleteAndRelocate(list, index){
            list.splice(index, 1);
            for (var i=index; i<list.length-1; i++)
                list[i].code=list[i].code-1;
        }



        vm.deleteOption = function deleteOption(type, object){

            if (type == 'kind'){

                if (vm.dnSchema.kinds.length == 1){
                     toastService.showToast('Imposible eliminar, al menos debe exisitir un tipo en el sistema.');
                }else {
                    var index = vm.dnSchema.kinds.indexOf(object);
                    deleteAndRelocate(vm.dnSchema.kinds, index);
                }
            }
        };

        vm.updateOptions = function updateOptions(type, object){
            DisciplineService.updateSchema({},vm.dnSchema, function(){
            }, function(error) {
                 console.log('Any problem found saving the new dn options.', error);
            })
        };

        vm.compare = function compare() {

            if ($scope.dnSchemaModelHasChanged) {
                vm.updateButtonEnable = true;
            } else {
                vm.updateButtonEnable = false;
            }
        }

        vm.loadSettings = function loadSettings(){
            // Schema with data that must be selected to send the form and must be received before.
            vm.dnSchema = DisciplineService.getSchema(function () {


                // As we want to have a copy of original data to show when the save is possible.

                // ### Do a copy to save process. ###
                vm.dnSchemaOriginalCopy = angular.copy(vm.dnSchema);

                $scope.dnSchemaModelHasChanged = false;

                // To make possible the changes detections pre-saved item to avoid or allow the save action.
                $scope.$watch('vm.dnSchema', function (newValue, oldValue){
                    if(newValue != oldValue){
                        $scope.dnSchemaModelHasChanged = !angular.equals(vm.dnSchema, vm.dnSchemaOriginalCopy);
                    }
                    vm.compare();
                }, true);

            }, function(error){
                console.log('Any problem found when was retrieved disciplinary note schema.', error);
            });
        };

        /**
         * Open the floating dialog to create a new disciplinary note.
         */
        function openNewDisciplinaryNoteDialog() {

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm}, controller: 'newDisciplinaryNoteDialogController',
                controllerAs: 'vm', templateUrl: 'app/views/studentsControl/discipline/newDisciplinaryNoteDialog.html'
            }).then(function () {console.log('true')}, function () {console.log('fail')});
        }


    });