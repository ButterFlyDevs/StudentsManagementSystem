angular.module('students')
    .controller('newStudentDialogController',function($scope, $state, $mdDialog, StudentsService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveStudent = saveStudent

            vm.student =  new StudentsService();
            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

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