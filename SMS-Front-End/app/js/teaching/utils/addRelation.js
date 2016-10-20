

angular.module('teachers')
    .controller('addRelationController',function($scope, $resource, $mdDialog, $stateParams, TeachersService, SubjectsService, ClassesService, AssociationsService, ImpartsService){

            var vm = this;

            activate();
            vm.closeDialog = closeDialog;
            vm.saveRelation = saveRelation;
            vm.checkRelationSelected = checkRelationSelected;

            vm.subjectSelected = -1;
            vm.classSelected = -1;
            vm.associationId = -1
            vm.createNewAssociationCheckboxValue = false;

            vm.associationRelationExists = true;
            vm.associationImpartExists = false;
            vm.addButtonEnable = false;

            vm.teacherId = $stateParams.teacherId

            ///////////////////////////////////////////////////////////
            function activate() {
                console.log('Activating addRelation controller.')

                // IT's retrieved all tea
                vm.teachersList = TeachersService.query({}, function(){
                    console.log('List of teachers retrieved.')
                    console.log(vm.teachersList)
                }, function(){
                    console.log('Any problem found when was retrieved the teachers list.')
                })

                // We need all signatures
                vm.subjectsList = SubjectsService.query({}, function(){
                    console.log('List of subjects retrieved.')
                    console.log(vm.subjectsList)
                }, function(){
                    console.log('Any problem found when was retrieved the subjects list.')
                })

                // We need all classes
                vm.classesList = ClassesService.query({}, function(){
                    console.log('List of classes retrieved.')
                    console.log(vm.classesList)
                },function(){
                    console.log('Any problem found when was retrieved the classes list.')
                })

                // We need all associations
                vm.associationsList = AssociationsService.query({}, function(){
                    console.log('List of associations retrieved.')
                    console.log(vm.associationsList)
                },function(){
                    console.log('Any problem found when was retrieved the associations list.')
                })

                // We need all imparts
                vm.impartsList = ImpartsService.query({}, function(){
                    console.log('List of imparts retrieved.')
                    console.log(vm.impartsList)
                },function(){
                    console.log('Any problem found when was retrieved the imparts list.')
                })


            }

            // Function to close the dialog
            function closeDialog() {
                $mdDialog.cancel();
            }

            // Function to call backend to save the relation.
            function saveRelation(){
                console.log('saveRelation function called')

                var impart = new ImpartsService();
                impart.data = {
                  teacherId: vm.teacherId,
                  associationId: vm.associationId
                }
                impart.$save(function(){
                    console.log('Save successfully');
                    $mdDialog.cancel();
                });
            }

            function checkRelationSelected(subjectSelected, classSelected) {

                console.log(vm.teacherId)

                if (subjectSelected != -1 && classSelected != -1) {
                    console.log('subjectSelected:  ' + subjectSelected + '   classSelected: ' + classSelected)
                    var exists = false;
                    for (var i = 0; i < vm.associationsList.length; i++) {
                        if (vm.associationsList[i].subjectId == subjectSelected && vm.associationsList[i].classId == classSelected) {
                            exists = true;
                            vm.associationId = vm.associationsList[i].associationId;
                            console.log(vm.associationId)
                        }
                    }

                    if (exists) {

                        vm.associationRelationExists = true;

                        for (var i = 0; i < vm.impartsList.length; i++) {
                            if (vm.impartsList[i].associationId == vm.associationId && vm.impartsList[i].teacherId == vm.teacherId){
                                vm.associationImpartExists = true;
                            }
                        }

                        if (!vm.associationImpartExists){
                            vm.addButtonEnable = true;
                        }






                    } else {
                        // To show a message in the dialog to confirm that this relation doesn't exists.
                        vm.associationRelationExists = false;
                    }
                }
            }

});

//angular.module('teachers').controller('teachersListController', ['$scope', function($scope) {}]);
