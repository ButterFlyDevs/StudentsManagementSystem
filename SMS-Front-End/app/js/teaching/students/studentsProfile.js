angular.module('students')
    .controller('studentsProfileController', function ($scope, $resource, $state, $stateParams, $mdDialog, StudentsService, toastService, globalService) {

        var vm = this;

        vm.studentId = $stateParams.studentId

        // References to functions.
        vm.updateStudent = updateStudent;
        vm.showDeleteStudentConfirm = showDeleteStudentConfirm
        //vm.addRelation = addRelation;

        vm.defaultAvatar = globalService.defaultAvatar;

        vm.student = StudentsService.get({id: vm.studentId}, function () {
            console.log(vm.student)
            var parts = vm.student.birthdate.split('-');
            var tmpDateObject = new Date(parts[0], parts[1] - 1, parts[2]);
            vm.student.birthdate = tmpDateObject;

        }, function () {
            console.log('Student not found')
            vm.student = null;
        })

        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating studentsProfileController controller.')

        }

        /** Delete student in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.student that is
         * a instance of StudentsService.*/
        function deleteStudent() {

            vm.student.$delete(
                function(){ // Success
                    console.log('Student deleted successfully.')
                    $state.go('students')
                    toastService.showToast('Estudiante eliminado con éxito.')
                },
                function(error){ // Fail
                    console.log('Student deleted process fail.')
                    console.log(eror)
                    toastService.showToast('Error eliminando al estudiante.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteStudentConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar a este estudiante?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(function () {
                deleteStudent();
            }, function () {
                console.log('Operacion cancelada.')
            });

        };

        /** Update student data in server.
         * Call to server with PUT method ($update = PUT) using vm.student that is
         * a instance of StudentsService.*/
        function updateStudent() {
            console.log('Calling updateStudent() function.')

            // A dirty solution to problem that does that the date is saved with a day minus.
            vm.student.birthdate.setDate(vm.student.birthdate.getDate() + 1);

            vm.student.$update(
                function () { // Success
                    console.log('Student saved successfully.')
                    toastService.showToast('Estudiante actualizado con éxito.')
                },
                function (error) { // Fail
                    console.log('Error saving student.')
                    console.log(error)
                    toastService.showToast('Error actualizando al estudiante.')
                });
        }


    })

    /** Configure date format in <md-datepicker> */
    .config(function ($mdDateLocaleProvider) {
        $mdDateLocaleProvider.formatDate = function (date) {

            // While don't find other better solution to set format DD-MM-YYYY like in Spain
            // and set default text: "Fecha de nacimiento"
            if (date == undefined) {
                console.log('undefined')
                return 'Fecha Nacimiento'
            } else {
                return moment(date).format('DD-MM-YYYY');
            }
        };
    });
