angular.module('attendanceControls')
    .factory("attendanceControlsService",
        function ($resource, globalService) {

            var restPath = 'http://'+globalService.defaultMicroServicesURL;


            // The second param is [paramDefaults] to pass param to URL
            return $resource(restPath + ':id', {id: '@acId'}, {

                'getAll': {
                    method: 'GET',
                    url: restPath + '/ac',
                    isArray: true
                },
                'getBase': {
                    method: 'GET',
                    url: restPath + '/acbase/' + ':id'
                }

            });
     });
