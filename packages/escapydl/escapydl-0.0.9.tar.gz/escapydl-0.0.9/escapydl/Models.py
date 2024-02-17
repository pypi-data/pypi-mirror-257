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

import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.debug(device)

import sys
import time
import numpy as np
import collections
import Callbacks
import Utils


#---------------------------------------------------#
# Models

class MLP(nn.Module):
    default_Hparams = {"activation_function":'tanh',
                        "lr": 1e-3,
                        "n_layers":2,
                        "n_units_l0": 20, 
                        "n_units_l1": 10}
    def __init__(self, parameters, Hparams={}):
        super(MLP, self).__init__()
        self.name = "MLP"
        self.Hparams = {**MLP.default_Hparams, **Hparams}#Merge default and given Hparams
        self.n_layers = int(self.Hparams['n_layers'])
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()] if 'activation_function' in self.Hparams.keys() else nn.ReLU()
        self.hidden = nn.ModuleList()
        self.hidden.append(nn.Linear(parameters["n_samples"], int(self.Hparams['n_units_l0'])))
        for i in range(self.n_layers-1):
            self.hidden.append(nn.Linear(int(self.Hparams['n_units_l{}'.format(i)]), int(self.Hparams['n_units_l{}'.format(i+1)])))
        self.fc1 = nn.Linear(int(self.Hparams['n_units_l{}'.format(self.n_layers-1)]), parameters["num_classes"])
        self.dropout = nn.Dropout(0.1)
        self.bnorm = nn.BatchNorm1d(parameters["n_samples"])
        # self.bnorm0 = nn.BatchNorm1d(1)
        self.flatten = nn.Flatten()
    def forward(self, x):
        # x = self.bnorm0(x)
        x = self.flatten(x)
        x = self.bnorm(x)
        for h_layer in self.hidden:
            x = self.act(h_layer(x))
            x = self.dropout(x)
        x = self.fc1(x)
        return x

    def fit(self,*args, **kwargs):
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return fit(self, *args, **kwargs)

class CNN_onetrace(nn.Module):
    def __init__(self, parameters, Hparams={}):
        super(CNN_onetrace, self).__init__()
        logger.debug("Create CNN module.")
        logger.debug(">> Input size:{}, num_classes:{}".format(parameters["n_samples"], parameters["num_classes"]))
        self.name = "CNN"
        self.n_samples = parameters["n_samples"]
        self.num_blocks = len(bin(self.n_samples)[2:]) - 2
        self.cnn_output_size = self.n_samples >> self.num_blocks
        logger.debug(">> Number of hidden conv blocks:{}, cnn output size:{}".format(self.num_blocks, self.cnn_output_size>>1))
        self.cnn_sequence = nn.Sequential(collections.OrderedDict([
            ('batchnorm0', nn.BatchNorm1d(1)),
            ('conv1', nn.Conv1d(1, 8, kernel_size=3, padding='same')),
            ('batchnorm1', nn.BatchNorm1d(8)),
            ('maxpool1', nn.MaxPool1d(2))
            ])
        )
        for i in range(0,self.num_blocks):
            self.cnn_sequence.append(nn.Conv1d(min(512,8<<i), min(512,8<<(i+1)),kernel_size=3, padding='same'))
            self.cnn_sequence.append(nn.ReLU())
            if i%2==1:
                self.cnn_sequence.append(nn.BatchNorm1d(min(512,8<<(i+1))))
            self.cnn_sequence.append(nn.MaxPool1d(2))
        self.cnn_sequence.append(nn.Flatten())
        self.cnn_sequence.append(nn.Dropout(0.5))
        #input size is the number of filters in last conv layer * output size of last conv layer
        self.cnn_sequence.append(nn.Linear(min(512,8<<self.num_blocks)*(self.cnn_output_size>>1) ,512))
        self.cnn_sequence.append(nn.ReLU())
        self.cnn_sequence.append(nn.Dropout(0.5))
        self.cnn_sequence.append(nn.Linear(512,parameters["num_classes"]))

    def forward(self, x):
        x = self.cnn_sequence(x)
        return x
    
    def fit(self,*args, **kwargs):
        return fit(self, *args, **kwargs)
    
