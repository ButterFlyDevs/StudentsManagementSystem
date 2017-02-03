angular.module('main')
    .directive('spinner', spinnerDirective)
    .service("globalService",
        function(){
            console.log('Activating globalService service.');
            return {
             defaultAvatar : 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcThQiJ2fHMyU37Z0NCgLVwgv46BHfuTApr973sY7mao_C8Hx_CDPrq02g',
             //defaultMicroServicesURL: 'https://sms-back-end.appspot.com'
              defaultMicroServicesURL: 'localhost:8001'
            }
        }
    );