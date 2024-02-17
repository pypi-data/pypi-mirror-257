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
import shutil
import json
import logging 
logging.basicConfig(format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import time, datetime
import argparse
import inspect

import torch
from torch.utils import tensorboard
import Dataset
import Callbacks
import Models
import Utils

def main():
    #Parse arguments
    #TODO: remove default dataset and model and default to help
    parser = argparse.ArgumentParser(description='eSCAPyDL: Deep Leaning SCA PyTorch framework. Training models for tracesets with SCA metrics.')
    parser.add_argument('-d', '--dataset', help='The dataset to use for training. (All datasets have different functions for intermediate value and power model).', default="dpav4")
    parser.add_argument('-m', '--model', help='Type of NN to use (choices: MLP, CNN) CNN is the onetrace implementation.', default=None)
    parser.add_argument('-j', '--json', help='Input data from json file')
    parser.add_argument('-a', '--timestamp', help='Timestamp of the experiment', default=time.strftime("%Y%m%d_%H%M%S",time.localtime()))
    parser.add_argument('-v', '--verbose', help='Verbose level', action='count', default=0)
    parser.add_argument('-l', '--log', help='Log into a file at path', default='')
    args = parser.parse_args()
    available_models = [x[0] for x in inspect.getmembers(Models, inspect.isclass)]
    if args.verbose == 1:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("Dataset").setLevel(logging.DEBUG)
        logging.getLogger("Callbacks").setLevel(logging.DEBUG)
        logging.getLogger("models").setLevel(logging.DEBUG)
        logging.getLogger("utils").setLevel(logging.DEBUG)
    if args.log != '':
        file_handler = logging.FileHandler(args.log, mode='w', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    __trs_dataset__ = args.dataset
    __DL_type__ = args.model
    if args.json == "None":
        args.json = None
    if args.json != None:
        try:
            with open(args.json, 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            logger.error("Json File '{}' not found".format(args.json))
            exit(1)
    else:
        json_data = {}

    #Main program
    try:
        start_time = datetime.datetime.now().replace(microsecond=0)

        #load traceset
        dataset = Dataset.Dataset(__trs_dataset__, __DL_type__, json_data=json_data)
        parameters = dataset.get_parameters()
        Hparams = dataset.get_model_parameters()
        callbacks_params = dataset.get_callbacks()

        #Load traces
        trace_data = dataset.traceset()
        trainset = torch.utils.data.TensorDataset(torch.Tensor(trace_data["x_train"]), torch.Tensor(trace_data["m_train"]["label"]))
        valset = torch.utils.data.TensorDataset(torch.Tensor(trace_data["x_val"]), torch.Tensor(trace_data["m_val"]["label"]))

        # Create model
        try:
            assert Hparams["model_type"] in available_models, "Model {} not found, available models are: {}".format(Hparams["model_type"], available_models)
            model = eval("Models."+Hparams["model_type"])(parameters, Hparams=Hparams)
        except AttributeError:
            raise Exception("module 'Models' has no attribute '{}', available attributes are: {}".format(Hparams["model_type"], [x[0] for x in inspect.getmembers(Models, inspect.isclass)]))

        #Print train session summary for debug
        logger.info("Dataset: {}".format(__trs_dataset__))
        logger.info("Model: {}".format(Hparams["model_type"]))
        logger.info("Parameters: {}".format(dataset.parameters))
        logger.info("Model parameters: {}".format(Hparams))
        logger.info(model)

        # Create experiment folders
        filebase = "{}/{}/{}".format(__trs_dataset__, __DL_type__, args.timestamp)
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
                                   Hparams=Hparams, 
                                   parameters=parameters, 
                                   exp_path=result_folder, 
                                   writer_path='runs/'+filebase)

        #Train model
        history = model.fit(trainset=trainset, 
                            valset=valset, 
                            parameters=parameters, 
                            Hparams = Hparams,
                            callbacks=callbacks,
                            verbose=1,
                        )
        #Save results
        Utils.save_model_weights(model, os.path.join(last_model_folder, 'last_model.pt'))
        Utils.save_history(history, history_folder + "history")
        Utils.save_db(root+'{}.sqlite'.format("experiment_db"), __trs_dataset__, dataset.parameters, model, history)

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