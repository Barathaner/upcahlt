#!/usr/bin/env python3

import os
import sys
import json
from ML_model import *

# Load parameter settings from the JSON file
params_file = "crf_params.json"
with open(params_file, "r") as file:
    param_settings = json.load(file)

# Get file where data is located
datafile = sys.argv[1]

for experiment, params in param_settings.items():
    # Generate a unique modelfile name for each experiment
    modelfile = f"{sys.argv[2]}_{experiment}.crf"

    # Make sure the model file does not exist, so ML_model creates an empty one
    if os.path.isfile(modelfile):
        os.remove(modelfile)

    # Initialize the model
    model = ML_model(modelfile)

    # Train and store the model with the current experiment's parameters
    model.train(datafile, modelfile, params)

    print(f"Model trained and saved for {experiment} with parameters: {params}")
