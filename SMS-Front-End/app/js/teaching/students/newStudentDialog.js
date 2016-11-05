angular.module('students')
    .controller('newStudentDialogController',function($scope, $state, $mdDialog, StudentsService, toastService){

            var vm = this;

            activate();

            // References to functions.
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


            /** Save student data in server.
             * Call to server with POST method ($save = POST) using vm.student that is
             * a instance of StudentsService.*/
            function saveStudent(){
                console.log('Calling saveStudent() function.')


                // A dirty solution to problem that does that the date is saved with a day minus.
                vm.student.data.birthdate.setDate(vm.student.data.birthdate.getDate() + 1);

                vm.student.$save(
                    function(){ // Success
                        console.log('Student saved successfully');
                        $mdDialog.cancel();
                        $state.reload();
                        toastService.showToast('Estudiante dado de alta con éxito.')
                    },
                    function(error){ // Fail
                        toastService.showToast('Error al dar de alta al alumno.')
                        console.log('Error while student was saved.')
                        console.log(error)
                    }
                );
            }

});