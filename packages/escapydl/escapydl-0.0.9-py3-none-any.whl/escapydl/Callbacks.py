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

import os
import numpy as np
import torch
import matplotlib.pyplot as plt
plt.set_loglevel("critical")
import logging 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
from torch.utils import tensorboard

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.debug(device)


def get_attack_parameters(traceset, subkey, index):
    """Returns a dictionary of parameters to be used to search for attack .
    To be used before calling intermediate_value().

    :param traceset: Traceset to use
    :type traceset: dict
    :param subkey: Subkey to target
    :type subkey: int
    :param index: Index of the traceset to use
    :type index: int or slice
    :return: Dictionary of parameters
    :rtype: dict
    """        
    return None

def get_known_key(traceset, subkey, index):
    """Returns the part of the key in traceset that corresponds to the Dataset and subkey
    
    :param traceset: Traceset to use
    :type traceset: dict
    :param subkey: Subkey to target
    :type subkey: int
    :param index: Index of the traceset to use
    :type index: int or slice
    :return: Known key
    :rtype: Any
    """
    return None

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate leakage value. 
    
    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return None


class Callback():
    """Base class for callbacks.
    """
    def __init__(self,*args,**kwargs): 
        self.name = None
    def on_train_begin(self,*args,**kwargs): pass
    def on_train_end(self,*args,**kwargs): pass
    def on_epoch_begin(self,*args,**kwargs): pass
    def on_epoch_end(self,*args,**kwargs): pass
    def on_batch_begin(self,*args,**kwargs): pass
    def on_batch_end(self,*args,**kwargs): pass
    def on_loss_begin(self,*args,**kwargs): pass
    def on_loss_end(self,*args,**kwargs): pass
    def on_step_begin(self,*args,**kwargs): pass
    def on_step_end(self,*args,**kwargs): pass
    def reset(self,*args,**kwargs): pass

class ModelCheckpoint(Callback):
    """Creates a callback that will be called when the epoch end of the training, and will save the model.
    """
    def __init__(self, path, period=50, *args, **kwargs):
        """ Initializes the callback

        :param path: Path to save the model
        :type path: str
        :param period: Interval of epochs between each save (default 50), set to -1 to desactivate saving after each epoch.
        :type period: int, optional
        """
        super(ModelCheckpoint, self).__init__(*args, **kwargs)
        self.name = 'modelcheckpoint'
        self.period = period
        self.path = path
        self.exp_path = path
        os.makedirs(self.exp_path, exist_ok=True)
    
    def reset(self, *args, **kwargs):
        self.period = kwargs['period'] if 'period' in kwargs.keys() else self.period
        self.exp_path = os.path.join(self.path,str(kwargs['trial'].number)) if 'trial' in kwargs.keys() else self.path
        os.makedirs(self.exp_path, exist_ok=True)

    def on_epoch_end(self, model, epoch, *args, **kwargs):
        #Save checkpoints every 'period' epochs in a subfolder
        if self.period != -1:
            if epoch % self.period == 0 and epoch != 0:
                if 'trial' in kwargs.keys():
                    filename = os.path.join(self.exp_path, 'model_trial{}_{:03d}epochs.pt'.format(kwargs['trial'].number, epoch))
                else:
                    filename = os.path.join(self.exp_path, 'model_{:03d}epochs.pt'.format(epoch))
                torch.save(model.state_dict(), filename)
                logger.info("Epoch {}: saving model to {}".format(epoch+1, filename))

    def on_train_end(self, model, *args, **kwargs):
        #Save final model in path
        if 'trial' in kwargs.keys():
            filename = os.path.join(self.exp_path, 'model_trial{}.pt'.format(kwargs['trial'].number))
        else:
            filename = os.path.join(self.exp_path, 'model.pt')
        torch.save(model.state_dict(), filename)
        logger.info("End of training: saving model to {}".format(filename))

