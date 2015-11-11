from featurizer import FeatureGenerator
from loader import GraphLoader
import random
from sklearn.ensemble import ExtraTreesClassifier

class EdgePredictor(object):
    # FeatureGenerator from featurizer.py
    featurizer = None

    # Influence graph
    IG = None

    # For now just easy ensemble method
    classifier = ExtraTreesClassifier()

    # Tuple Xtrain, Ytrain, set when self.train() is called by the client
    train_data = None

    # Tuple Xtest, YTest set when self.train() is called by the client
    test_data = None

    def __init__(self, IG):
        random.seed(0)
        self.IG = IG
        self.featurizer = FeatureGenerator(IG)

    def nrandom_negative_examples(self, m):
        """
        :return: list of m, (u,v) randomly selected negative examples (edges that don't exist in the graph)
        """
        examples = []
        while len(examples) < m:
            u, v = random.sample(self.IG.node, 2)
            if self.IG.edge_exists(u,v):  continue
            examples.append((u,v))
        return examples

    def train(self):
        """
        Generates features, randomly splits datasets, and fits classifier
        :return:
        """
        # Generate positive, negative examples
        pos_exs = self.featurizer.feature_matrix(self.IG.edges)
        mpos = len(pos_exs)
        neg_exs = self.featurizer.feature_matrix(self.nrandom_negative_examples(mpos))
        mneg = len(neg_exs)

        # Randomly Shuffle data

        # Split into train set and test set
        self.Xtr = None
        self.Ytr = None
        self.classifier.fit(self.Xtr, self.Ytr)

        self.Xtest = None
        self.Ytest = None

    def predict(self, u, v):
        """
        :return: Returns {1,0} if there should be an influence edge between u,v
        """
        features = self.featurizer.get_features(u,v)
        return self.classifier.predict(features)

    def evaluate_model(self):
        """
        returns auc score of current model
        """
        # Todo ROC AUC Curve


if __name__ == '__main__':
    IG = GraphLoader(verbose=True).load_networkx_influence_graph(pruned=True)
    ep = EdgePredictor(IG)
    ep.evaluate_model()

