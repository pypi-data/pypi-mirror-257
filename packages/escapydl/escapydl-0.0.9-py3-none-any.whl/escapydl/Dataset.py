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

import sys, os
import importlib
import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import ast
import trsfile
import h5py
import torch
import numpy as np
import Callbacks
from Utils import pbar

class Dataset:
    """
    Class to construct the traceset and easily get traces, labels and metadata without explicitly calling a specific dataset.
    (enable customizable shuffling + higher level functions for operation on traces)
    """
    def __init__(self, trs_dataset, dl_type, json_data={}):
        self.trs_dataset = trs_dataset
        self.dl_type = dl_type

        if json_data == {}:
            try:
                logger.debug("Loading info on dataset from datasets/{}.py".format(trs_dataset))
                module = importlib.import_module("datasets.{}".format(trs_dataset))
                parameters = getattr(module,"parameters")
                callbacks = getattr(module,"callbacks")
                model_params = getattr(module,"model")
                try:
                    self.hp_search_s = getattr(module,"hp_search_s")
                except AttributeError:
                    self.hp_search_s = {}
                get_attack_parameters = getattr(module,"get_attack_parameters")
                get_known_key = getattr(module,"get_known_key")
                intermediate_value = getattr(module,"intermediate_value")
            except AttributeError as e:
                logger.error(e)
                sys.exit("Dataset is incorrect. Check your command argument.")
        else:
            try:
                logger.debug("Loading info on dataset from loaded json file")
                model_params = json_data["model"]
                parameters = json_data["parameters"]
                callbacks = json_data["callbacks"]
                try:
                    parameters["dataset_name"] = eval(parameters["dataset_name"])
                except Exception:
                    parameters["dataset_name"] = parameters["dataset_name"].strip('"').strip("'")
                parameters["dataset_size"] = int(parameters["dataset_size"])
                parameters["training_size"] = int(parameters["training_size"])
                parameters["val_size"] = int(parameters["val_size"])
                parameters["subkey"] = ast.literal_eval(parameters["subkey"])
                parameters["num_key_hypotheses"] = int(parameters["num_key_hypotheses"])
                parameters["n_samples"] = int(parameters["n_samples"])
                parameters["shuffle"] = bool(parameters["shuffle"])
                try:
                    parameters["pre_trained_model"] = eval(parameters["pre_trained_model"])
                except Exception:
                    pass
                self.hp_search_s = json_data["hp_search_s"] if "hp_search_s" in json_data.keys() else {}
                _locals = {}
                for arg_import in json_data["extra_imports"]:
                    exec(arg_import, globals())
                    exec(arg_import, globals(), _locals)
                for function in json_data["functions"]:
                    exec(json_data["functions"][function], globals())
                    exec(json_data["functions"][function], globals(), _locals)
                get_attack_parameters = _locals["get_attack_parameters"]
                get_known_key = _locals["get_known_key"]
                intermediate_value = _locals["intermediate_value"]
            except Exception as e:
                logger.error(e)
                sys.exit("JSON file is incorrect. Check your json data for missing key argument.")

        model_params["model_type"] = dl_type
        self.model_params = model_params
        #Redefine function in utils module
        Callbacks.intermediate_value = intermediate_value
        Callbacks.get_attack_parameters = get_attack_parameters
        Callbacks.get_known_key = get_known_key
        self.parameters = parameters
        self.callbacks = callbacks
    
    def get_parameters(self):
        return self.parameters
    
    def get_model_parameters(self):
        return self.model_params
    
    def get_callbacks(self):
        return self.callbacks
    
    def get_hp_search_s(self):
        return self.hp_search_s

    def traceset(self):
        """
        Class to construct the traceset and easily get traces, labels and metadata without explicitly calling a specific dataset.
        (enable customizable shuffling + higher level functions for operation on traces)
        """
        #TODO: add support for other file formats
        traces, metadata, e_dataset_size = read_dataset(self.parameters)

        PREPROCESS = False
        if PREPROCESS:
            traces /= np.linalg.norm(traces,axis=1)[:,None] # normalize
            # traces = traces + np.random.normal(0,1,size=traces.shape) # Add random noise
            # traces = np.array([np.sum(traces[:,i:i+5],axis=1) for i in range(0,traces.shape[1],5)]).T # average window resample
            self.parameters["n_samples"] = traces.shape[1]


        logger.info("Traceset loaded")
        #Recompute labels based on intermediate value model
        if isinstance(self.parameters["subkey"], int):
            metadata['label'] = np.array([Callbacks.intermediate_value(Callbacks.get_known_key(metadata, self.parameters["subkey"], i),Callbacks.get_attack_parameters(metadata, self.parameters["subkey"], i)) for i in pbar(range(e_dataset_size), desc="Compute labels")])
        elif isinstance(self.parameters["subkey"], list):
            metadata['label'] = np.array([[Callbacks.intermediate_value(Callbacks.get_known_key(metadata,sk,i),Callbacks.get_attack_parameters(metadata,sk,i)) for sk in self.parameters['subkey']] for i in pbar(range(e_dataset_size), desc="Compute labels")])
        self.parameters["num_classes"] = len(set(metadata["label"].reshape(-1)))
        logger.info("Labels computed")

        traces = np.array(traces)
        traces = np.expand_dims(traces, axis=1)
        logger.info(traces.shape)

        train_size = self.parameters["training_size"]
        val_size = self.parameters["val_size"]
        assert train_size+val_size <= len(traces), "Error: dataset is too small to be splitted"
        #split dataset into train, val and test
        traces_train = np.array(traces[:train_size], dtype=np.float32)
        traces_val = np.array(traces[train_size:train_size+val_size], dtype=np.float32)
        metadata_train = {k:metadata[k][:train_size] for k in metadata.keys()}
        metadata_val = {k:metadata[k][train_size:train_size+val_size] for k in metadata.keys()}
        #if Shuffle is enabled, shuffle the dataset and keep the same order for traces and metadata
        if self.parameters["shuffle"]:
            perm_train = np.random.permutation(train_size)
            perm_val = np.random.permutation(val_size)
            traces_train = traces_train[perm_train]
            traces_val = traces_val[perm_val]
            metadata_train = {k:metadata_train[k][perm_train] for k in metadata_train.keys()}
            metadata_val = {k:metadata_val[k][perm_val] for k in metadata_val.keys()}
        logger.info("Dataset splitted into train and validation sets")

        # logger.debug(metadata_val.keys())
        for i in range(val_size):
            assert (metadata_val["key"][0]).all() == (metadata_val["key"][i]).all(), "Validation set should be on fixed key: {}".format(i)

        #return a dictionary with the traces and metadata
        return  {
            "x_train" : torch.from_numpy(traces_train),
            "x_val" : torch.from_numpy(traces_val),
            "m_train" : {k:torch.from_numpy(metadata_train[k]) for k in metadata_train.keys()},
            "m_val" : {k:torch.from_numpy(metadata_val[k]) for k in metadata_val.keys()},
            }


