angular.module('classes')
    .controller('newClassDialogController',function($scope, $state, $mdDialog, ClassesService, toastService){

            var vm = this;

            activate();

            // References to functions.
            vm.closeDialog = closeDialog;
            vm.saveClass = saveClass

            vm.class =  new ClassesService();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newClassDialogController controller.')
            }

            /** Close floating dialog */
            function closeDialog() {
                $mdDialog.cancel();
            }

            /** Save class data in server.
             * Call to server with POST method ($save = POST) using vm.class that is
             * a instance of ClassesService.*/
            function saveClass(){
                console.log('Calling save class function.')
                vm.class.$save(
                    function(){ // Success
                        console.log('Class saved successfully');
                        $mdDialog.cancel();
                        $state.reload();
                        toastService.showToast('Grupo insertado con éxito.')
                    },
                    function(error){ // Fail
                        toastService.showToast('Error al insertar grupo.')
                        console.log('Error while class was saved.')
                        console.log(error)
                    });
            }

});