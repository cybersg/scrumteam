function GenerateHistoryViewModel(containerId) {
    var self = this;
    
    ViewElement.call(self, containerId);

    self.url = '/generate_history';
    self.tmpl = 'static/generate_history.html';

    self.login = ko.observable();
    self.password = ko.observable();

    self.progressId = 0;
    self.intervalId = null;

    self.currentProgress = ko.observable(0);
    self.inProgress = ko.observable(false);
    self.percentComplete = ko.computed(function() {
        return self.currentProgress() + '%';
    });
    self.percentCompleteMsg = ko.computed(function() {
        if (self.currentProgress() == 0) {
            return "Generating history. Please wait while\
            connecting to external client..."
        }
        if (self.currentProgress() >= 100) {
            return "Process finished successfully";
        }
        return self.currentProgress() + ' percent completed';
    });

    self.init = function() {
        self.container.load(self.tmpl, function () {
            ViewElement.prototype.init.call(self);
        });
    };
    
    self.progress = function() {
        $.getJSON(
            self.url + '/' + self.progressId,
            function (data) {
                var percent = 0;
                if (data.current > 0) {
                    percent =  parseInt(100 / (data.total / data.current));
                    self.currentProgress(percent);
                    if (percent >= 100) {
                        clearInterval(self.intervalId);
                        self.currentProgress(0);
                        self.inProgress(false);                     
                    }
                }
                else {

                }
            }
        ).fail(function() {
            clearInterval(self.intervalId);
            self.reportError("Server error")
        });
    }
    self.generateHistoryInit = function() {
        if (!self.login() || !self.password()) {
            self.alertBadInput();
            return false;
        }
        self.clearErrMsg();
        $.ajax({
            url: self.url,
            data: JSON.stringify(
                {ext_login: self.login(), ext_password: self.password()}
            ),
            dataType: 'json',
            contentType: 'application/json',
            type: 'POST'
        }).done(function(data) {
            self.progressId = data.task_id;
            if (self.progressId) {
                self.intervalId = setInterval(self.progress, 500);
                self.inProgress(true);
            }
            else{
                self.reportError("Undefined task id");
            }
        }).fail(function(j, t, s) {
            self.reportError("Generating history failed");
        });
    };

    self.errDiv = $('#err-msg');
    self.errCls = 'alert alert-danger';
    self.alertBadInput = function() {
        self.reportError("Login and password are required!");
    };

    self.reportError = function(msg) {
        self.clearErrMsg();
        self.errDiv.addClass(self.errCls);
        self.errDiv.html(msg);
        self.currentProgress(0);
        self.inProgress(false); 
    }

    self.clearErrMsg = function() {
        if (self.errDiv.hasClass(self.errCls)) {
            self.errDiv.removeClass(self.errCls);
        }
        self.errDiv.html('');
    };
            
}
GenerateHistoryViewModel.prototype = new ViewElement();
GenerateHistoryViewModel.prototype.constructor = GenerateHistoryViewModel;

    
