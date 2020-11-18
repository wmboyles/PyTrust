var app = angular.module(
    "editDemographicsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
// load full personnel personnel object if it exists
// if not, load just the user object
app.factory("waitForSelfToLoad", ($http) => {
    var load_self = () => {
        return $http.get("/api/personnel/self").then(
            (res) => {
                return [true, res.data];
            },
            (err) => {
                return [false, err.data];
            }
        );
    };

    return { load_self: load_self };
});
app.controller("editDemographicsCtrl", ($scope, $http, waitForSelfToLoad) => {
    var check_personnel = (personnel) => {
        // TODO
    };

    // load all the hospitals
    // $scope.personnel.user MUST exist to call this method
    $scope.load_workplaces = () => {
        var url = "/api/";
        if ($scope.personnel.user.role == "hcp") {
            url += "hospitals";
        } else if ($scope.personnel.user.role == "pharmacist") {
            url += "pharmacies";
        } else {
            $scope.error_message = "No workplaces associated with user role";
        }

        $http.get(url).then(
            (res) => {
                $scope.workplaces = res.data;
            },
            (err) => {
                $scope.workplaces = [];
            }
        );
    };

    // load all the states
    $scope.load_states = () => {
        $http.get("/api/states").then(
            (res) => {
                $scope.states = res.data;
            },
            (err) => {
                $scope.states = [];
            }
        );
    };

    // when submit button is pressed
    $scope.submit_demographics = () => {
        var err = check_personnel($scope.personnel);
        if (err) {
            $scope.error_message = err;
            $scope.success_message = "";
        }

        var fn = $http.post;
        if ($scope.existing_personnel) {
            var fn = $http.put;
        }

        fn("/api/personnel", $scope.personnel).then(
            (res) => {
                $scope.error_message = "";
                $scope.success_message = "Successfully updated demographics";

                var self_promise = waitForSelfToLoad.load_self();
                self_promise.then((res) => {
                    $scope.existing_personnel = res[0];
                    if ($scope.existing_personnel) {
                        $scope.personnel = res[1];
                    } else {
                        $scope.personnel = {};
                        $scope.personnel.user = res[1];
                    }
                });
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // delete personnel self
    $scope.delete_self = () => {
        if (!$scope.existing_personnel) {
            $scope.error_message =
                "You already don't have personnel demographic information";
            $scope.success_message = "";
            return;
        }
        if (
            confirm(
                "Are you sure you want to delete your personnel demographic information? You will still have an account."
            )
        ) {
            $http.delete("/api/personnel/" + $scope.personnel.user.id).then(
                (res) => {
                    $scope.error_message = "";
                    $scope.success_message =
                        "Successfully deleted personnel demographic information";

                    var self_promise = waitForSelfToLoad.load_self();
                    self_promise.then((res) => {
                        $scope.existing_personnel = res[0];
                        if ($scope.existing_personnel) {
                            $scope.personnel = res[1];
                        } else {
                            $scope.personnel = {};
                            $scope.personnel.user = res[1];
                        }
                    });
                },
                (err) => {
                    $scope.error_message =
                        "Could not delete personnel demographic information";
                    $scope.success_message = "";
                }
            );
        }
    };

    // runs on pageload
    $scope.load_states();
    var self_promise = waitForSelfToLoad.load_self();
    self_promise.then((res) => {
        $scope.existing_personnel = res[0];
        if ($scope.existing_personnel) {
            $scope.personnel = res[1];
        } else {
            $scope.personnel = {};
            $scope.personnel.user = res[1];
        }

        $scope.load_workplaces();
    });
});
