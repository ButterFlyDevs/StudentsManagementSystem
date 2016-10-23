angular.module('students')
    .controller('newStudentDialogController',function($scope, $mdDialog, StudentsService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveStudent = saveStudent

            vm.teacher =  new StudentsService();


            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newStudentDialogController controller.')
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            function saveStudent(){
                console.log('Calling save student function.')
                vm.teacher.$save(function(){
                    console.log('Save successfully');
                    $mdDialog.cancel();
                });
            }

});