#! /bin/bash

BASEDIR=..

# convert datasets to feature vectors
echo "Extracting features..."
python3 extract-features.py $BASEDIR/data/train/ > train.feat
python3 extract-features.py $BASEDIR/data/devel/ > devel.feat

# train models
echo "Training models..."
python3 train.py train.feat model

# run models
echo "Running CRF models..."
python3 predict.py devel.feat model_experiment1.crf > predictions_devel1crf.out 
python3 predict.py devel.feat model_experiment2.crf > predictions_devel2crf.out 
python3 predict.py devel.feat model_experiment3.crf > predictions_devel3crf.out 
python3 predict.py devel.feat model_experiment4.crf > predictions_devel4crf.out 
python3 predict.py devel.feat model_experiment5.crf > predictions_devel5crf.out 

echo "Running LR models..."
python3 predict.py devel.feat model_experiment1.lrg > predictions_devel1lrg.out
python3 predict.py devel.feat model_experiment2.lrg > predictions_devel2lrg.out 
python3 predict.py devel.feat model_experiment3.lrg > predictions_devel3lrg.out 
python3 predict.py devel.feat model_experiment4.lrg > predictions_devel4lrg.out 
python3 predict.py devel.feat model_experiment5.lrg > predictions_devel5lrg.out 

# evaluate models
echo "Evaluating CRF models..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel1crf.out > evaluation_devel1crf.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel2crf.out > evaluation_devel2crf.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel3crf.out > evaluation_devel3crf.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel4crf.out > evaluation_devel4crf.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel5crf.out > evaluation_devel5crf.stats

echo "Evaluating LR models..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel1lrg.out > evaluation_devel1lrg.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel2lrg.out > evaluation_devel2lrg.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel3lrg.out > evaluation_devel3lrg.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel4lrg.out > evaluation_devel4lrg.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel predictions_devel5lrg.out > evaluation_devel5lrg.stats

