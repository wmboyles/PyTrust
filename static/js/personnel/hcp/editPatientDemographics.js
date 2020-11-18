var app = angular.module(
    "editPatientDemographicsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.factory("waitForLoadPatients", ($http) => {
    var load_patients = () => {
        return $http.get("/api/patients").then(
            (res) => {
                var patients = res.data;
                for (var i in patients) {
                    patients[i].dob = new Date(patients[i].dob);
                }

                return patients;
            },
            (err) => {
                return [];
            }
        );
    };

    return { load_patients: load_patients };
});
app.controller(
    "editPatientDemographicsCtrl",
    ($scope, $http, waitForLoadPatients) => {
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

        // load all the drug types from the db
        $scope.load_drug_types = () => {
            $http.get("/api/drug_types").then(
                (res) => {
                    $scope.drug_types = res.data;
                },
                (err) => {
                    $scope.drug_types = [];
                }
            );
        };

        // load all the blood types from the db
        $scope.load_blood_types = () => {
            $http.get("/api/blood_types").then(
                (res) => {
                    $scope.blood_types = res.data;
                },
                (err) => {
                    $scope.blood_types = [];
                }
            );
        };

        // load all the pharmacist from the db
        $scope.load_pharmacies = () => {
            $http.get("/api/pharmacies").then(
                (res) => {
                    $scope.pharmacies = res.data;
                },
                (err) => {
                    $scope.pharmacies = [];
                }
            );
        };

        // load all the ethnicities from the db
        $scope.load_ethnicities = () => {
            $http.get("/api/ethnicities").then(
                (res) => {
                    $scope.ethnicities = res.data;
                },
                (err) => {
                    $scope.ethnicities = [];
                }
            );
        };

        // load all the genders from the db
        $scope.load_genders = () => {
            $http.get("/api/genders").then(
                (res) => {
                    $scope.genders = res.data;
                },
                (err) => {
                    $scope.genders = [];
                }
            );
        };

        // when submit button is pressed
        $scope.submit_demographics = () => {
            $scope.patient.dob = Intl.DateTimeFormat("en-US").format(
                $scope.patient.dob
            );

            $http.put("/api/patients", $scope.patient).then(
                (res) => {
                    $scope.error_message = "";
                    $scope.success_message =
                        "Successfully updated patient demographics";

                    $scope.patients = [];
                    var patients_promise = waitForLoadPatients.load_patients();
                    patients_promise.then((res2) => {
                        $scope.patients = res2;

                        for (var i in $scope.patients) {
                            if (
                                $scope.patients[i].user.id === res.data.user.id
                            ) {
                                $scope.patient = $scope.patients[i];
                            }
                        }
                    });
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        };

        // runs on page load
        $scope.load_states();
        $scope.load_drug_types();
        $scope.load_blood_types();
        $scope.load_pharmacies();
        $scope.load_ethnicities();
        $scope.load_genders();
        var patients_promise = waitForLoadPatients.load_patients();
        patients_promise.then((res) => {
            $scope.patients = res;
        });
    }
);
