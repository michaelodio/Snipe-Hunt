// Controller for accessing Accumulo tables
mainApp.controller('AccumuloController', function ($scope, $http) {

    $scope.getAccumulo = function () {
        // REST URL:
        var url = "/Snipe-Hunt/getAccumulo";
        var url2 ="/Snipe-Hunt/getVideosTable";

        $http.get(url).then(
            // Success
            function (response) {
                $scope.analytics = response.data;
                return $http.get(url2)
            })
            .then(function(response) {
                $scope.jsons = response.data;
            });
    };
});
