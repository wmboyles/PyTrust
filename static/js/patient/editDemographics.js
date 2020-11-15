var app = angular.module(
    "editDemographicsApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("editDemographicsCtrl", ($scope, $http) => {
    // load full patient object if it exists
    // if not, load just the user object
    $scope.load_self = () => {
        $http.get("/api/patients/self").then(
            (res) => {
                var patient = res.data;
                patient.dob = new Date(patient.dob);
                $scope.patient = patient;

                $scope.existing_patient = true;
            },
            (err) => {
                $scope.patient = {};
                $scope.patient.user = err.data;
                $scope.existing_patient = false;
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
        var fn = $http.post;
        if ($scope.existing_patient) {
            var fn = $http.put;
        }

        fn("/api/patients", $scope.patient).then(
            (res) => {
                $scope.error_message = "";
                $scope.success_message = "Successfully updated demographics";
                $scope.load_self();
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // delete patient self
    $scope.delete_self = () => {
        if (!$scope.existing_patient) {
            $scope.error_message =
                "You already don't have patient demographic information";
            $scope.success_message = "";
            return;
        }

        if (
            confirm(
                "Are you sure you want to delete your patient demographic information? You will still have an account, but all your office vists and prescriptions will be lost."
            )
        ) {
            $http.delete("/api/patients/" + $scope.patient.user.id).then(
                (res) => {
                    $scope.error_message = "";
                    $scope.success_message =
                        "Successfully deleted patient demographic information";
                    $scope.load_self();
                },
                (err) => {
                    $scope.error_message =
                        "Could not delete patient demographic information";
                    $scope.success_message = "";
                }
            );
        }
    };

    // runs on page load
    $scope.load_states();
    $scope.load_drug_types();
    $scope.load_blood_types();
    $scope.load_pharmacies();
    $scope.load_ethnicities();
    $scope.load_genders();

    $scope.load_self();
});
