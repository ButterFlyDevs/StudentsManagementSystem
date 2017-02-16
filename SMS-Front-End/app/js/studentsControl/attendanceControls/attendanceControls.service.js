angular.module('attendanceControls')
    .factory("attendanceControlsService",
        function ($resource, globalService) {

            var restPath = 'http://'+globalService.defaultMicroServicesURL + '/ac';


            // The second param is [paramDefaults] to pass param to URL
            return $resource(restPath + ':id', {id: '@acId'}, {

                'getAll': {
                    method: 'GET',
                    url: restPath,
                    isArray: true
                },
                'getBase': {
                    method: 'GET',
                    url: restPath + 'base/' + ':id'
                }

            });
     });
