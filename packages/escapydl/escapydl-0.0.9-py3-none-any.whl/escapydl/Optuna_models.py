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

import inspect, types
import sys
import time
import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.debug(device)

import Utils
import Callbacks

from torch.utils import tensorboard
import optuna
#---------------------------------------------------#
# Hyperparameter optimization

def is_function_local(object):
    return isinstance(object, types.FunctionType) and object.__module__ == __name__

hp_search_s_default = {"activation_function_s": ['relu', 'tanh', 'selu'],
                            "epochs": [100,100,1], 
                            "bs": [32,512,32],
                            "loss_function_s": ["crossentropy"],
                            "n_neurons_s": [10,500,10], 
                            "n_layers_s": [1,5,1], 
                            "kernel_size_s": [3,8,1],
                            "n_conv_block_s": [0,2,1],
                            "optimizer_s": ["Adam"], 
                            "lr_s": [1e-3,1e-3,'log']}

def make_MLP(trial, hp_search_s, trace_length, num_classes, **kwargs):
    in_features = trace_length
    n_layers_s = hp_search_s['n_layers_s']
    n_neurons_s = hp_search_s['n_neurons_s']
    activation_function_s = [x.lower() for x in hp_search_s['activation_function_s']]

    n_layers = trial.suggest_int("n_layers", int(n_layers_s[0]), int(n_layers_s[1]), int(n_layers_s[2]))
    activation_function = trial.suggest_categorical("activation_function", activation_function_s)
    try:
        act = {"relu":nn.ReLU, "tanh":nn.Tanh, "selu":nn.SELU}[activation_function]
    except:
        logger.error('Activation function is not supported now..')
        sys.exit(-1)
    layers = []
    layers.append(nn.Flatten())
    layers.append(nn.BatchNorm1d(trace_length))
    for i in range(n_layers):
        out_features = trial.suggest_int('n_units_l{}'.format(i), int(n_neurons_s[0]), int(n_neurons_s[1]), int(n_neurons_s[2]))
        layers.append(nn.Linear(in_features, out_features))
        layers.append(act())
        layers.append(nn.Dropout(0.1))
        in_features = out_features
    layers.append(nn.Linear(in_features, num_classes))
    return nn.Sequential(*layers)

