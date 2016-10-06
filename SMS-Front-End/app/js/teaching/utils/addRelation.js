

angular.module('teachers')
    .controller('addRelationController',function($scope, $mdDialog, TeachersService, SubjectsService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.subjectIsSelected = subjectIsSelected;

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating addRelation controller.')

                vm.teachersList = TeachersService.query({}, function(){
                    console.log(vm.teachersList)
                }, function(){
                    console.log('Any problem found when was retrieved the teachers list.')
                })

                vm.subjectsList = SubjectsService.query({}, function(){
                    console.log(vm.subjectsList)
                }, function(){
                    console.log('Any problem found when was retrieved the subjects list.')
                })


            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            // Function to select only the classes that are related with this subjects in database.
            function subjectIsSelected(subjectId) {
                console.log('Subject elected: ' + subjectId)

                // now we search all classes that is related with this subject.

            }


});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