def read_dataset(parameters):
    if "validation_dataset" in parameters and parameters["validation_dataset"]!=None:
        dataset = Dataset_raw(parameters["dataset_name"], parameters["training_size"])
        assert dataset.len_train_dataset() >= parameters["training_size"]
        val_dataset = Dataset_raw(parameters["validation_dataset"], parameters["val_size"])
        assert val_dataset.len_attack_dataset() >= parameters["val_size"]
        e_dataset_size = parameters["training_size"] + parameters["val_size"]
        traces = np.array([dataset.get_train_trace(i) for i in pbar(range(parameters["training_size"]),desc='Loading training traces')] + [val_dataset.get_attack_trace(i) for i in pbar(range(parameters["val_size"]),desc='Loading validation traces')])
        assert dataset.metadata_keys == val_dataset.metadata_keys, "Parameters in the two datasets must match"
        metadata = {k:np.empty((e_dataset_size, len(dataset.get_train_metadata(0,k))), dtype=np.uint8) for k in dataset.metadata_keys}
        for i in pbar(range(e_dataset_size), desc='Loading metadata'):
            for k in list(dataset.metadata_keys):
                if k<parameters["training_size"]:
                    metadata[k][i] = dataset.get_train_metadata(i,k)
                else:
                    metadata[k][i] = val_dataset.get_attack_metadata(i-parameters["training_size"],k)
    else:
        dataset = Dataset_raw(parameters["dataset_name"], parameters["dataset_size"])
        e_dataset_size = parameters["training_size"] + parameters["val_size"]
        assert int(parameters['dataset_size']) >= e_dataset_size
        traces = np.array([dataset.get_train_trace(i) for i in pbar(range(parameters["training_size"]), desc='Loading training traces')] + [dataset.get_attack_trace(i) for i in pbar(range(parameters["val_size"]),desc='Loading validation traces')])
        metadata = {k:np.empty((e_dataset_size, len(dataset.get_train_metadata(0,k))), dtype=np.uint8) for k in dataset.metadata_keys}
        for i in pbar(range(e_dataset_size), desc='Loading metadata'):
            for k in list(dataset.metadata_keys):
                if i<parameters["training_size"]:
                    metadata[k][i] = dataset.get_train_metadata(i,k)
                else:
                    metadata[k][i] = dataset.get_attack_metadata(i-parameters["training_size"],k)
    return traces, metadata, e_dataset_size
    
