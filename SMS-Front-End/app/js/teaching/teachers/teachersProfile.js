angular.module('teachers')
    .controller('teachersProfileController',function($scope, TeachersService){

            var vm = this;
            vm.text='hi';

            vm.defaultAvatar = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g'


            vm.teacher = TeachersService.get({id: 2}, function(){
                console.log(vm.teacher)
            })


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
                console.log('Activating teachersProfileController controller.')

            }

});
