

angular.module('teachers')
    .controller('teachersListController',function($scope){

            var vm = this;
            vm.text='hi';

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersListController controller.')

            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
