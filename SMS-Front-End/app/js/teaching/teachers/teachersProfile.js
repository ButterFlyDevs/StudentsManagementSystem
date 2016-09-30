angular.module('teachers')
    .controller('teachersProfileController',function($scope){

            var vm = this;
            vm.text='hi';

            activate();

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating teachersProfileController controller.')

            }

});
