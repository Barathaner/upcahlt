python3 predict.py devel.feat model_experiment1.crf > devel1crf.out 
python3 predict.py devel.feat model_experiment2.crf > devel2crf.out 
python3 predict.py devel.feat model_experiment3.crf > devel3crf.out 
python3 predict.py devel.feat model_experiment4.crf > devel4crf.out 
python3 predict.py devel.feat model_experiment5.crf > devel5crf.out 

python3 predict.py devel.feat model_experiment1.lrg > devel1lrg.out
python3 predict.py devel.feat model_experiment2.lrg > devel2lrg.out 
python3 predict.py devel.feat model_experiment3.lrg > devel3lrg.out 
python3 predict.py devel.feat model_experiment4.lrg > devel4lrg.out 
python3 predict.py devel.feat model_experiment5.lrg > devel5lrg.out 

python3 ../util/evaluator.py NER ../data/devel devel1crf.out > devel1crf.stats
python3 ../util/evaluator.py NER ../data/devel devel2crf.out > devel2crf.stats
python3 ../util/evaluator.py NER ../data/devel devel3crf.out > devel3crf.stats
python3 ../util/evaluator.py NER ../data/devel devel4crf.out > devel4crf.stats
python3 ../util/evaluator.py NER ../data/devel devel5crf.out > devel5crf.stats
python3 ../util/evaluator.py NER ../data/devel devel1lrg.out > devel1lrg.stats
python3 ../util/evaluator.py NER ../data/devel devel2lrg.out > devel2lrg.stats
python3 ../util/evaluator.py NER ../data/devel devel3lrg.out > devel3lrg.stats
python3 ../util/evaluator.py NER ../data/devel devel4lrg.out > devel4lrg.stats
python3 ../util/evaluator.py NER ../data/devel devel5lrg.out > devel5lrg.stats