class TensorboardCallback(Callback):
    """Creates a callback that will be called when the epoch end of the training, and will write the loss and accuracy in tensorboard.
    """
    def __init__(self, *args, **kwargs):
        """ Initializes the callback

        :param writer: Tensorboard writer
        :type writer: tf.summary.FileWriter, optional
        """
        super().__init__(*args, **kwargs)
        #Get the writer in kwargs
        self.name = 'tensorboard'
        if 'path' in kwargs.keys():
            self.path = kwargs['path']
            self.writer_path = kwargs['path']
            self.writer = tensorboard.SummaryWriter(self.writer_path)
        else:
            self.path = None
            self.writer = None
            self.writer_path = None
        if "callbacks_param" in kwargs.keys():
            self.callbacks_param = kwargs["callbacks_param"]
        else:
            self.callbacks_param = None

    def reset(self, *args, **kwargs):
        if self.path != None:
            self.writer_path = os.path.join(self.path,str(kwargs['trial'].number)) if 'trial' in kwargs.keys() else self.path
            self.writer = tensorboard.SummaryWriter(self.writer_path)

    def on_epoch_end(self, *args, **kwargs):
        #Write train and validation loss and accuracy
        if self.writer != None:
            epoch = kwargs['epoch']
            history = kwargs['history']
            if self.callbacks_param["training_loss"] or self.callbacks_param["training_loss"] == 'True':
                self.writer.add_scalars('metrics/loss', {'training':history['loss'][epoch]}, epoch)
            if self.callbacks_param["training_accuracy"] or self.callbacks_param["training_accuracy"] == 'True':
                self.writer.add_scalars('metrics/accuracy', {'training':history['accuracy'][epoch]}, epoch)
            if self.callbacks_param["validation_loss"] or self.callbacks_param["validation_loss"] == 'True':
                self.writer.add_scalars('metrics/loss', {'validation':history['val_loss'][epoch]}, epoch)
            if self.callbacks_param["validation_accuracy"] or self.callbacks_param["validation_accuracy"] == 'True':
                self.writer.add_scalars('metrics/accuracy', {'validation':history['val_accuracy'][epoch]}, epoch)

