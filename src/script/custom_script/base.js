var app = angular.module('Qwe', ['ngResource']);


app.factory('UserLogInFactory', function($resource) {
    var url = '/auth/token/api/';
    return $resource(url,
        {},
        {
            post: {
                method: "POST",
                params: {},
                isArray: false,
                cache:false
            }
        },
        {
            stripTrailingSlashes: false
        }
    )
});


app.controller('CatCtrl',
    ['$scope', '$http', '$window', 'UserRegisterFactory', 'UserLogInFactory', 'Catsfactory', 'Catfactory',
    function($scope, $http, $window, UserRegisterFactory, UserLogInFactory, Catsfactory, Catfactory) {

        $http.defaults.headers.common['Authorization'] = $window.localStorage['jwt_token'];
        $http.defaults.headers.post['Content-Type'] = 'application/json';

    // logged in user
        $scope.loggedInUser = $window.localStorage.getItem('username') || '';

    // oauth api
        $scope.checkIfLogIn = function() {
            return localStorage.getItem('jwt_token')
        };
        $scope.authRegister = function(authUsername, authPassword) {
            var data = {
                "username": authUsername,
                "password": authPassword
            };
            UserRegisterFactory.post(data)
                .$promise.then(function(response) {
                    console.log(response);
                    $scope.authLogin(authUsername, authPassword)
                }, function (e) {
                    console.log(e)
                })
        };

        $scope.authLogin = function(authUsername, authPassword) {
            var data = {
                "username": authUsername,
                "password": authPassword
            };
            UserLogInFactory.post(data)
                .$promise.then(function(response) {
                    $http.defaults.headers.common['Authorization'] = 'JWT ' + response.token;
                    $window.localStorage['jwt_token'] = 'JWT ' + response.token;
                    $window.localStorage['username'] = authUsername;
                    $scope.loggedInUser = authUsername;
                    $scope.initCats();
                }, function (e) {
                    $http.defaults.headers.common['Authorization'] = '';
                    $window.localStorage.removeItem('jwt_token');
                    $window.localStorage.removeItem('username');
                    $scope.loggedInUser = '';
                    console.log(e)
                })
        };
        $scope.authLogout = function() {
            $window.localStorage.removeItem('jwt_token');
            $window.localStorage.removeItem('username');
            $scope.loggedInUser = ''
        };

    // Set cats list
        $scope.catsList = [];
        $scope.initCats = function() {
            if ($scope.loggedInUser) {
                var cats_list = Catsfactory.query({});
                angular.forEach(cats_list,
                    function(item){
                        item.showe = false;
                    }
                );
                $scope.catsList = cats_list
            }
        };
        $scope.initCats();
    // clear fluffy is > 10
        $scope.clearCatFluffy = function (fluffy) {
            var fluffy_input = angular.element( document.querySelector( '.add-new-cat .cat-fluffy' ) );
            if (fluffy > 10 ) {
                fluffy_input.addClass('is-invalid');
            } else {
                fluffy_input.removeClass('is-invalid');
            }
        };
    // Create cat
        $scope.createCat = function(name, breed, age, fluffy) {
            if (name) {
                var data = {
                    name:   name    || '',
                    breed:  breed   || '',
                    age:    age     || '',
                    fluffy: fluffy  || '',
                    gone:   false
                };
                Catsfactory.put(data)
                    .$promise
                    .then(function(new_cat) {
                        $scope.catsList.push(new_cat)
                        }, function(e) {
                            console.log(e)
                    }
                );
            }
        };
    // Change cat
        $scope.submitCatChange = function (index, cat_id, name, breed, age, fluffy) {
            var cat = $scope.catsList[index];
            var data = {
                pk: cat_id,
                name: name || cat.name,
                age: age || cat.age,
                breed: breed || cat.breed,
                fluffy: fluffy || cat.fluffy
            };
            var patched_cat = Catfactory.patch(data);
            cat.name    = patched_cat.name;
            cat.breed   = patched_cat.breed;
            cat.age     = patched_cat.age;
            cat.fluffy  = patched_cat.fluffy;
            cat.showe = false
        };
    // restore cat input
        $scope.changeCatName = {};
        $scope.changeCatAge = {};
        $scope.changeCatBreed = {};
        $scope.changeCatFluffy = {};
        $scope.stopTouchingCat = function(index) {
            var cat = $scope.catsList[index];
            $scope.changeCatName[cat.id] = cat.name;
            $scope.changeCatAge[cat.id] = cat.age;
            $scope.changeCatBreed[cat.id] = cat.breed;
            $scope.changeCatFluffy[cat.id] = cat.fluffy;
            cat.showe = false
        };
    // remove cat
        $scope.removeCat = function(index, cat_id) {
            Catfactory.delete({pk: cat_id})
                .$promise.then(
                    function(r) {
                        $scope.catsList.splice(index, 1);
                    }, function (e) {
                        console.log(e)
                    }
                );
        }
}]);
