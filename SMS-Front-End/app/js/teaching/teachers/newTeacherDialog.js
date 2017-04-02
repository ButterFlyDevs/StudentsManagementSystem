angular.module('teachers')
    .controller('newTeacherDialogController',function($scope, $state, $mdDialog, TeachersService, toastService){

            var vm = this;

            activate();

            // References to functions.
            vm.closeDialog = closeDialog;
            vm.saveTeacher = saveTeacher;

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


            /** Save teacher data in server.
             * Call to server with POST method ($save = POST) using vm.teacher that is
             * a instance of TeachersService.*/
            function saveTeacher(){
                console.log('Calling saveTeacher() function.');

                // A dirty solution to problem that does that the date is saved with a day minus.
                vm.teacher.birthdate.setDate(vm.teacher.birthdate.getDate() + 1);

                vm.teacher.$save(
                    function(){ // Success
                        console.log('Teacher saved successfully');
                        $mdDialog.cancel();
                        $state.reload();
                        toastService.showToast('Profesor dado de alta con éxito.')
                    },
                    function(error){ // Fail
                        toastService.showToast('Error al dar de alta al profesor.');
                        console.log('Error while teacher was saved.');
                        console.log(error)
                    });

            }

});