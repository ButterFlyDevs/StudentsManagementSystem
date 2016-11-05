angular.module('teachers')
    .controller('teachersProfileController', function ($scope, moment, $resource, $state, $stateParams, $mdDialog, TeachersService, toastService, globalService) {

        var vm = this;

        vm.teacherId = $stateParams.teacherId


        // References to functions.
        vm.addRelation = addRelation;
        vm.updateTeacher = updateTeacher;
        vm.showDeleteTeacherConfirm = showDeleteTeacherConfirm

        vm.defaultAvatar = globalService.defaultAvatar;


        vm.teacher = TeachersService.get({id: vm.teacherId}, function () {
            console.log(vm.teacher)

            // We need change time data from string to JavaScript date object.

            // Thu Oct  6 00:00:00 2016
            console.log(vm.teacher.birthdate);
            //tmpDateObject.setTime(Date.parse( vm.teacher.birthdate ));


            var parts = vm.teacher.birthdate.split('-');
            var tmpDateObject = new Date(parts[0], parts[1] - 1, parts[2]);

            vm.teacher.birthdate = tmpDateObject;

            //Date 2016-10-05T22:00:00.000Z teachersProfile.js:26:17
            console.log(vm.teacher.birthdate);


        }, function () {
            console.log('Teacher not found')
            vm.teacher = null;
        })


        vm.teacherSubjects = TeachersService.getSubjects({id: vm.teacherId}, function () {
            console.log('Teachers subjects')
            console.log(vm.teacherSubjects)
        })

        vm.teacherClasses = TeachersService.getClasses({id: vm.teacherId}, function () {
            console.log('Teachers classes')
            console.log(vm.teacherClasses)
        })


        activate();

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating teachersProfileController controller.')

        }

        /**
         * Open the dialog to add a relation to this teacher.
         * The add action is done in addUserToProjectController
         */
        function addRelation() {

            $mdDialog.show({
                locals: {parentScope: $scope, parentController: vm},
                controller: 'addRelationController',
                controllerAs: 'vm',
                templateUrl: 'app/views/teaching/utils/addRelationTemplate.html'
            })
                .then(function () {

                }, function () {

                });
        }


        /** Delete teacher in server.
         * Call to server with DELETE method ($delete= DELETE) using vm.teacher that is
         * a instance of TeachersService.*/
        function deleteUser() {

            vm.teacher.$delete(
                function () { // Success
                    console.log('Teacher deleted successfully.')
                    $state.go('teachers')
                    toastService.showToast('Profesor eliminado con éxito.')
                },
                function (error) { // Fail
                    console.log('Teacher deleted process fail.')
                    console.log(error)
                    toastService.showToast('Error eliminando al profesor.')
                });

        }

        /** Show the previous step to delete item, a confirm message */
        function showDeleteTeacherConfirm() {

            var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar a este usuario?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

            $mdDialog.show(confirm).then(
                function () {
                    deleteUser();
                },
                function () {
                    console.log('Del teacher operation canceled.')
                }
            );
        };


        /** Update teacher data in server.
         * Call to server with PUT method ($update = PUT) using vm.teacher that is
         * a instance of TeachersService.*/
        function updateTeacher() {
            console.log('Calling updateTeacher() function.')

            // A dirty solution to problem that does that the date is saved with a day minus.
            vm.teacher.birthdate.setDate(vm.teacher.birthdate.getDate() + 1);

            vm.teacher.$update(
                function () { // Success
                    console.log('Success saving the teacher.')
                    toastService.showToast('Profesor actualizado con éxito.')
                },
                function (error) { // Fail
                    console.log('Error saving the teacher.')
                    console.log(error)
                    toastService.showToast('Error actualizando al profesor.')
                });
        }
    })

    /** Configure date format in <md-datepicker> */
    .config(function ($mdDateLocaleProvider) {
        $mdDateLocaleProvider.formatDate = function (date) {

            // While don't find other better solution to set format DD-MM-YYYY like in Spain
            // and set default text: "Fecha de nacimiento" .
            if (date == undefined) {
                console.log('undefined')
                return 'Fecha Nacimiento'
            } else {
                return moment(date).format('DD-MM-YYYY');
            }
        };
    });