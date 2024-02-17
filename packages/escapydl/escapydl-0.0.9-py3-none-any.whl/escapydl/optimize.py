# eSCAPyDL - a Deep Learning Side-Channel Analysis Python Framework
# Copyright (C) 2023  Weissbart Léo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys
import inspect
import shutil
import json
import logging 
logging.basicConfig(format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import time, datetime
import argparse

import torch
from torch.utils import tensorboard
import Dataset
import Callbacks
import Optuna_models

import optuna
from optuna.trial import TrialState

def main():
    #Parse arguments
    #TODO: remove default dataset and model and default to help
    parser = argparse.ArgumentParser(description='eSCAPyDL: Deep Leaning SCA PyTorch framework. Training models for tracesets with SCA metrics.')
    parser.add_argument('-d', '--dataset', help='The dataset to use for training. (All datasets have different functions for intermediate value and power model).', default="dpav4")
    parser.add_argument('-m', '--model', help='Type of NN to use (choices: MLP, CNN) CNN is the onetrace implementation.', default=None)
    parser.add_argument('-s', '--study', help='Optuna study name, for parallelization of study')
    parser.add_argument('-u', '--database', help='Optuna database name', default="sqlite:///cnn_sca.db")
    parser.add_argument('-j', '--json', help='Input data from json file')
    parser.add_argument('-a', '--timestamp', help='Timestamp of the experiment', default=time.strftime("%Y%m%d_%H%M%S",time.localtime()))
    parser.add_argument('-v', '--verbose', help='Verbose level', action='count', default=0)
    parser.add_argument('-l', '--log', help='Log into a file at path', default='')
    args = parser.parse_args()
    __DL_type__ = args.model
    available_models = [x[0] for x in inspect.getmembers(Optuna_models, inspect.isfunction) if x[0].startswith("make_")]
    assert __DL_type__ in available_models, "Model {} not found, available models are: {}".format(__DL_type__, available_models)
    if args.verbose == 1:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("Dataset").setLevel(logging.DEBUG)
        logging.getLogger("Callbacks").setLevel(logging.DEBUG)
        logging.getLogger("optuna_models").setLevel(logging.DEBUG)
    if args.log != '':
        file_handler = logging.FileHandler(args.log, mode='w', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
        logger.addHandler(file_handler)
    __trs_dataset__ = args.dataset
    db_name = args.database
    study_name = args.study
    if args.json == "None":
        args.json = None
    if args.json != None:
        try:
            with open(args.json, 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            logging.error("Json File '{}' not found".format(args.json))
            exit(1)
    else:
        json_data = {}

    #Main program
    try:
        start_time = datetime.datetime.now().replace(microsecond=0)

        #load traceset
        dataset = Dataset.Dataset(__trs_dataset__,__DL_type__,json_data=json_data)
        parameters = dataset.get_parameters()
        trace_data = dataset.traceset()
        callbacks_params = dataset.get_callbacks()
        hp_search_s = dataset.get_hp_search_s()

        # Create folders
        timestamp = args.timestamp
        filebase = '{}/{}/{}'.format(__trs_dataset__, __DL_type__, timestamp)
        root                = os.getcwd() + '/experiments/' + filebase + '/'
        os.makedirs(root)
        model_folder        = root + 'models/'
        last_model_folder   = root + 'last_models/'
        history_folder      = root + 'history/'
        result_folder       = root + 'results/'
        for folder in [model_folder,model_folder,last_model_folder,history_folder,result_folder]:
            try:
                os.mkdir(folder)
            except:
                pass

        #Create callbacks
        callbacks = Callbacks.init_callbacks(callbacks_params, 
                                   traceset=trace_data,
                                   parameters=parameters, 
                                   exp_path=result_folder, 
                                   writer_path='runs/'+filebase)

        #Train model
        metric, direction = "gge", "minimize"
        objective = Optuna_models.objective_hp(parameters=parameters,
                            hp_search_s=hp_search_s,
                            trace_data=trace_data,
                            callbacks=callbacks,
                            verbose=1,
                            model_name=__DL_type__,
                            metric=metric
                        )
        pruner = optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5, interval_steps=1), patience=30)
        
        if study_name!=None:
            logging.debug("Loading study from name: {}".format(study_name))
            study = optuna.load_study(study_name=study_name, storage=db_name)
        else:
            study_name = "{}_{}_{}".format(__trs_dataset__, __DL_type__, timestamp)
            study = optuna.create_study(sampler=optuna.samplers.TPESampler(), 
                                        direction=direction, 
                                        pruner=pruner, 
                                        study_name=study_name, 
                                        storage=db_name)
        study.optimize(objective, n_trials=100, timeout=None)

        pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
        complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])

        logging.debug("Study statistics: ")
        logging.debug("  Number of finished trials: ", len(study.trials))
        logging.debug("  Number of pruned trials: ", len(pruned_trials))
        logging.debug("  Number of complete trials: ", len(complete_trials))

        logging.debug("Best trial:")
        trial = study.best_trial

        logging.debug("  Value: ", trial.value)

        logging.debug("  Params: ")
        for key, value in trial.params.items():
            logging.debug("    {}: {}".format(key, value))
        
        stop_time = datetime.datetime.now().replace(microsecond=0)
        logger.info("----------------------\n  The operation was \ncompleted successfully\n Clear time {}\n----------------------".format(stop_time-start_time))
    except:
        # Create handler to remove uncessful experiment folder tree if program crashed
        logger.warning("------------------\nException caught\n------------------")
        try:
            if os.path.isdir(root):
                shutil.rmtree(root)
            if os.path.isdir('runs/'+filebase):
                shutil.rmtree('runs/'+filebase)
            logger.warning("------------------\nCurrent experiment folder tree deleted\n------------------")
        except UnboundLocalError:
            pass
        logger.exception('')
    finally:
        logger.info("--------------------\nEnd of main reached!")
    logger.info("--------------------")

if __name__ == "__main__":
    sys.exit(main())