class GuessingEntropyCallback(Callback):
    """Creates a callback that will be called when the epoch end of the training, and will compute the guessing entropy of the model.
    If writer is not None, the guessing entropy will be written in the tensorboard as a plot.
    """
    def __init__(self, traceset, subkey=[0], number_of_key_hypothesis=256, epochs=200, rate=10, n_repeat=5, r=0.6, exp_path="experiments/default/", writer_path=None, *args, **kwargs):
        """ Initializes the callback
        
        :param traceset: Attack dataset
        :type traceset: dict
        :param subkey: List of the indexes of the byte key to target (default [0])
        :type subkey: List[int] or int
        :param number_of_key_hypothesis: Number of key hypothesis to consider (default 256)
        :type number_of_key_hypothesis: int, optional
        :param epochs: Number of epochs to consider (default 200)
        :type epochs: int, optional
        :param rate: Interval of epochs between each run of epoch_end() (default 10)
        :type rate: int, optional
        :param n_repeat: Number of repeat to compute GGE (default 20)
        :type n_repeat: int, optional
        :param r: Rate of the generalized guessing entropy (default 0.6)
        :type r: float, optional
        :param writer: Tensorboard writer
        :type writer: tf.summary.FileWriter, optional
        """
        super(GuessingEntropyCallback, self).__init__(*args, **kwargs)
        self.name = 'gge'
        self.epochs = epochs
        self.subkey = subkey if isinstance(subkey, list) else [subkey]
        self.nk = len(self.subkey)
        self.traceset = {"x_attack":traceset["x_val"].to(device), "m_attack":traceset["m_val"]}
        self.attack_size = len(self.traceset["x_attack"])
        self.repeat = n_repeat
        self.r = r # Percentage of traces used to computes gge
        self.Q = int((1-self.r)*self.attack_size)#number of traces used in GGE
        self.number_of_key_hypothesis = number_of_key_hypothesis
        self.rate = int(rate)
        self.e_path = exp_path
        self.exp_path = exp_path
        if rate != -1:
            os.makedirs(exp_path, exist_ok=True)
        self.ge_index = 0
        self.n_ge = int(self.epochs/self.rate)
        self.guessing_entropy = torch.zeros((self.nk,self.n_ge, self.Q)).to(device)
        self.pred = torch.zeros((self.nk, self.Q, self.number_of_key_hypothesis)).to(device)
        self.last_guessing_entropy = torch.zeros((self.nk, self.Q)).to(device)
        self.w_path = writer_path
        self.writer_path = writer_path
        self.writer = tensorboard.SummaryWriter(self.writer_path) if self.writer_path != None else None
        self.patience = 0
        self.stopping_threshold = 10
        self.fit_value = 0
        self.best_fit_value = number_of_key_hypothesis/2

    def reset(self, *args, **kwargs):
        #Renew parameters and reset state
        #TODO: diff between tensorboard_path and experiment_path
        self.epochs = kwargs['epochs'] if 'epochs' in kwargs.keys() else self.epochs
        self.subkey = kwargs['subkey'] if 'subkey' in kwargs.keys() else self.subkey
        self.nk = len(self.subkey)
        self.repeat = kwargs['n_repeat'] if 'n_repeat' in kwargs.keys() else self.repeat
        self.r = kwargs['r'] if 'r' in kwargs.keys() else self.r
        self.Q = int((1-self.r)*self.attack_size)
        self.rate = kwargs['rate'] if 'rate' in kwargs.keys() else self.rate
        self.n_ge = int(self.epochs/self.rate)
        self.guessing_entropy = torch.zeros((self.nk,self.n_ge, self.Q)).to(device)
        self.pred = torch.zeros((self.nk, self.Q, self.number_of_key_hypothesis)).to(device)
        self.last_guessing_entropy = torch.zeros((self.nk, self.Q)).to(device)
        self.patience = 0
        self.stopping_threshold = 10
        self.fit_value = 0
        self.best_fit_value = self.number_of_key_hypothesis/2
        if self.writer != None:
            self.writer_path = os.path.join(self.w_path,str(kwargs['trial'].number)) if 'trial' in kwargs.keys() else self.w_path
            self.writer = tensorboard.SummaryWriter(self.writer_path)
        if self.e_path != None:
            self.exp_path = os.path.join(self.e_path,str(kwargs['trial'].number)) if 'trial' in kwargs.keys() else self.e_path
            os.makedirs(self.exp_path, exist_ok=True)

    def on_train_begin(self, *args, **kwargs):
        self.ge_index = 0
        self.guessing_entropy.zero_()
        return 0

    def on_epoch_end(self, model, epoch, *args, **kwargs):
        """ Function called on every epoch end.

        :param model: The model to get predicitons from.
        :type model: torch.nn.Module
        :param epoch: Index of the current epoch of the training phase.
        :type epoch: int
        """
        if (epoch+1)%self.rate==0:#trigger every 'rate' epochs
            #make predictions for the validation set
            output_probabilities = model(self.traceset["x_attack"])
            if isinstance(output_probabilities, torch.Tensor):
                output_probabilities = output_probabilities.reshape((1,self.attack_size,-1))
            known_key = torch.ByteTensor([get_known_key(self.traceset["m_attack"], sk, 0) for sk in self.subkey]).to(device)# knwon_key in attack set should be the same for all traces
            
            #Compute GGE
            for _ in range(self.repeat):
                #shuffle validation set
                p = torch.randperm(self.attack_size)
                self.traceset["x_attack"] = self.traceset["x_attack"][p]
                for k in range(len(output_probabilities)):
                    output_probabilities[k] = output_probabilities[k][p]
                self.traceset["m_attack"] = {k:self.traceset["m_attack"][k][p] for k in self.traceset["m_attack"].keys()}
                #compute GE for one iteration
                self.pred.zero_()
                # for sk in range(self.nk):#TODO:Is it possible to skip this loop and work on all subkeys at once?
                for kg in range(self.number_of_key_hypothesis):
                    pw_out = torch.stack([intermediate_value(torch.ShortTensor([kg]*self.Q), get_attack_parameters(self.traceset["m_attack"], sk, slice(0,self.Q))) for sk in range(self.nk)])
                    for sk in range(self.nk):
                        self.pred[sk,:,kg] += output_probabilities[sk][:self.Q][torch.arange(self.Q), pw_out[sk].tolist()]
                for index in range(self.Q-1,0,-1):
                    self.pred[:, index] = torch.sum(self.pred[:,:index],dim=1)
                for sk in range(self.nk):
                    self.guessing_entropy[sk, self.ge_index] += torch.nonzero(torch.argsort(self.pred[sk],dim=1,descending=True) == known_key[sk])[:,1]# correct key rank and accumulate in GE

            self.guessing_entropy[:, self.ge_index] /= self.repeat
            avg_bytes_ge = torch.sum(self.guessing_entropy[:, self.ge_index],dim=0)/self.nk
            logger.info(avg_bytes_ge)
            #Save GE, for tensorboard
            if self.writer != None:
                fig = plt.figure()
                for sk in range(self.nk):
                    plt.plot(self.guessing_entropy[sk, self.ge_index].cpu(), label="target {}".format(self.subkey[sk]))
                plt.ylim((0,self.number_of_key_hypothesis))
                plt.title('Guessing Entropy @ epoch {}'.format(epoch))
                self.writer.add_figure('images/gge', fig, self.ge_index)
                plt.close()
                self.writer.add_scalars('metrics/gge', {'gge':avg_bytes_ge[-1]}, epoch)

            if 'trial' in kwargs.keys():
                #Report intermediate value metric if chosen metric is gge
                self.fit_value = torch.sum(self.guessing_entropy[:,self.ge_index])/(self.nk*len(self.guessing_entropy[0,self.ge_index]))
                kwargs['trial'].set_user_attr("guessingEntropy", self.guessing_entropy[:,self.ge_index].tolist())
                if 'metric' in kwargs.keys():
                    if kwargs['metric'] == 'gge':
                        kwargs['trial'].report(self.fit_value, step=epoch)

                # Early stopping based on average of GE
                if self.fit_value < self.best_fit_value:
                    self.best_fit_value = self.fit_value
                    self.patience = 0
                else:
                    self.patience += 1
                if self.patience >= self.stopping_threshold:
                    logger.info("early stopping based on gge")
                    model.stop_training = True
            self.ge_index += 1

    def on_train_end(self, *args, **kwargs):
        # Save GE to npy file
        guessingEntropy = self.guessing_entropy.detach().cpu().numpy()
        if 'trial' in kwargs.keys():
            filename = os.path.join(self.exp_path, "GE_trail{}.npy".format(kwargs['trial'].number))
        else:
            filename = os.path.join(self.exp_path, 'GE.npy')
        np.save(filename, guessingEntropy)
        self.patience = 0 #Reset patience
        # Return GE as Dict with a numpy array
        return {"GE":guessingEntropy}
        
    def get_fit_value(self):
        return self.fit_value
    
    def get_guessing_entropy(self):
        return self.guessing_entropy.detach().cpu().numpy()
    

