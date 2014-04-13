function User(login, role) {
    var self = this;
    self.login = ko.observable(login);
    self.role = ko.observable(role);
}
function UserViewModel(usersData) {
    var self = this;
    self.idata = usersData;
    self.users = ko.observableArray([]);

    self.clear = function() {
        self.users([]);
    }

    self.load = function() {
        for (var i=0; i<self.idata.length; i++) {
            self.users().push(
                new User(
                    self.idata[i]['login'], self.idata[i]['role']
                )
            );
        }
    }
    self.load(usersData);
    
}

function NotImplementedException(msg) {
    this.message = msg;
}
function VMFactory() {

    this.create =  function(type, args) {
        var obj = null;
        switch (type) {
            case 'users':
                obj =  new UserViewModel(args);
                break;
            default:
                throw new NotImplementedException(
                    "Undefined ViewModel type"
                );
        }
        if (obj != null) {obj.clear();}
        return obj;
    }
}

function AppViewModel() {
    var self = this;

    self.home = function() {
        self.currentMenu(null);
        self.currentSubMenu(null);
        self.submenu([]);
    }

    self.menu = ko.observableArray(['Admin', 'Team'])
    self.currentMenu = ko.observable();
    self.selectMenuItem = function (item, ev) {
        self.currentMenu(item);
        var menu = {
            'Admin': ['Users', 'Generate history'],
            'Team': ['Estimates']
        };
        self.currentSubMenu(null);
        self.submenu(menu[item]);
    }

    self.submenu = ko.observableArray([]);
    self.currentSubMenu = ko.observable();

    self.rdata = null;

    self.loadSubMenuContents = function (menuItem) {
        var resource = menuItem.toLowerCase().replace(/\s/g, '_');
        $.getJSON(resource, function (data) {
            self.rdata = data;
            $('#template-container').load(resource + '.html', function () {
                vmObj = new VMFactory().create(resource, self.rdata);
                vmObj.load();
                ko.applyBindings(vmObj, $('#template-container')[0]);
            });
        });
    }

    
    
}
ko.applyBindings(new AppViewModel());   