def make_CNN(trial, hp_search_s, trace_length, num_classes, **kwargs):
    in_features = trace_length
    n_layers_s = hp_search_s['n_layers_s']
    n_neurons_s = hp_search_s['n_neurons_s']
    # n_filters_s = hp_search_s['n_filters_s']
    kernel_size_s = hp_search_s['kernel_size_s']
    activation_function_s = [x.lower() for x in hp_search_s['activation_function_s']]
    n_conv_block_s = hp_search_s['n_conv_block_s']
    #default conv1d parameters
    padding = 0
    stride = 1
    dilation = 1

    n_conv_block = trial.suggest_int('n_conv_block', int(n_conv_block_s[0]), int(n_conv_block_s[1]), int(n_conv_block_s[2]))
    activation_function = trial.suggest_categorical("activation_function", activation_function_s)
    try:
        act = {"relu":nn.ReLU, "tanh":nn.Tanh, "selu":nn.SELU}[activation_function]
    except:
        logger.error('Activation function is not supported now..')
        sys.exit(-1)
    i=0
    layers = []
    layers.append(nn.BatchNorm1d(1))
    for _ in range(n_conv_block):
        kernel_size = trial.suggest_int('kernel_size_{}'.format(i), int(kernel_size_s[0]), int(kernel_size_s[1]), int(kernel_size_s[2]))
        c_in = min(512,8**i)
        c_out = min(512,8**(i+1))
        layers.append(nn.Conv1d(c_in, c_out, kernel_size=kernel_size))
        out_features = (in_features + 2 * padding - dilation * (kernel_size - 1) - 1) // stride + 1
        layers.append(act())
        if i%2==1:
            layers.append(nn.BatchNorm1d(c_out))
        layers.append(nn.AvgPool1d(2))
        out_features = max(1, (out_features - 2) // 2 + 1)
        i+=1
        in_features = out_features
    # layers.append(Dropout(0.5))
    layers.append(nn.Flatten())
    in_features = min(512,8**(i))*(in_features)#Number of filters * number of features
    n_layers = trial.suggest_int("n_layers", int(n_layers_s[0]), int(n_layers_s[1]), int(n_layers_s[2]))
    for i in range(n_layers):
        out_features = trial.suggest_int('n_units_l{}'.format(i), int(n_neurons_s[0]), int(n_neurons_s[1]), int(n_neurons_s[2]))
        layers.append(nn.Linear(in_features, out_features))
        layers.append(act())
        in_features = out_features
    layers.append(nn.Linear(in_features, num_classes))
    return nn.Sequential(*layers)

def make_CNN_simpler(trial, hp_search_s, trace_length, num_classes, **kwargs):
    in_features = trace_length
    n_layers_s = hp_search_s['n_layers_s']
    n_neurons_s = hp_search_s['n_neurons_s']
    activation_function_s = [x.lower() for x in hp_search_s['activation_function_s']]
    #default conv1d parameters
    padding = 0
    stride = 1
    dilation = 1

    activation_function = trial.suggest_categorical("activation_function", activation_function_s)
    try:
        act = {"relu":nn.ReLU, "tanh":nn.Tanh, "selu":nn.SELU}[activation_function]
    except:
        logger.error('Activation function is not supported now..')
        sys.exit(-1)

    i=0
    layers = []
    layers.append(nn.BatchNorm1d(1))
    cin = 1
    for i in range(3):
        kernel_size = 80//(i+1)
        stride = 1
        cout = 128
        layers.append(nn.Conv1d(cin, cout, kernel_size=kernel_size, stride=stride))
        layers.append(act())
        in_features = (in_features + 2 * padding - dilation * (kernel_size - 1) - 1) // stride + 1
        layers.append(nn.BatchNorm1d(cout))
        layers.append(nn.AvgPool1d(2))
        in_features = max(1, (in_features - 2) // 2 + 1)
        cin = cout

    for i in range(2):
        kernel_size = 5
        stride = 1
        cout = 256
        layers.append(nn.Conv1d(cin, cout, kernel_size=kernel_size, stride=stride))
        layers.append(act())
        in_features = (in_features + 2 * padding - dilation * (kernel_size - 1) - 1) // stride + 1
        layers.append(nn.BatchNorm1d(cout))
        layers.append(nn.AvgPool1d(2))
        in_features = max(1, (in_features - 2) // 2 + 1)
        cin = cout

    for _ in range(2):
        kernel_size = 3
        stride = 1
        cout = 512
        layers.append(nn.Conv1d(cin, cout, kernel_size=kernel_size, stride=stride))
        layers.append(act())
        in_features = (in_features + 2 * padding - dilation * (kernel_size - 1) - 1) // stride + 1
        layers.append(nn.BatchNorm1d(cout))
        layers.append(nn.AvgPool1d(2))
        in_features = max(1, (in_features - 2) // 2 + 1)
        cin = cout
    
    layers.append(nn.Flatten())
    in_features = cout*(in_features)#Number of filters * number of features
    n_layers = trial.suggest_int("n_layers", int(n_layers_s[0]), int(n_layers_s[1]), int(n_layers_s[2]))
    for i in range(n_layers):
        out_features = trial.suggest_int('n_units_l{}'.format(i), int(n_neurons_s[0]), int(n_neurons_s[1]), int(n_neurons_s[2]))
        layers.append(nn.Linear(in_features, out_features))
        layers.append(act())
        in_features = out_features
    layers.append(nn.Linear(in_features, num_classes))
    return nn.Sequential(*layers)

def objective_hp(parameters, hp_search_s, trace_data, callbacks=[Callbacks.Callback()], verbose=0, *args, **kwargs):
    hp_search_s = {**hp_search_s_default, **hp_search_s}
    logger.info("\nHyperparameters search space:")
    #TODO: print values without the string representation, maybe use strip("'") for elements in list
    for key in hp_search_s.keys():
        logger.info("{}: {}".format(key,hp_search_s[key]))
    logger.info("\n")

    #Create dataloaders
    trainset = torch.utils.data.TensorDataset(torch.Tensor(trace_data["x_train"]), torch.Tensor(trace_data["m_train"]["label"]))
    valset = torch.utils.data.TensorDataset(torch.Tensor(trace_data["x_val"]), torch.Tensor(trace_data["m_val"]["label"]))
    valloader = torch.utils.data.DataLoader(valset, batch_size=1024, shuffle=True, pin_memory=True, num_workers=4)#no need for gradient descent
    def objective(trial):
        epochs = trial.suggest_int("epochs", hp_search_s['epochs'][0], hp_search_s['epochs'][1], hp_search_s['epochs'][2])
        bs = trial.suggest_int("bs", hp_search_s['bs'][0], hp_search_s['bs'][1], hp_search_s['bs'][2])
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=bs, shuffle=True, pin_memory=True, num_workers=4)

        model = eval(kwargs['model_name'])(trial, hp_search_s, parameters['n_samples'], parameters['num_classes'], **kwargs).to(device)
        
        #Give a new writer to the callbacks for a given trial
        for c in callbacks:
            c.reset(epochs=epochs, trial=trial)
        
        optimizer_name = trial.suggest_categorical("optimizer", hp_search_s['optimizer_s'])
        if hp_search_s['lr_s'][2] == 'log':
            lr = trial.suggest_float("lr", float(hp_search_s['lr_s'][0]), float(hp_search_s['lr_s'][1]), log=True)
        else:
            lr = trial.suggest_float("lr", float(hp_search_s['lr_s'][0]), float(hp_search_s['lr_s'][1]), step=hp_search_s['lr_s'][2])
        optimizer = getattr(optim, optimizer_name)(model.parameters(), lr=lr, betas=(0.9, 0.999), weight_decay=10e-5)

        model.apply(Utils.he_uniform_init_weights)
        history = {'loss':torch.zeros((epochs), device=device), 'accuracy':torch.zeros((epochs), device=device), 'val_loss':torch.zeros((epochs), device=device), 'val_accuracy':torch.zeros((epochs), device=device)}

        loss_function = trial.suggest_categorical("loss_function", hp_search_s['loss_function_s'])
        criterion = {"crossentropy":nn.CrossEntropyLoss(), "mse":nn.MSELoss()}[loss_function.lower()]
        m = nn.LogSoftmax(dim=1)

        model.train()
        skip = [cb.on_train_begin() for cb in callbacks]
        for epoch in range(epochs):
            start_t = time.time()
            skip = [cb.on_epoch_begin(trial=trial) for cb in callbacks]
            for i, (data, labels) in enumerate(trainloader):
                skip = [cb.on_batch_begin() for cb in callbacks]
                inputs, labels = data.to(device), labels.to(device)
                # forward + backward + optimize
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(m(outputs), labels.long())
                skip = [cb.on_loss_end() for cb in callbacks]
                loss.backward()
                skip = [cb.on_step_begin() for cb in callbacks]
                optimizer.step()
                skip = [cb.on_step_end() for cb in callbacks]
                history['loss'][epoch] += loss.detach().detach()
                history['accuracy'][epoch] += (outputs.argmax(dim=1) == labels).sum()
            history['loss'][epoch] /= (i+1)
            history['accuracy'][epoch] /= parameters['training_size']

            #Validation pass
            with torch.no_grad():
                for i, (data, labels) in enumerate(valloader):
                    inputs, labels = data.to(device), labels.to(device)
                    # forward only
                    outputs = model(inputs)
                    loss = criterion(m(outputs), labels.long())
                    history['val_loss'][epoch] += loss
                    history['val_accuracy'][epoch] += (outputs.argmax(dim=1) == labels).sum()
                history['val_loss'][epoch] /= (i+1)
                history['val_accuracy'][epoch] /= parameters['val_size']
                skip = [cb.on_epoch_end(model=model, epoch=epoch, history=history, trial=trial, last_epoch=epochs, **kwargs) for cb in callbacks]

            # Get the objective value from the metric, and report to trial
            if 'metric' in kwargs.keys():
                if kwargs['metric'] in ['val_accuracy', 'val_loss', 'accuracy', 'loss']:
                    objective_value = history[kwargs['metric']][epoch]
                    trial.report(objective_value, epoch)
                elif kwargs['metric'] == 'gge':
                    # objective value is evaluated inside the callback, and reported here
                    for cb in callbacks:
                        if cb.name == 'gge':
                            objective_value = cb.get_fit_value()
                else:
                    logging.warning("Metric '{}' is not defined, default to objective_value=0".format(kwargs['metric']))
                    objective_value = 0 #No value to report
            
            # Handle pruning based on the intermediate value.
            if trial.should_prune():
                raise optuna.exceptions.TrialPruned()
            
            #deserialize history
            np_history = {}
            for key in history.keys():
                np_history[key] = history[key].detach().cpu().numpy()
            torch.cuda.empty_cache()
            if verbose > 0:
                logger.info("Epoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
        if verbose == 0:
            logger.info("\nEpoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
        skip = [cb.on_train_end(model, trial=trial) for cb in callbacks]
        #Return one float value as final score
        return objective_value
    return objective
