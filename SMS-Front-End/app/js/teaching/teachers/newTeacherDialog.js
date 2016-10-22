angular.module('teachers')
    .controller('newTeacherDialogController',function($scope, $mdDialog, TeachersService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveTeacher = saveTeacher

            vm.teacher =  new TeachersService();


            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newTeacherDialogController controller.')
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            function saveTeacher(){
                console.log('Calling save teacher function.')
                vm.teacher.$save(function(){
                    console.log('Save successfully');
                    $mdDialog.cancel();
                });
            }

});