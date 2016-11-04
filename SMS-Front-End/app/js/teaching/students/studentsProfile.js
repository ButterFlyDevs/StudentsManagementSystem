angular.module('students')
    .controller('studentsProfileController',function($scope, $resource, $state, $stateParams, $mdDialog, StudentsService, toastService){

            var vm = this;

            vm.studentId = $stateParams.studentId

            // Functions associations


            //vm.addRelation = addRelation;

            vm.updateStudent = updateStudent;
            vm.showDeleteStudentConfirm = showDeleteStudentConfirm

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


            vm.student = StudentsService.get({id: vm.studentId}, function(){
                console.log(vm.student)

            }, function(){
                console.log('Student not found')
                vm.student = null;
            })

            /*
            vm.teacherSubjects = StudentsService.getSubjects({id: vm.teacherId}, function(){
                console.log('Teachers subjects')
                console.log(vm.teacherSubjects)
            })

            vm.teacherClasses = StudentsService.getClasses({id: vm.teacherId}, function(){
                console.log('Teachers classes')
                console.log(vm.teacherClasses)
            })
            */



            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating studentsProfileController controller.')

            }



            /**
             * Open the dialog to add a relation to this teacher.
             * The add action is done in addUserToProjectController

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
            }*/


            function deleteStudent(){

                vm.student.$delete(function(){
                            console.log('Student deleted successfully.')
                            $state.go('students')
                            toastService.showToast('Estudiante eliminado.')

                        },
                        function(){
                            console.log('Student deleted process fail.')
                        });

            }

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

             function updateStudent(){

                 vm.student.$update(function(){
                    console.log('Student saved successfully.')
                    }, function(error){
                        console.log('Error saving student.')
                        console.log(error)
                    });

            }



});
