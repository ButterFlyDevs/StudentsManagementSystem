angular.module('teachers')
    .controller('teachersProfileController',function($scope, $resource, $stateParams, $mdDialog, TeachersService){

            var vm = this;

            vm.teacherId = $stateParams.teacherId


            // Functions associations
            vm.addRelation = addRelation;
            vm.saveTeacher = saveTeacher;
            vm.showDeleteUserConfirm = showDeleteUserConfirm

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


            vm.teacher = TeachersService.get({id: vm.teacherId}, function(){
                console.log(vm.teacher)


            }, function(){
                console.log('Teacher not found')
                vm.teacher = null;
            })


            vm.teacherSubjects = TeachersService.getSubjects({id: vm.teacherId}, function(){
                console.log('Teachers subjects')
                console.log(vm.teacherSubjects)
            })

            vm.teacherClasses = TeachersService.getClasses({id: vm.teacherId}, function(){
                console.log('Teachers classes')
                console.log(vm.teacherClasses)
            })


            /*
            vm.teacher = {
                "name": "El nombre",
                "surname": "Los apellidos",
                "locality": "Granada",
                "email": "correo@gmail.com",
                "asignaturas":{
                    "num": 2,
                    "items": [{
                        "name": "francés",
                        "idAsignatura": 324
                        },{
                        "name": "francés",
                        "idAsignatura": 324
                        }
                    ]
                }
            }*/

            activate();

            ///////////////////////////////////////////////////////////
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





            function deleteUser(){


                vm.teacher.$delete(function(){
                            console.log('success')
                        },
                        function(){
                            console.log('fail')
                        });

            }


            function showDeleteUserConfirm() {


                var confirm = $mdDialog.confirm()
                .title('¿Está seguro de que quiere eliminar a este usuario?')
                //.textContent('If you do, you will be erased from all project which you are and you can not access to app.')
                //.ariaLabel('Lucky day')
                .ok('Estoy seguro')
                .cancel('Cancelar');

                $mdDialog.show(confirm).then(function () {
                    //$scope.status = _('You decided to get rid of your debt.');

                    deleteUser();
                    //window.location.replace("http://www.google.es");

                    }, function () {
                        console.log('Operacion cancelada')
                        //$scope.status = _('You decided to keep your debt.');
                });



        };


            function saveTeacher() {

                 vm.teacher.$update(function(){
                    console.log('Success saving the teacher.')
                    }, function(error){
                        console.log('Error saving the teacher.')
                        console.log(error)
                    });

            }


});
