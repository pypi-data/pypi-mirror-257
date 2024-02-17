import os
import torch
import helpers.ascon_helper as ascon

parameters = {
    "dataset_name"        : 'data/ASCON_Encrypt_60000_20230404_132906_sbox_chunk_random_mlpsca_ready.trs',#Random key
    "dataset_size"        : 60000,
    "training_size"       : 50000,
    "val_size"            : 10000,
    "subkey"              : 0,
    "chunk_size"          : 8,
    "num_key_hypotheses"  : 1<<(2*8),
    "n_samples"           : 772,#Random key
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
            'k':traceset["key"][index],
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return ascon.select_subkey_sbox_chunk(subkey, traceset['key'][index])

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    nonce0 and nonce1 should be byte arrays of size (8) as they both are half of the nonce length (16 bytes).
    k should be a 2-bit value as an integer. This bit corresponds to the part of the key concerned in the attack given subkey.

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """        
    return ascon.intermediate_value_sbox_chunk(keyguess,trace_parameters,self.parameters['chunk_size'])