class CNN(nn.Module):
    default_Hparams = {"activation_function": "tanh", 
                           "pooling": "average",
                           "optimizer": "adam",
                           "weight_init": "he_uniform",
                           "n_conv_block": 2,
                           "kernel_size_0": 11, 
                           "c_out_0": 3,
                           "kernel_size_1": 6,
                           "c_out_1": 3, 
                           "lr": 1e-3,  
                           "n_layers": 2, 
                           "n_units_l0": 20, 
                           "n_units_l1": 10}
    def __init__(self, parameters, Hparams={}, *args, **kwargs) -> None:
        super(CNN, self).__init__(*args, **kwargs)
        self.name = "CNN"
        self.Hparams = {**CNN.default_Hparams, **Hparams}#Merge default and given Hparams
        self.n_conv_blocks = int(self.Hparams["n_conv_block"])
        self.n_fc_layers = int(self.Hparams["n_layers"])
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()] if 'activation_function' in self.Hparams.keys() else nn.ReLU()
        #default conv1d parameters
        padding = int(self.Hparams["padding"]) if "padding" in self.Hparams.keys() else 0
        stride = int(self.Hparams["stride"]) if "stride" in self.Hparams.keys() else 1
        dilation = int(self.Hparams["dilation"]) if "dilatation" in self.Hparams.keys() else 1
        pooling_ks = int(self.Hparams["pooling_ks"]) if "pooling_ks" in self.Hparams.keys() else 2
        pooling_stride = int(self.Hparams["pooling_stride"]) if "pooling_stride" in self.Hparams.keys() else pooling_ks
        pooling_padding = int(self.Hparams["pooling_padding"]) if "pooling_padding" in self.Hparams.keys() else 0
        self.pooling = {"none":None, "max":nn.MaxPool1d, "average":nn.AvgPool1d}[self.Hparams['pooling'].lower()] if 'pooling' in self.Hparams.keys() else None
        if self.pooling is not None:
            self.pooling = self.pooling(pooling_ks, stride=pooling_stride, padding=pooling_padding)
        
        i=0
        in_features = parameters["n_samples"]
        c_in = 1
        self.cnn_layers = nn.ModuleList()
        self.input_bn = nn.BatchNorm1d(c_in)
        for i in range(self.n_conv_blocks):
            c_out = int(self.Hparams["c_out_{}".format(i)])
            self.cnn_layers.append(nn.Conv1d(c_in, c_out, kernel_size=int(self.Hparams["kernel_size_{}".format(i)]), padding='same'))
            # out_features = (in_features + 2 * padding - dilation * (int(self.Hparams["kernel_size_{}".format(i)]) - 1) - 1) // stride + 1
            out_features = in_features
            if self.pooling is not None:
                out_features = max(1, (out_features - 2*pooling_padding - pooling_ks) // pooling_stride + 1)
            in_features = out_features
            c_in = c_out
        self.flatten = nn.Flatten()
        in_features = int(c_in * in_features)
        self.fc_input_bn = nn.BatchNorm1d(in_features)
        self.fc_layers = nn.ModuleList()
        for i in range(self.n_fc_layers):
            self.fc_layers.append(nn.Linear(in_features, int(self.Hparams['n_units_l{}'.format(i)])))
            in_features = int(self.Hparams['n_units_l{}'.format(i)])
        self.last_fc = nn.Linear(in_features, parameters["num_classes"])
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, x):
        x = self.input_bn(x)
        for i in range(self.n_conv_blocks):
            x = self.act(self.cnn_layers[i](x))
            if self.pooling is not None:
                x = self.pooling(x)
        x = self.flatten(x)
        x = self.fc_input_bn(x)
        for i in range(self.n_fc_layers):
            x = self.act(self.fc_layers[i](x))
            x = self.dropout(x)
        x = self.last_fc(x)
        return x
    
    def fit(self,*args, **kwargs):
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return fit(self, *args, **kwargs)

