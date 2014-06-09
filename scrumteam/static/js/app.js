
requirejs(
    ['user', 'generate_history', 'estimates'], 
    function(user, generate_history, estimates) {
    }
);

function NotImplementedException(msg) {
    this.message = msg;
}
function VMFactory() {

    this.create =  function(type, containerId) {
        var obj = null;
        switch (type) {
            case 'users':
                obj =  new UserViewModel(containerId);
                break;
            case 'generate_history':
                obj = new GenerateHistoryViewModel(containerId);
                break;
            case 'estimates':
                obj = new EstimatesViewModel(containerId);
                break;
            default:
                throw new NotImplementedException(
                    "Undefined ViewModel type"
                );
        }
        return obj;
    };
}

function AppViewModel() {
    var self = this;

    self.home = function() {
        self.currentMenu(null);
        self.currentSubMenu(null);
        self.submenu([]);
    };

    self.menu = ko.observableArray(['Admin', 'Team']);
    self.currentMenu = ko.observable();
    self.selectMenuItem = function (item, ev) {
        self.currentMenu(item);
        var menu = {
            'Admin': ['Users', 'Generate history'],
            'Team': ['Estimates']
        };
        self.currentSubMenu(null);
        self.submenu(menu[item]);
    };

    self.submenu = ko.observableArray([]);
    self.currentSubMenu = ko.observable();

    self.loadSubMenuContents = function (menuItem) {
        self.currentSubMenu(menuItem);
        var resource = menuItem.toLowerCase().replace(/\s/g, '_');
        var vmElement = new VMFactory().create(
            resource, 'template-container-content'
        );
        vmElement.init();
    };
    self.clearErrMsg = null;
}

function ViewElement(containerId) {
    this.containerId = containerId;
    this.container = $('#' + containerId);
}

ViewElement.prototype = {
    url: null,
    tmpl: null,
    errDiv: null,
    errCls: null
};

ViewElement.prototype.init = function () {
    this.errDiv = $('#err-msg');
    this.errCls = 'alert alert-danger';
    ko.applyBindings(this, this.container.parent()[0]);
};

ViewElement.prototype.reportError = function(msg) {
    this.clearErrMsg();
    this.errDiv.addClass(this.errCls);
    this.errDiv.html(msg);
};

ViewElement.prototype.clearErrMsg = function() {
    if (this.errDiv.hasClass(this.errCls)) {
        this.errDiv.removeClass(this.errCls);
    }
    this.errDiv.html('');
};

ko.applyBindings(new AppViewModel());   
