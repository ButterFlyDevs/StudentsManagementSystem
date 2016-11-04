angular.module('teachers')
    .controller('newTeacherDialogController',function($scope, $state, $mdDialog, TeachersService){

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
                console.log('Calling saveTeacher() function.')
                vm.teacher.$save(function(){
                    console.log('Teacher saved successfully');
                    $mdDialog.cancel();
                    $state.reload();
                });
            }

});