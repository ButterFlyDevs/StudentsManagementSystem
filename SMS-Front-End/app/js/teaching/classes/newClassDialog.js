angular.module('classes')
    .controller('newClassDialogController',function($scope, $state, $mdDialog, ClassesService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveClass = saveClass

            vm.class =  new ClassesService();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newClassDialogController controller.')
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            function saveClass(){
                console.log('Calling save class function.')
                vm.class.$save(function(){
                    console.log('Class saved successfully');
                    $mdDialog.cancel();
                    $state.reload();
                });
            }

});