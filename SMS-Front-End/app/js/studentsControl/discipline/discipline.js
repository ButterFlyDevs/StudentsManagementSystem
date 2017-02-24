angular.module('discipline')
    .controller('disciplineController', function ($scope, moment, $q, $resource, $state, $stateParams, $mdDialog, toastService, globalService) {

            var vm = this;

            console.log(vm.action);

            vm.defaultAvatar = globalService.defaultAvatar;

            activate();


            ///////////////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating discipline controller.');


            }


    });