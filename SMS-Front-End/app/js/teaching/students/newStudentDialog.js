angular.module('students')
    .controller('newStudentDialogController',function($scope, $state, $mdDialog, StudentsService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveStudent = saveStudent

            vm.student =  new StudentsService();


            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating newStudentDialogController controller.')
            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            function saveStudent(){
                console.log('Calling saveStudent() function.')
                vm.student.$save(function(){
                    console.log('Student saved successfully');
                    $mdDialog.cancel();
                    $state.reload();
                });
            }

});