def init_callbacks(callbacks:dict, **kwargs):
    """Initialize callbacks from a dictionary of callbacks.
    
    :param callbacks: Dictionary of callbacks
    :type callbacks: dict
    :return: List of callbacks
    :rtype: list
    """
    callbacks_list = []
    for callback_name in callbacks.keys():
        if callback_name.lower() == 'modelcheckpoint':
            callbacks_list.append(ModelCheckpoint(path=kwargs["exp_path"], 
                                                  period=int(callbacks[callback_name]["period"])))
        elif callback_name.lower() == 'tensorboard':
            callbacks_list.append(TensorboardCallback(path=kwargs['writer_path'], callbacks_param=callbacks[callback_name]))
        elif callback_name.lower() == 'guessingentropy':
            callbacks_list.append(GuessingEntropyCallback(traceset=kwargs["traceset"], 
                                                          subkey=kwargs["parameters"]["subkey"], 
                                                          number_of_key_hypothesis=int(kwargs["parameters"]["num_key_hypotheses"]), 
                                                          epochs=int(kwargs["Hparams"]["num_epochs"]) if 'Hparams' in kwargs.keys() else 100, 
                                                          rate=int(callbacks[callback_name]["ge_rate"]), 
                                                          n_repeat=int(callbacks[callback_name]["n_repeat"]), 
                                                          r=float(callbacks[callback_name]["r"]), 
                                                          exp_path=kwargs["exp_path"], 
                                                          writer_path=kwargs["writer_path"]))
        else:
            logger.warning("Callback {} not implemented".format(callback_name))
    return callbacks_list