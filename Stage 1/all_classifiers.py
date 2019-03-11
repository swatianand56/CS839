import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn import linear_model

from sklearn.model_selection import StratifiedKFold


CLF = {
	"DT" : {"name": "Decision Tree", "precision": [], "recall": []},
	"RF" : {"name": "Random Forest", "precision": [], "recall": []},
	"SVM" : {"name": "Support Vector", "precision": [], "recall": []},
	"LR" : {"name": "Linear Regression", "precision": [], "recall": []},
	"LOR" : {"name": "Logistic Regression", "precision": [], "recall": []},
	"NN" : {"name": "Neural Network", "precision": [], "recall": []}
}

class Classifiers:

	def __init__(self, train_fname, test_fname):
		self.input_data = pd.read_csv(train_fname)
		self.test_data = pd.read_csv(test_fname)
		self.X_train = self.input_data.drop(['label', 'Unnamed: 0', 'position', 'token', 'fid'], axis=1)
		self.y_train = self.input_data[['label']]

		self.X_test = self.test_data.drop(['label', 'Unnamed: 0', 'position', 'token', 'fid'], axis=1)
		self.y_test = self.test_data[['label']]

	def decision_tree(self, xtr, xts, ytr, yts):
		clf = DecisionTreeClassifier(criterion="entropy")
		clf.fit(xtr, ytr)
		# y_pred = clf.predict(xts)
		y_pred = (clf.predict_proba(xts)[:,1] >= 0.78).astype(bool)
		return (precision_recall_fscore_support(yts, y_pred, average='binary'))

	def random_forest(self, xtr, xts, ytr, yts):
		clf = clf = RandomForestClassifier(n_estimators = 1000, criterion="entropy", bootstrap=False)
		clf.fit(xtr, ytr.values.ravel())

		y_pred = (clf.predict_proba(xts)[:,1] >= 0.78).astype(bool)
		feature_list = list(self.X_test.columns)
		feature_importance = clf.feature_importances_

		return (precision_recall_fscore_support(yts, y_pred, average='binary'))
		
	def support_vector(self, xtr, xts, ytr, yts):
		clf = svm.SVC(gamma='scale', tol=0.00001, probability=True)
		clf.fit(xtr, ytr.values.ravel())

		y_pred = (clf.predict_proba(xts)[:,1] >= 0.78).astype(bool)
		return (precision_recall_fscore_support(yts, y_pred, average='binary'))

	def neural_network(self, xtr, xts, ytr, yts):
		clf = MLPClassifier(solver='adam', activation='relu', alpha=0.0001, hidden_layer_sizes=(15,15), random_state=42, max_iter=500)
		clf.fit(xtr, ytr.values.ravel())

		y_pred = (clf.predict_proba(xts)[:,1] >= 0.78).astype(bool)
		return (precision_recall_fscore_support(yts, y_pred, average='binary'))

	def linear_regression(self, xtr, xts, ytr, yts):
		clf = linear_model.LinearRegression()
		clf.fit(xtr, ytr.values.ravel())

		y_pred = clf.predict(xts)
		y_binary_pred = [1 if p > 0.78 else 0 for p in y_pred]
		return (precision_recall_fscore_support(yts, y_binary_pred, average='binary'))

	def logistic_regression(self, xtr, xts, ytr, yts):
		clf = linear_model.LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
		clf.fit(xtr, ytr.values.ravel())

		y_pred = (clf.predict_proba(xts)[:,1] >= 0.78).astype(bool)
		return (precision_recall_fscore_support(yts, y_pred, average='binary'))

	def print_results(self, clf, result):
		print("{classifier: <20} {precision:.5f} {recall:.5f}".format(classifier=CLF[clf]["name"], precision=result[0], recall=result[1]))

	def run_kfold(self, classifier):
		N = 10
		skf = StratifiedKFold(n_splits=N)
		X_numpy = self.X_train.values
		y_numpy = self.y_train.values

		for train_index, test_index in skf.split(X_numpy, y_numpy):
			Xtr, Xts = X_numpy[train_index], X_numpy[test_index]
			ytr, yts = y_numpy[train_index], y_numpy[test_index]
			Xtr = pd.DataFrame(Xtr)
			Xts = pd.DataFrame(Xts)
			ytr = pd.DataFrame(ytr)
			yts = pd.DataFrame(yts)

			if classifier == "DT": res = self.decision_tree(Xtr, Xts, ytr, yts)
			if classifier == "SVM": res = self.support_vector(Xtr, Xts, ytr, yts)
			if classifier == "RF": res = self.random_forest(Xtr, Xts, ytr, yts)
			if classifier == "NN": res = self.neural_network(Xtr, Xts, ytr, yts)
			if classifier == "LR": res = self.linear_regression(Xtr, Xts, ytr, yts)
			if classifier == "LOR": res = self.logistic_regression(Xtr, Xts, ytr, yts)

			CLF[classifier]["precision"].append(res[0])
			CLF[classifier]["recall"].append(res[1])

		[self.print_results(classifier, [p, r]) for p, r in zip(CLF[classifier]["precision"], CLF[classifier]["recall"])]
		print()
		self.print_results(classifier, [sum(CLF[classifier]["precision"])/N, sum(CLF[classifier]["recall"])/N])

	def run(self, classifier):
		if classifier == "DT": self.print_results("DT", self.decision_tree(self.X_train, self.X_test, self.y_train, self.y_test))
		if classifier == "SVM": self.print_results("SVM", self.support_vector(self.X_train, self.X_test, self.y_train, self.y_test))
		if classifier == "RF": self.print_results("RF", self.random_forest(self.X_train, self.X_test, self.y_train, self.y_test))
		if classifier == "NN": self.print_results("NN", self.neural_network(self.X_train, self.X_test, self.y_train, self.y_test))
		if classifier == "LR": self.print_results("LR", self.linear_regression(self.X_train, self.X_test, self.y_train, self.y_test))
		if classifier == "LOR": self.print_results("LOR", self.logistic_regression(self.X_train, self.X_test, self.y_train, self.y_test))
