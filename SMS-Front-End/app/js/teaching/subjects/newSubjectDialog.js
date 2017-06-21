angular.module('subjects')
    .controller('newSubjectDialogController',function($scope, $state, $mdDialog, SubjectsService, toastService){

            var vm = this;

            activate();

            // References to functions.
            vm.closeDialog = closeDialog;
            vm.saveSubject = saveSubject;

            vm.subject =  new SubjectsService();



            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newSubjectDialogController controller.')
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            /** Save subject data in server.
             * Call to server with POST method ($save = POST) using vm.subject that is
             * a instance of SubjectsService.*/
            function saveSubject(){
                console.log('Calling save subject function.')
                vm.subject.$save(
                    function(){ // Success
                        console.log('Subject saved successfully');
                        $mdDialog.cancel();
                        $state.reload();
                        toastService.showToast('Asignatura insertada con éxito.')
                    },
                    function(error){ // Fail
                        toastService.showToast('Error al insertar asignatura.')
                        console.log('Error while subject was saved.')
                        console.log(error)
                    });
            }

});