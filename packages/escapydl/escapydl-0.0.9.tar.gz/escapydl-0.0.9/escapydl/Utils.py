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
import time
import numpy as np
import progressbar
import json
import sqlalchemy
import pickle
import ast

import torch
import torch.nn as nn
import torch.nn.functional as F

#---------------------------------------------------#
# Loss functions
class FocalLoss(nn.Module):
    def __init__(
            self,
            weight=None,
            gamma=2.,
            reduction='mean'
    ):
        nn.Module.__init__(self)
        self.weight = weight
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, input_tensor, target_tensor):
        log_prob = F.log_softmax(input_tensor, dim=-1)
        prob = torch.exp(log_prob)
        return F.nll_loss(
                ((1 - prob) ** self.gamma) * log_prob,
                target_tensor,
                weight=self.weight,
                reduction=self.reduction
        )

class RankLoss(nn.Module):
    def __init__(self):
        nn.Module.__init__(self)
    def forward(self, input_tensor, target_tensor):
        log_prob = F.log_softmax(input_tensor, dim=-1)
        prob = torch.exp(log_prob)
        return torch.argwhere(torch.argsort(prob)==target_tensor)

#---------------------------------------------------#
# Custom layers
class LocallyConnected2d(nn.Module):
    """2D Locally connected layer (i.e., convolution without weight sharing)
    Source:https://discuss.pytorch.org/t/locally-connected-layers/26979/2
    """
    def __init__(self, in_channels, out_channels, output_size, kernel_size, stride, bias=False):
        super(LocallyConnected2d, self).__init__()
        output_size = torch.nn.modules.utils._pair(output_size)
        self.weight = nn.Parameter(
            torch.randn(1, out_channels, in_channels, output_size[0], output_size[1], kernel_size**2)
        )
        if bias:
            self.bias = nn.Parameter(
                torch.randn(1, out_channels, output_size[0], output_size[1])
            )
        else:
            self.register_parameter('bias', None)
        self.kernel_size = torch.nn.modules.utils._pair(kernel_size)
        self.stride = torch.nn.modules.utils._pair(stride)
        
    def forward(self, x):
        _, c, h, w = x.size()
        kh, kw = self.kernel_size
        dh, dw = self.stride
        x = x.unfold(2, kh, dh).unfold(3, kw, dw)
        x = x.contiguous().view(*x.size()[:-2], -1)
        # Sum in in_channel and kernel_size dims
        out = (x.unsqueeze(1) * self.weight).sum([2, -1])
        if self.bias is not None:
            out += self.bias
        return out

class LocallyConnected1d(nn.Module):
    """1D Locally connected layer (i.e., convolution without weight sharing)
    Adapted from a 2D implementation
    Source:https://discuss.pytorch.org/t/locally-connected-layers/26979/2
    """
    def __init__(self, in_channels, input_features, out_channels, kernel_size, stride, bias=False):
        super(LocallyConnected1d, self).__init__()
        self.output_size = (input_features - (kernel_size - 1)) // stride if stride==1 else (input_features - (kernel_size - 1) - 1) // stride + 1
        self.weight = nn.Parameter(
            torch.randn(1, out_channels, in_channels, self.output_size, kernel_size)
        )
        if bias:
            self.bias = nn.Parameter(
                torch.randn(1, out_channels, self.output_size)
            )
        else:
            self.register_parameter('bias', None)
        self.kernel_size = kernel_size
        self.stride = stride
        
    def forward(self, x):
        x = x.unfold(2, self.kernel_size, self.stride)
        x = x.contiguous().view(*x.size()[:-1], -1)
        # Sum in in_channel and kernel_size dims
        out = (x.unsqueeze(1) * self.weight).sum([2, -1])
        if self.bias is not None:
            out += self.bias
        return out

#---------------------------------------------------#
# Utilities 
def he_uniform_init_weights(m):
    """Initialize weights of a layer with He uniform distribution

    :param m: layer to initialize
    :type m: torch.nn.Module
    """
    if type(m) == nn.Linear:
        nn.init.kaiming_uniform_(m.weight, mode='fan_in', nonlinearity='relu')#same as glorot_uniform
        if m.bias != None:
            m.bias.data.zero_()

