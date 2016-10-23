angular.module('students')
    .controller('studentsProfileController',function($scope, $resource, $stateParams, $mdDialog, StudentsService){

            var vm = this;

            vm.studentId = $stateParams.studentId

            // Functions associations
            //vm.addRelation = addRelation;

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



});
