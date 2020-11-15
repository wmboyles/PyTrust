var app = angular.module(
    "manageUsersApp",
    [],
    // Change the delimiter symbols to [[ and ]]
    ($interpolateProvider) => {
        $interpolateProvider.startSymbol("[[");
        $interpolateProvider.endSymbol("]]");
    }
);
app.controller("manageUsersCtrl", ($scope, $http) => {
    // Is the user being edited or viewed?
    $scope.get_template = (user) => {
        if (user.id === $scope.selected_user.id) {
            return "edit";
        } else {
            return "view";
        }
    };

    // check that user fields are valid
    var check_user = (user) => {
        var err = [];
        if (!user.username) {
            err.push("User must have a username");
        }
        if (!user.password && !user.password_hash) {
            err.push("User must have a password");
        }
        if (!user.role) {
            err.push("User must have a role");
        }

        return err.join(". ");
    };

    // load all the users from the DB
    $scope.load_users = () => {
        $http.get("/api/users").then(
            (res) => {
                $scope.users = res.data;
            },
            (err) => {
                $scope.users = [];
            }
        );
    };

    // load all the user roles from the db
    $scope.load_user_roles = () => {
        $http.get("/api/user_roles").then(
            (res) => {
                $scope.roles = res.data;
            },
            (err) => {
                $scope.roles = [];
            }
        );
    };

    // user edit operation is cancelled
    $scope.reset_edit = () => {
        $scope.selected_user = {};
    };

    // user has been submitted
    $scope.reset_create = () => {
        $scope.user = {};
    };

    // reset success and error messages
    $scope.reset_messages = () => {
        $scope.error_message = "";
        $scope.success_message = "";
    };

    // when user is selected for editing
    $scope.edit_user = (user) => {
        $scope.selected_user = angular.copy(user);
    };

    // user has been edited and now should be saved
    $scope.save_user = () => {
        var err = check_user($scope.selected_user);
        if (err) {
            $scope.error_message = err;
            return;
        }

        $http.put("/api/users", $scope.selected_user).then(
            (res) => {
                $scope.reset_edit();
                $scope.load_users();
                $scope.error_message = "";
                $scope.success_message = "Successfully edited user";
            },
            (err) => {
                $scope.error_message = "" + err.data;
                $scope.success_message = "";
            }
        );
    };

    // user is being deleted
    $scope.delete_user = (user) => {
        if (confirm("Are you sure you want to delete this user?")) {
            $http.delete("/api/users/" + user.id).then(
                (res) => {
                    $scope.load_users();
                    $scope.error_message = "";
                    $scope.success_message = "Successfully deleted user";
                },
                (err) => {
                    $scope.error_message = err.data;
                    $scope.success_message = "";
                }
            );
        }
    };

    // a new user has been submitted for creation
    $scope.add_user = () => {
        $http.post("/api/users", $scope.user).then(
            (res) => {
                $scope.reset_create();
                $scope.load_users();
                $scope.error_message = "";
                $scope.success_message = "Successfully created user";
            },
            (err) => {
                $scope.error_message = err.data;
                $scope.success_message = "";
            }
        );
    };

    // Runs on page load
    $scope.reset_edit();
    $scope.reset_create();
    $scope.reset_messages();

    $scope.load_users();
    $scope.load_user_roles();
});
