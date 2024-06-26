#####################################################
## Class to store an ngram ME model
#####################################################

import sys
import pycrfsuite
from dataset import *


class CRF:

    ## --------------------------------------------------
    ## Constructor: Load model from file
    ## --------------------------------------------------
    def __init__(self, modelfile=None):

        if modelfile is not None:
            # modelfile given, assume it is an existing model and load it
            self.tagger = pycrfsuite.Tagger()
            self.tagger.open(modelfile)

        else:
            # no model file, create an empty model, waiting to be trained
            self.tagger = None

    ## --------------------------------------------------
    ## train a model on given data, store in modelfile
    ## --------------------------------------------------

    def train(self, datafile, modelfile, params):
        # Load dataset
        ds = Dataset(datafile)
        # Create trainer
        trainer = pycrfsuite.Trainer()

        # Add examples to trainer
        for xseq, yseq, _ in ds.instances():
            trainer.append(xseq, yseq, 0)

        # set parameters
        trainer.select(
            "l2sgd", "crf1d"
        )  # Use L2-regularized SGD and 1st-order dyad features.

        print("Training with following parameters: ", file=sys.stderr)
        for name in trainer.params():
            print(name, trainer.get(name), trainer.help(name), file=sys.stderr)

        # Dynamically set parameters from a provided dictionary
        for param, value in params.items():
            trainer.set(param, value)

        # Training
        trainer.train(modelfile, -1)

    ## --------------------------------------------------
    ## predict best class for each element in xseq
    ## --------------------------------------------------
    def predict(self, xseq):
        if self.tagger is None:
            print("This model has not been trained", file=sys.stderr)
            sys.exit(1)

        return self.tagger.tag(xseq)
