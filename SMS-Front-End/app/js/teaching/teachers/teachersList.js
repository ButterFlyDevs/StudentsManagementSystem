

angular.module('teachers')
    .controller('teachersListController',function($scope, TeachersService){

            var vm = this;
            vm.text='hi';

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

                vm.teachersList = TeachersService.query({}, function(){
                    console.log(vm.teachersList)
                })

            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