def zero_init_weights(m):
    """Initialize weights of a layer with zeros

    :param m: layer to initialize
    :type m: torch.nn.Module
    """
    if type(m) == nn.Linear:
        m.weight.data.zero_()
        if m.bias != None:
            m.bias.data.zero_()

class NumpyArrayEncoder(json.JSONEncoder):
    """Encode numpy arrays to json

    :param json: json encoder
    :type json: json.JSONEncoder
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
def save_history(history,filename):
    """Save training history to json file

    :param history: training history of the model
    :type history: dict
    :param filename: name of the file to save
    :type filename: str
    """
    with open(filename.replace('.json','').rstrip('/')+'.json','w') as output:
        json.dump(history,output,cls=NumpyArrayEncoder)
    return

def load_history(filename):
    """Load training history from json file

    :param filename: name of the file to load
    :type filename: str
    """
    with open(filename,'r') as f:
        ret = json.load(f)
    return ret

def save_model_weights(model,filename):
    """Save the weights of a model to a file

    :param model: model to save
    :type model: torch.nn.Module
    :param filename: name of the file to save
    :type filename: str
    """
    torch.save(model.state_dict(), filename)
    return

def load_model_weights(model,filename):
    """Load the weights of a model from a file to model

    :param model: model to load
    :type model: torch.nn.Module
    :param filename: name of the file to load
    :type filename: str
    """
    return model.load_state_dict(torch.load(filename))

def save_model_torchscript(model,filename):
    """Save the torchscript of a model to a file

    :param model: model to save
    :type model: torch.nn.Module
    :param filename: name of the file to save
    :type filename: str
    """
    return torch.jit.save(torch.jit.script(model),filename)

def load_model_torchscript(filename):
    """Load the torchscript of a model from a file to model
    Call model.eval() on returned model if you want to do inference on the model

    :param filename: name of the file to load
    :type filename: str
    """
    return torch.jit.load(filename)

def shuffle_numpy(x):
    """Shuffle a numpy array

    :param x: array to shuffle
    :type x: numpy.ndarray
    """
    p = np.random.permutation(x[0].shape[0])
    for i in range(len(x)):
        x[i] = x[i][p]

def shuffle_dict(x,shuffled_keys):
    """Shuffle a dictionary of arrays

    :param x: dictionary of arrays to shuffle
    :type x: dict
    :param shuffled_keys: list of keys to shuffle
    :type shuffled_keys: list
    """
    p = np.random.permutation(x[shuffled_keys[0]].shape[0])
    for i in shuffled_keys:
        x[i] = x[i][p]

def shuffle_torch(x):
    """Shuffle a torch tensor

    :param x: tensor to shuffle
    :type x: torch.Tensor
    """
    p = torch.randperm(x[0].shape[0])
    for i in range(len(x)):
        x[i] = x[i][p]
    return x

def save_db(db_filepath, dataset_name, dataset_parameters, model, history):
    """Save the dataset parameters, model, and training history to a sqlite database
    Uses sqlalchemy to sqlite database

    Structure of the database:\n
    - alembic_version\n
    - datset_parameters (id, dataset_name, value)\n
    - model (id, model_name, model_hyperparameters, model_class, fit_function, pickled_model_weights)\n
    - training_outputs (id, training_history)

    :param db_filepath: path to the database file
    :type db_filepath: str
    :param dataset_parameters: Dictionary of dataset parameters
    :type dataset_parameters: dict
    :param model: model to save
    :type model: torch.nn.Module
    :param history: training history of the model
    :type history: dict
    """
    engine = sqlalchemy.create_engine('sqlite:///'+db_filepath, echo=True)
    con = engine.connect()
    con.execute(sqlalchemy.text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL, CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num))"))
    con.execute(sqlalchemy.text("INSERT INTO alembic_version VALUES(:version_num)"), [{"version_num":sqlalchemy.__version__}])
    con.commit()

    intermediate_value_code = ""
    get_attack_parameters_code = ""
    get_known_key_code = ""
    with open(os.path.join(os.path.join(os.path.dirname(__file__), "datasets"), dataset_name+".py"), "r") as f:
        callbacks_file = ast.parse(f.read())
        for p in callbacks_file.body:
            if isinstance(p, ast.FunctionDef):
                if p.name == "intermediate_value":
                    intermediate_value_code = ast.unparse(p)
                if p.name == "get_attack_parameters":
                    get_attack_parameters_code = ast.unparse(p)
                if p.name == "get_known_key":
                    get_known_key_code = ast.unparse(p)
    con.execute(sqlalchemy.text("CREATE TABLE IF NOT EXISTS datset_parameters (id PRIMARY KEY, dataset_name TEXT, dataset_parameters JSON, intermediate_value_code TEXT, get_attack_parameters_code TEXT, get_known_key_code TEXT)"))
    con.execute(
        sqlalchemy.text("INSERT INTO datset_parameters VALUES(1, :dataset_name, :dataset_parameters, :intermediate_value_code, :get_attack_parameters_code, :get_known_key_code)"),
        [{"dataset_name":dataset_name,
          "dataset_parameters":json.dumps(dataset_parameters),
          "intermediate_value_code":intermediate_value_code,
          "get_attack_parameters_code":get_attack_parameters_code,
          "get_known_key_code":get_known_key_code,}],
    )

    model.Hparams['loss_function'] = str(model.Hparams['loss_function'])
    model_code = ""
    fit_function_code = ""
    with open(os.path.join(os.path.dirname(__file__), "Models.py"), "r") as f:
        models_file = ast.parse(f.read())
        for p in models_file.body:
            if isinstance(p, ast.ClassDef):
                if p.name == model.__class__.__name__:
                    model_code = ast.unparse(p)
            if isinstance(p, ast.FunctionDef):
                if p.name == model.fit.__name__:
                    fit_function_code = ast.unparse(p)
    con.execute(sqlalchemy.text("CREATE TABLE IF NOT EXISTS model (id PRIMARY KEY, model_name TEXT, model_hyperparameters TEXT, model_class TEXT, fit_function TEXT, pickled_model_weights BLOB)"))
    con.execute(
        sqlalchemy.text("INSERT INTO model VALUES(1, :model_name, :model_hyperparameters, :model_class, :fit_function, :pickled_model_weights)"),
        [{  "model_name":model.name,
            "model_hyperparameters":json.dumps(model.Hparams),
            "model_class":model_code,
            "fit_function":fit_function_code,
            "pickled_model_weights":pickle.dumps(model.state_dict()),
        }]
    )

    con.execute(sqlalchemy.text("CREATE TABLE IF NOT EXISTS training_outputs (id PRIMARY KEY, history JSON)"))
    con.execute(
        sqlalchemy.text("INSERT INTO training_outputs VALUES(1, :history)"),
        [{"history":json.dumps(history,cls=NumpyArrayEncoder)}]
    )
    con.commit()

def load_db(db_filepath):
    """Load the dataset parameters, model, and training history from a sqlite database

    :param db_filepath: path to the database file
    :type db_filepath: str
    """
    engine = sqlalchemy.create_engine('sqlite:///'+db_filepath, echo=True)
    con = engine.connect()
    
    result = con.execute(sqlalchemy.text("SELECT * FROM datset_parameters")).first()
    dataset_name = result[1]
    dataset_parameters = result[2:]
    print("dataset_name = ",dataset_name)
    print("dataset_parameters = ", dataset_parameters)

    result = con.execute(sqlalchemy.text("SELECT model_hyperparameters, model_class, fit_function, pickled_model_weights FROM model")).first()
    model_hyperparameters = json.loads(result[0])
    model_class = result[1]
    fit_function = result[2]
    pickled_model_weights = pickle.loads(result[3])
    print(model_hyperparameters, model_class, fit_function, pickled_model_weights)

    result = con.execute(sqlalchemy.text("SELECT history FROM training_outputs")).first()
    training_history = json.loads(result[0])
    print(training_history)
    return dataset_name


def pbar(iter,desc=''):
    widgets = [
        progressbar.Bar(marker='█'),
        progressbar.Counter(format='%(value)d/%(max_value)d'),
        ' [', progressbar.Timer(format='%(elapsed)s'), '<', progressbar.ETA(format='%(eta)8s', format_not_started='--:--:--', format_finished='%(elapsed)8s', format_zero='00:00:00'), '] ',
    ]
    bar = progressbar.ProgressBar(redirect_stdout=True, widgets=widgets, suffix='\\r', prefix=desc, max_value=len(iter)).start()
    for i,it in enumerate(iter):
        yield it
        bar.update(i+1)
    bar.finish(end='\n')

