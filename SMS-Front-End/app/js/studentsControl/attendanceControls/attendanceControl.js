angular.module('attendanceControls')
    .controller('attendanceControlController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, toastService, globalService, attendanceControlsService) {

        var vm = this;

        // vm.teacherId = $stateParams.teacherId;

        vm.defaultAvatar = globalService.defaultAvatar;

        // Functions:
        vm.changeAssistanceForStudent = changeAssistanceForStudent;

        // To control the loading spinner.
        vm.dataIsReady = false;

        vm.delayList = ['5', '10', '15', '20', '30', '45'];

        activate();

        ///////////////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating attendanceControlController controller.');

            vm.acBase = attendanceControlsService.getBase({id: 5629499534213120},
                function () {
                    console.log('Attendance Control Base Data Block');
                    console.log(vm.acBase);
                    vm.dataIsReady = true;

                }, function (error) {
                    console.log('Get ac base process fail.');
                    console.log(error);
                    toastService.showToast('Error obteniendo la base para el control de asistencia.')
                })

        }

        function changeAssistanceForStudent(studentId){
            console.log('changing');
            console.log(studentId);


            for(var a=0; a<vm.acBase.students.length; a++){
                if (vm.acBase.students[a].studentId == studentId){
                    if(vm.acBase.students[a].control.assistance == true){
                        vm.acBase.students[a].control.assistance = false;
                    }else{
                        vm.acBase.students[a].control.assistance = true;
                    }
                }
            }

        }

    });