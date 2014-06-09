function Sprint(name, tasks) {
	this.name = ko.observable(name);
	this.tasks = ko.observableArray([]);
	for (var i=0; i<tasks.length; i++) {
		this.tasks.push(Task(tasks[i]));
	}
}

function Task(taskData) {
	var self = this;

	self.title = ko.observable(taskData.title);
	self.estimated = ko.observable(
		parseInt((taskData.estimated || 0) / 3600)
	);
	self.spent = ko.observable(
		parseInt((taskData.spent || 0) / 3600)
	);
	self.ratio = ko.computed(function() {
		if (self.estimated > 0 && self.spent > 0) {
			return (self.spent / self.estimated) * 100;
		}
		return null;
	});

	// self.subtasks = ko.observableArray([]);
	// if (taskData.subtasks && taskData.subtasks.length > 0) {
	// 	for (var i=0; i<taskData.subtasks.length; i++) {
	// 		self.subtasks.push(taskData.subtasks[i]);
	// 	}
	// }
}

function EstimatesViewModel(containerId) {
	var self = this;

	ViewElement.call(self, containerId);

	self.sprints = ko.observableArray([]);
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
		if (self.phrase().length < 3) {
			self.reportError(
				"At least 3 characters required"
			);
			return;
		}
		$.getJSON('/search/' + self.phrase(), self.renderTasks);
	};

	self.renderTasks = function(response) {
		for (var i=0; i<response.length; i++) {
			self.sprints.push(new Sprint(response[i].name, response[i].tasks));
		}
	};
}
EstimatesViewModel.prototype = Object.create(ViewElement.prototype);
EstimatesViewModel.prototype.constructor = EstimatesViewModel;