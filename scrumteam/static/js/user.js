function User(login, role) {
    var self = this;
    self.login = ko.observable(login);
    self.role = ko.observable(role);
}

function UserViewModel(containerId) {
    var self = this;

    ViewElement.call(self, containerId);

    self.url ='/users';
    self.tmpl = 'static/users.html';
    self.users = ko.observableArray([]);
    
    self.init = function() {
        $.getJSON(self.url, function (data) {
            self.container.load(self.tmpl, function () {
                for (var i=0; i<data.length; i++) {     
                    var d = data[i];
                    self.users().push(
                        new User(d['login'], d['role'])                            
                    );
                }
                ViewElement.prototype.init.call(self);
            });
        });
    }
}
 UserViewModel.prototype = new ViewElement();
 UserViewModel.prototype.constructor = UserViewModel;        

