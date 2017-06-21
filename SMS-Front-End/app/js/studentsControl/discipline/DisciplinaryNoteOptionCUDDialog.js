angular.module('discipline')
    .controller('newDisciplinaryNoteOptionDialogController', function ($scope, $state, $q, $mdDialog, toastService, parentController) {

        var vm = this;

        vm.title = null;
        activate();

        ///////////////////////////////////////////////////////////
        function activate() {
            console.log('Activating newDisciplinaryNoteOptionDialogController controller.');

            vm.mode = parentController.mode;
            vm.type = parentController.type;
            vm.item = parentController.item;


            if (parentController.type == 'kind'){
                if (vm.mode == 'create'){
                    vm.title = "Añadir tipo";
                    vm.subtitle = "Inserte el nombre.";
                }
                if (vm.mode == 'update'){
                    vm.title = "Actualizar tipo";
                    vm.subtitle = "Modifique el nombre del tipo."
                    vm.typeName = vm.item.meaning;
                }
            }



        }


        vm.closeDialog = function closeDialog() {
            $mdDialog.cancel();
        };


        vm.saveOption = function saveOption() {
            console.log('Calling saveDisciplinaryNote() function.');

            if(parentController.type == 'kind'){

                if(vm.mode == 'create') {

                    var kinds = parentController.dnSchema.kinds;
                    var isPosible = true;
                    for(var a=0; a<kinds.length; a++)
                        if (kinds[a].meaning == vm.typeName) {
                            toastService.showToast('Elemento duplicado');
                            isPosible = false;
                        }

                    if (isPosible)
                        parentController.dnSchema.kinds.push({'code': kinds.length + 1, 'meaning': vm.typeName})
                }
                if(vm.mode == 'update'){
                    parentController.dnSchema.kinds[parentController.dnSchema.kinds.indexOf(vm.item)]['meaning'] = vm.typeName;
                }

                parentController.compare();
            }

            vm.closeDialog();



        }





    });