class payAttentionNN(nn.Module):
    default_Hparams = {"activation_function": "tanh", 
                           "optimizer": "adam",
                           "weight_init": "he_uniform",
                           "reshape_size": 2,
                           "kernel_size": 21,
                           "stride": 10,
                           "units": 128,
                           }
    def __init__(self, parameters, Hparams={}, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.Hparams = {**payAttentionNN.default_Hparams, **Hparams}#Merge default and given Hparams
        self.units = int(self.Hparams['units'])
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()]
        self.reshape_size = int(self.Hparams['reshape_size'])
        self.kernel_size = int(self.Hparams['kernel_size'])
        self.stride = int(self.Hparams['stride'])

        self.local1d = Utils.LocallyConnected1d(1, parameters["n_samples"], 1, self.kernel_size, self.stride, bias=True)
        self.bn1 = nn.BatchNorm1d(self.local1d.output_size//self.reshape_size)
        self.bidir_lstm = nn.LSTM(self.reshape_size,self.units,1,bidirectional=True)

        self.dense_att = nn.Linear(2*self.units, 1, bias=False)
        self.flatten = nn.Flatten()
        self.softmax = nn.Softmax(dim=1)

        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(2*self.units, parameters["num_classes"])
        self.bn3 = nn.BatchNorm1d(parameters["num_classes"])

    def forward(self, x):
        #Encoder
        x = self.local1d(x)
        x = torch.reshape(x,(x.shape[0],-1,self.reshape_size))#Cut the sequences into smaller chunks
        x,_ = self.bidir_lstm(x)
        lstm_out = self.bn1(x)
        x = self.act(lstm_out)
        #Attention
        x = self.dense_att(x)
        x = self.flatten(x)
        x = self.softmax(self.bn1(x))
        x = x.repeat(2*self.units,1).view(-1,self.local1d.output_size//self.reshape_size,2*self.units)#Attention probabilities
        #Merge attention and raw lstm output
        x = torch.sum(x*lstm_out, dim=1)
        #Classifier
        x = self.dropout(x)
        x = self.bn3(self.fc1(x))
        return x
    
    def fit(self,*args, **kwargs):
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return fit(self, *args, **kwargs)
        
class MLP_byte(nn.Module):
    default_Hparams = {"activation_function":'relu',
                        "n_layers":2,
                        "n_units_l0": 20, 
                        "n_units_l1": 10}
    def __init__(self, parameters, Hparams={}, device_list=[torch.device('cpu')], device_idx=0, *args, **kwargs) -> None:
        super(MLP_byte, self).__init__()
        self.name = "MLP"
        self.device_list = device_list
        self.s_device = device_list[device_idx]
        self.Hparams = {**MLP_byte.default_Hparams, **Hparams}#Merge default and given Hparams
        self.n_layers = int(self.Hparams['n_layers'])
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()] if 'activation_function' in self.Hparams.keys() else nn.ReLU()
        self.hidden = nn.ModuleList()
        self.hidden.append(nn.Linear(parameters["n_samples"], int(self.Hparams['n_units_l0'])))
        for i in range(self.n_layers-1):
            self.hidden.append(nn.Linear(int(self.Hparams['n_units_l{}'.format(i)]), int(self.Hparams['n_units_l{}'.format(i+1)])))
        self.hidden = self.hidden.to(self.s_device)
        self.fc1 = nn.Linear(int(self.Hparams['n_units_l{}'.format(self.n_layers-1)]), parameters["num_classes"]).to(self.s_device)
        self.dropout = nn.Dropout(0.1)
        self.bnorm = nn.BatchNorm1d(parameters["n_samples"]).to(self.s_device)
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.flatten(x.to(self.s_device))
        # x = self.bnorm(x)
        for i in range(self.n_layers):
            x = self.act(self.hidden[i](x))
            x = self.dropout(x)
        x = self.fc1(x)
        return x.to(self.device_list[0])

def fit(model, parameters, trainset, valset, Hparams={}, callbacks=[Callbacks.Callback()], verbose=0, *args, **kwargs):
    default_Hparams = {"optimizer":"adam", "weight_init":"he_uniform", "loss_function":"crossentropy", "lr":1e-3, "bs":128, "num_epochs":100}
    Hparams = {**default_Hparams, **Hparams}
    logging.info("fit Hparams: {}".format(Hparams))
    weight_init_func = {"he_uniform":Utils.he_uniform_init_weights, "zero":Utils.zero_init_weights}[Hparams['weight_init'].lower()]
    optimizer_func = {"adam":optim.Adam, "rmsprop":optim.RMSprop, "sgd":optim.SGD}[Hparams['optimizer'].lower()]
    loss_function = {"crossentropy":nn.CrossEntropyLoss(), "mse":nn.MSELoss()}[Hparams['loss_function'].lower()] if isinstance(Hparams['loss_function'], str) else Hparams['loss_function']
    learning_rate = float(Hparams['lr'])
    batch_size = int(Hparams['bs'])
    epochs = int(Hparams['num_epochs'])

    #Create loaders
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, pin_memory=True, num_workers=4)
    valloader = torch.utils.data.DataLoader(valset, batch_size=parameters['val_size'], shuffle=True, pin_memory=True, num_workers=4)#no need for gradient descent

    model.to(device)
    model.apply(weight_init_func)
    optimizer = optimizer_func(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    
    criterion = loss_function
    m = nn.LogSoftmax(dim=1)

    history = {'loss':torch.zeros((epochs), device=device), 'accuracy':torch.zeros((epochs), device=device), 'val_loss':torch.zeros((epochs), device=device), 'val_accuracy':torch.zeros((epochs), device=device)}
    model.train()
    skip = [cb.on_train_begin() for cb in callbacks]
    for epoch in range(epochs):
        start_t = time.time()
        skip = [cb.on_epoch_begin() for cb in callbacks]
        for i, (data, labels) in enumerate(trainloader):
            skip = [cb.on_batch_begin() for cb in callbacks]
            inputs, labels = data.to(device), labels.to(device)
            # forward + backward + optimize
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(m(outputs), labels.long())
            loss.backward()
            skip = [cb.on_loss_end() for cb in callbacks]
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
            skip = [cb.on_epoch_end(model=model, epoch=epoch, history=history, last_epoch=epochs) for cb in callbacks]

        if verbose > 0:
            logger.info("Epoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
    if verbose == 0:
        logger.info("\nEpoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
    training_results = [cb.on_train_end(model) for cb in callbacks]

    #Return all results in history
    np_history = {}
    for d in training_results:
        try:
            np_history = {**np_history, **d}
        except:
            pass
    for key in history.keys():
        np_history[key] = history[key].detach().cpu().numpy()
    return np_history


#---------------------------------------------------#
# Models (multi-target)

class CNN_multi_bytes(nn.Module):
    # TODO: Give a pre-trained CNN on one byte and copy the convlution blocks to freeze it in the network, leaving only the MLPs to train.
    default_Hparams = {"activation_function": "relu", 
                           "pooling": "average",
                           "optimizer": "radam",
                           "weight_init": "he_uniform",
                           "n_conv_block": 2,
                           "kernel_size_0": 30, 
                           "c_out_0": 8,
                           "kernel_size_1": 5,
                           "c_out_1": 16, 
                        #    "kernel_size_2": 6,
                        #    "c_out_2": 32, 
                           "lr": 1e-3,  
                           "n_layers": 4, 
                           "n_units_l0": 500, 
                           "n_units_l1": 470,
                           "n_units_l2": 10,
                           "n_units_l3": 480,
                        #    "n_units_l4": 100,
                        #    "n_units_l5": 100,
                        #    "n_units_l6": 100,
                        #    "n_units_l7": 100,
                           }
    def __init__(self, parameters, Hparams={}, device_list=[torch.device('cuda:{:d}'.format(x)) for x in range(torch.cuda.device_count())], *args, **kwargs) -> None:
        super(CNN_multi_bytes, self).__init__(*args, **kwargs)
        self.name = "multiTargetCNN"
        self.Hparams = {**CNN_multi_bytes.default_Hparams, **Hparams}#Merge default and given Hparams
        self.device_list = device_list if device_list!=[] else [torch.device('cpu')]
        self.nk = len(parameters["subkey"]) if isinstance(parameters["subkey"], list) else 1
        self.nk_per_device = np.ceil(self.nk/len(self.device_list))
        
        self.n_conv_blocks = int(self.Hparams["n_conv_block"])
        self.n_fc_layers = int(self.Hparams["n_layers"])
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()] if 'activation_function' in self.Hparams.keys() else nn.ReLU()
        #default conv1d parameters
        padding = int(self.Hparams["padding"]) if "padding" in self.Hparams.keys() else 0
        stride = int(self.Hparams["stride"]) if "stride" in self.Hparams.keys() else 1
        dilation = int(self.Hparams["dilation"]) if "dilatation" in self.Hparams.keys() else 1
        pooling_ks = int(self.Hparams["pooling_ks"]) if "pooling_ks" in self.Hparams.keys() else 2
        pooling_stride = int(self.Hparams["pooling_stride"]) if "pooling_stride" in self.Hparams.keys() else pooling_ks
        pooling_padding = int(self.Hparams["pooling_padding"]) if "pooling_padding" in self.Hparams.keys() else 0
        self.pooling = {"none":None, "max":nn.MaxPool1d, "average":nn.AvgPool1d}[self.Hparams['pooling'].lower()] if 'pooling' in self.Hparams.keys() else None
        if self.pooling is not None:
            self.pooling = self.pooling(pooling_ks, stride=pooling_stride, padding=pooling_padding).to(self.device_list[0])

        self.dropout = nn.FeatureAlphaDropout(0.1)
        
        in_features = parameters["n_samples"]
        c_in = 1
        self.cnn_layers = nn.ModuleList()
        self.input_bn = nn.BatchNorm1d(c_in).to(self.device_list[0])
        for i in range(self.n_conv_blocks):
            c_out = int(self.Hparams["c_out_{}".format(i)])
            self.cnn_layers.append(nn.Conv1d(c_in, c_out, kernel_size=int(self.Hparams["kernel_size_{}".format(i)])))
            out_features = (in_features + 2 * padding - dilation * (int(self.Hparams["kernel_size_{}".format(i)]) - 1) - 1) // stride + 1
            if self.pooling is not None:
                out_features = max(1, (out_features - 2*pooling_padding - pooling_ks) // pooling_stride + 1)
            in_features = out_features
            c_in = c_out
        self.cnn_layers = self.cnn_layers.to(self.device_list[0])
        in_features = int(c_in * in_features)
        #Divise the branch equally between the number of available devices
        self.multy_byte_mlps = nn.ModuleDict([[str(k), MLP_byte({"n_samples":in_features, "num_classes":parameters["num_classes"]}, device_list=self.device_list, Hparams=self.Hparams, device_idx=int(k//self.nk_per_device))] for k in range(self.nk)])

        if "pre_trained_model" in parameters.keys():
            self.load_weights(parameters["pre_trained_model"])

    def load_weights(self, pre_trained_model):
        #Load the weights of the pre-trained model
        weights = torch.load(pre_trained_model)
        for i, layer in enumerate(self.cnn_layers):
            layer.weight = nn.parameter.Parameter(weights[list(weights)[i*2]])
            layer.bias = nn.parameter.Parameter(weights[list(weights)[i*2+1]])
            layer.weight.requires_grad = False
            layer.bias.requires_grad = False

    def forward(self, x):
        x = self.input_bn(x)
        for i in range(self.n_conv_blocks):
            x = self.act(self.cnn_layers[i](x))
            x = self.dropout(x)
            if self.pooling is not None:
                x = self.pooling(x)
        #Divise the branch equally between the number of available devices
        x = [self.multy_byte_mlps[str(k)](x) for k in range(self.nk)]
        return x
    
    def fit(self,*args, **kwargs):
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return multi_fit(self, *args, **kwargs)
    
class MLP_multi_bytes(nn.Module):
    # TODO: Give a pre-trained CNN on one byte and copy the convlution blocks to freeze it in the network, leaving only the MLPs to train.
    default_Hparams = {}
    def __init__(self, parameters, Hparams={}, device_list=[torch.device('cuda:{:d}'.format(x)) for x in range(torch.cuda.device_count())]):
        super(MLP_multi_bytes, self).__init__()
        self.name = "multiTargetMLP"
        self.Hparams = {**MLP_multi_bytes.default_Hparams, **Hparams}#Merge default and given Hparams
        self.device_list = device_list if device_list!=[] else [torch.device('cpu')]
        self.nk = len(parameters["subkey"]) if isinstance(parameters["subkey"], list) else 1
        self.nk_per_device = np.ceil(self.nk/len(self.device_list))
        in_features = parameters["n_samples"]
        
        #Divise the branch equally between the number of available devices
        self.multy_byte_mlps = nn.ModuleDict([[str(k), MLP_byte({"n_samples":in_features, "num_classes":parameters["num_classes"]}, device_list=self.device_list, device_idx=int(k//self.nk_per_device))] for k in range(self.nk)])

    def forward(self, x):
        #Divise the branch equally between the number of available devices
        x = [self.multy_byte_mlps[str(k)](x) for k in range(self.nk)]
        return x
    
    def fit(self,*args, **kwargs):
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return multi_fit(self, *args, **kwargs)

def multi_criterion(loss_func,outputs,labels):
  losses = 0
  m = nn.LogSoftmax(dim=1)
  for k in range(labels.shape[1]):
    losses += loss_func(m(outputs[k]), labels[:,k].long().to(device))
  return losses/labels.shape[1]

def multi_fit(model, parameters, trainset, valset, Hparams={}, callbacks=[Callbacks.Callback()], verbose=0, *args, **kwargs):
    default_Hparams = {"optimizer":"adam", "weight_init":"he_uniform", "loss_function":"crossentropy", "lr":1e-3, "bs":128, "num_epochs":100}
    Hparams = {**default_Hparams, **Hparams}
    logging.info("fit Hparams: {}".format(Hparams))
    weight_init_func = {"he_uniform":Utils.he_uniform_init_weights, "zero":Utils.zero_init_weights}[Hparams['weight_init'].lower()]
    optimizer_func = {"adam":optim.Adam, "radam":optim.RAdam, "rmsprop":optim.RMSprop, "sgd":optim.SGD}[Hparams['optimizer'].lower()]
    loss_function = {"crossentropy":nn.CrossEntropyLoss(), "mse":nn.MSELoss()}[Hparams['loss_function'].lower()] if isinstance(Hparams['loss_function'], str) else Hparams['loss_function']
    learning_rate = float(Hparams['lr'])
    batch_size = int(Hparams['bs'])
    epochs = int(Hparams['num_epochs'])

    #Create loaders
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, pin_memory=True, num_workers=4)
    valloader = torch.utils.data.DataLoader(valset, batch_size=parameters['val_size'], shuffle=True, pin_memory=True, num_workers=4)#no need for gradient descent

    # model.to(device)
    model.apply(weight_init_func)
    optimizer = optimizer_func(model.parameters(), lr=learning_rate, weight_decay=1e-5)
    # lrsc = optim.lr_scheduler.CosineAnnealingLR(optimizer=optimizer,T_max=100)

    history = {'loss':torch.zeros((epochs), device=device), 'accuracy':torch.zeros((epochs), device=device), 'val_loss':torch.zeros((epochs), device=device), 'val_accuracy':torch.zeros((epochs), device=device)}
    model.train()
    skip = [cb.on_train_begin() for cb in callbacks]
    for epoch in range(epochs):
        start_t = time.time()
        skip = [cb.on_epoch_begin() for cb in callbacks]
        for i, (data, labels) in enumerate(trainloader):
            skip = [cb.on_batch_begin() for cb in callbacks]
            inputs, labels = data.to(device), labels.to(device)
            # forward + backward + optimize
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = multi_criterion(loss_function, outputs, labels)#Multi-task aggregation
            loss.backward()
            skip = [cb.on_loss_end() for cb in callbacks]
            skip = [cb.on_step_begin() for cb in callbacks]
            optimizer.step()
            skip = [cb.on_step_end() for cb in callbacks]
            history['loss'][epoch] += loss.detach()
            history['accuracy'][epoch] += sum([(outputs[k].argmax(dim=1) == labels[:,k].flatten()).sum() for k in range(model.nk)])/model.nk
        history['loss'][epoch] /= (i+1)
        history['accuracy'][epoch] /= parameters['training_size']

        #Validation pass
        with torch.no_grad():
            for i, (data, labels) in enumerate(valloader):
                inputs, labels = data.to(device), labels.to(device)
                # forward only
                outputs = model(inputs)
                loss = multi_criterion(loss_function, outputs, labels)#Multi-task aggregation
                history['val_loss'][epoch] += loss
                history['val_accuracy'][epoch] += sum([(outputs[k].argmax(dim=1) == labels[:,k]).sum() for k in range(model.nk)])/model.nk
            history['val_loss'][epoch] /= (i+1)
            history['val_accuracy'][epoch] /= parameters['val_size']
            skip = [cb.on_epoch_end(model=model, epoch=epoch, history=history, last_epoch=epochs) for cb in callbacks]

        if verbose > 0:
            logger.info("Epoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
        # lrsc.step()
    if verbose == 0:
        logger.info("\nEpoch {}/{} - {:.3f}s - loss: {:.4f} - accuracy: {:.4f} - val_loss: {:.4f} - val_accuracy: {:.4f}".format(epoch+1, epochs, time.time()-start_t, history['loss'][epoch], history['accuracy'][epoch], history['val_loss'][epoch], history['val_accuracy'][epoch]))
    skip = [cb.on_train_end(model) for cb in callbacks]

    #detach and Save metrics in reults folder
    np_history = {}
    for key in history.keys():
        np_history[key] = history[key].detach().cpu().numpy()
    return np_history