angular.module('teachers')
    .controller('newTeacherDialogController',function($scope, $state, $mdDialog, TeachersService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveTeacher = saveTeacher

            vm.teacher =  new TeachersService();
            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

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

                // A dirty solution to problem that does that the date is saved with a day minus.
                vm.teacher.data.birthdate.setDate(vm.teacher.data.birthdate.getDate() + 1);

                vm.teacher.$save(function(){
                    console.log('Teacher saved successfully');
                    $mdDialog.cancel();
                    $state.reload();
                });

            }

});