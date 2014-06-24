var searchPhrase = null;
function Sprint(name, tasks) {
	var self = this;

	self.name = ko.observable(name);
	self.tasks = ko.observableArray();
	for (var i=0; i<tasks.length; i++) {
		self.tasks.push(new Task(tasks[i]));
	}
	self.tasks.sort(function(a, b) {
		return a.title() < b.title() ? -1 : 1;
	});
}

function Task(taskData, phrase) {
	var self = this;
	self.title = ko.observable(taskData.title);
	if (searchPhrase) {
		var re = new RegExp(searchPhrase ,"gi");
		self.title(self.title().replace(
			re, "<b>$&</b>"
		));
	}
	self.estimated = ko.observable(
		parseInt((taskData.estimated || 0) / 3600)
	);
	self.spent = ko.observable(
		parseInt((taskData.spent || 0) / 3600)
	);
	self.ratio = ko.computed(function() {
		if (self.estimated() > 0 && self.spent() > 0) {
			return ((self.spent() / self.estimated()) * 100).toFixed(0) + '%';
		}
		return null;
	});

	self.subtasks = ko.observableArray();
	if (taskData.subtasks && taskData.subtasks.length > 0) {
		for (var i=0; i<taskData.subtasks.length; i++) {
			self.subtasks.push(new Task(taskData.subtasks[i]));
		}
	}
	self.subtasks.sort(function(a, b) {
		return a.title() < b.title() ? -1 : 1;
	});
}

function EstimatesViewModel(containerId) {
	var self = this;

	ViewElement.call(self, containerId);

	self.availSprints = ko.observableArray([]);
	self.selectedSprint = ko.observable();

	self.url = '/estimates';
	self.tmpl = 'static/estimates.html';
	
	self.init = function() {
		$.getJSON(self.url, function(response) {
			self.container.load(self.tmpl, function() {
				for (var i=0; i<response.length; i++) {
					self.availSprints.push(response[i]);
				}
				ViewElement.prototype.init.call(self);
			});
		});
	}

	self.showHistory = function() {
		if (self.selectedSprint() == 0) {
			return;
		}
		$.getJSON('/history/' + self.selectedSprint(), self.renderTasks);
	}

	self.phrase = ko.observable();
	self.searchTasks = function(formEl) {
		searchPhrase = self.phrase();
		self.clearErrMsg();
		if (self.phrase().length < 3) {
			self.reportError(
				"At least 3 characters required"
			);
			return;
		}
		$.getJSON('/search/' + self.phrase(), self.renderTasks);
	};

	self.sprints = ko.observableArray();
	self.renderTasks = function(response) {
		self.sprints.removeAll();
		for (var i=0; i<response.length; i++) {
			var tasks = response[i].tasks;
			if (!tasks || !tasks.length) {
				continue;
			}
			self.sprints.push(
				new Sprint(response[i].name, tasks)
			);
		}
		self.sprints.sort(function(a, b) {
			return a.name() < b.name() ? -1 : 1;
		});
	};
}
EstimatesViewModel.prototype = Object.create(ViewElement.prototype);
EstimatesViewModel.prototype.constructor = EstimatesViewModel;