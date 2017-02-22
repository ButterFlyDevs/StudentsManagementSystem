angular.module('marks')
    .controller('marksController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, toastService, globalService) {

            var vm = this;

            console.log(vm.action);

            vm.defaultAvatar = globalService.defaultAvatar;

            activate();


            ///////////////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating marks controller.');


            }


    });