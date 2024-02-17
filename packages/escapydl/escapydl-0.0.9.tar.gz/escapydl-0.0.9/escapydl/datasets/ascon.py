import os
import torch
import helpers.ascon_helper as ascon

parameters = {
    "dataset_name"        : "data/ascon_cw_unprotected.h5",
    "dataset_size"        : 100000,
    "training_size"       : 50000,
    "val_size"            : 10000,
    "subkey"              : 0,
    "num_key_hypotheses"  : 8,
    "n_samples"           : 772,
    "r"                   : 0.6,
    "n_repeat"            : 50,
    "ge_rate"             : 5,
    "shuffle"             : True,
}

model = {
    "num_epochs"          : 50,
    "loss_function"       : torch.nn.CrossEntropyLoss(),
    "lr"                  : 1e-03,
    "bs"                  : 128,
}

hp_search_s = {
    "num_epochs"            : [10, 500, 10],
    "lr"                    : [1e-05, 1e-03, 'log'],
    "bs"                    : [128, 512, 1],
    "n_neurons_s"           : [10, 500, 10], 
    "n_layers_s"            : [1, 5, 1], 
    "kernel_size_s"         : [3, 80, 1],
    "n_conv_block_s"        : [0, 3, 1],
}

callbacks = {
    "modelcheckpoint":{
        "period":-1,
    },
    "guessingentropy":{
        "ge_rate":5,
        "n_repeat":5,
        "r":0.6,
    },
    "tensorboard":{
        "training_accuracy":True,
        "validation_accuracy":True,
        "training_loss":True,
        "validation_loss":True,
    },
}

def get_attack_parameters(traceset, subkey, index):
    """Returns a dictionary of parameters to be used to search for attack .
    To be used before calling intermediate_value().

    :param traceset: Traceset to use
    :type traceset: dict
    :param subkey: Subkey to attack
    :type subkey: int
    :param index: Index of the traceset to use
    :type index: int or slice
    :return: Dictionary of parameters
    :rtype: dict
    """        
    return {'nonce0':traceset["nonce0"][index], 
            'nonce1':traceset["nonce1"][index], 
            'k':ascon.select_subkey(subkey, traceset["key"][index]),
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return ascon.select_subkey(subkey, traceset['key'][index])

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 3-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return ascon.intermediate_value(keyguess,trace_parameters)