class Dataset_raw:
    """Define a generic class to load a dataset from different file formats (trs, h5)
    """
    def __init__(self,filepath:str, dataset_size:int) -> None:
        self.file_type = filepath.split(".")[-1]
        self.supported_file_types = ["trs","h5"]
        if self.file_type == "h5":
            self.profiling_flag = "Profiling_traces" if "Profiling_traces" in h5py.File(filepath,'r').keys() else "fixed_keys"
            self.attack_flag = "Attack_traces" if "Attack_traces" in h5py.File(filepath,'r').keys() else "random_keys"
        self._load_file(filepath)
        self.trace_parameters = self._load_metadata_keys()
        self.dataset_size = dataset_size


    def _load_file(self,filepath):
        if self.file_type == "trs":
            self.file = trsfile.trs_open(filepath,'r')
        elif self.file_type == "h5":
            self.file = h5py.File(filepath,'r')
        else:
            raise NotImplementedError("Only .trs and .h5 files are supported for now")
        
    def _load_metadata_keys(self):
        if self.file_type == "trs":
            self.metadata_keys = list(self.file.get_header(trsfile.Header.TRACE_PARAMETER_DEFINITIONS).keys())
        elif self.file_type == "h5":
            self.metadata_keys = list(self.file[self.profiling_flag+'/metadata'].dtype.names)
        
    def len_attack_dataset(self):
        if self.file_type == "trs":
            return self.file.get_header(trsfile.Header.NUMBER_TRACES)
        elif self.file_type == "h5":
            return len(self.file[self.attack_flag+"/traces"])
        
    def len_train_dataset(self):
        if self.file_type == "trs":
            return self.file.get_header(trsfile.Header.NUMBER_TRACES)
        elif self.file_type == "h5":
            return len(self.file[self.profiling_flag+"/traces"])
        
    def get_train_trace(self, index):
        if self.file_type == "trs":
            return self.file[index].samples
        elif self.file_type == "h5":
            return self.file[self.profiling_flag+"/traces"][index]
        
    def get_attack_trace(self, index):
        if self.file_type == "trs":
            return self.file[self.dataset_size-1 - index].samples
        elif self.file_type == "h5":
            return self.file[self.attack_flag+"/traces"][index]
        
    def get_train_metadata(self, index, key):
        if self.file_type == "trs":
            return self.file[index].parameters[key].value
        elif self.file_type == "h5":
            return self.file[self.profiling_flag+"/metadata"][index][key]
        
    def get_attack_metadata(self, index, key):
        if self.file_type == "trs":
            return self.file[self.dataset_size-1 - index].parameters[key].value
        elif self.file_type == "h5":
            return self.file[self.attack_flag+"/metadata"][index][key]

