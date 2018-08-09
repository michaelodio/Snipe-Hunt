// Create the main module and make it use routing
var mainApp = angular.module('MainApp', ['ngRoute']);

// Configure the URL routes allowed
mainApp.config(function ($routeProvider) {
    $routeProvider
        .when('/upload', {
            controller: 'FileController',
            templateUrl: 'templates/upload.html'
        })
        .when('/analyze', {
            controller: 'AccumuloController',
            templateUrl: 'templates/analyze.html'
        })
        .when('/aboutus', {
            templateUrl: 'templates/aboutus.html'
        })
        .otherwise({
            redirectTo: '/upload'
        });
});

