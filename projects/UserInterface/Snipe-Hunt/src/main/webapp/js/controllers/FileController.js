// Controller for uploading and reading files
mainApp.controller('FileController', function ($scope, $http) {

    $scope.allFiles = [];

    $scope.getAllFiles = function () {

        // REST URL:
        var url = "/Snipe-Hunt/getAllFiles";
        $http.get(url).then(
            // Success
            function (response) {
                $scope.allFiles = response.data;
            },
            // Error
            function (response) {
                $scope.allFiles = response.data;
            }
        );
    };


    $scope.uploadResult = [];
    
    // Used in laying out how the file will be uploaded
    $scope.myForm = {
        description: "",
        files: []
    }

   // Handles the uploading process
    $scope.doUploadFile = function () {

    	// REST URL
        var url = "/Snipe-Hunt/upload";
        var data = new FormData();

        // Set the files uploaded from form into data structure for manipulation
        data.append("description", $scope.myForm.description);
        for (i = 0; i < $scope.myForm.files.length; i++) {
            data.append("files", $scope.myForm.files[i]);
        }

       // Set the configurations for the uploaded file
        var config = {
            transformRequest: angular.identity,
            transformResponse: angular.identity,
            headers: {
                'Content-Type': undefined
            }
        }

        // Sends the file data off
        $http.post(url, data, config).then(
            // Success
            function (response) {
                $scope.uploadResult = response.data;
                $scope.getAllFiles();
                var display = document.getElementById('showFileName');
                display.innerHTML = "";
            },
            // Error
            function (response) {
                $scope.uploadResult = response.data;
            });

    };

});
