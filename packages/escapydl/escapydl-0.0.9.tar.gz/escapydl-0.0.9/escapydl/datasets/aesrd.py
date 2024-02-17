import os
import torch
import helpers.aes_helper as aes

#Dataset parameters
parameters = {
    "dataset_name"        : os.getcwd() + '/data/aes_rd.trs',
    "dataset_size"        : 50000,
    "training_size"       : 40000,
    "val_size"            : 10000,
    "subkey"              : 2,
    "num_key_hypotheses"  : 256,
    "n_samples"           : 3500,
    "r"                   : 0.6,
    "n_repeat"            : 5,
    "ge_rate"             : 5,
    "shuffle"             : False,
}

model = {
    "num_epochs"          : 100,
    "loss_function"       : torch.nn.CrossEntropyLoss(),
    "bs"                  : 128,
    "lr"                  : 1e-3,
}

hp_search_s = {
    "activation_function_s" : ["relu"],
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
    return {'p':traceset["plaintext"][index,subkey], 
            'k':traceset["key"][index,subkey],
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return traceset['key'][index][subkey]

def intermediate_value(keyguess, trace_parameters):
    """Return the intermediate value of a key in the SBox . 
    First xor corresponds to the plaintext blinding, then we do addRoundKey with key guess and apply rsm fo subBytes

    :param trace_parameters: Dictionary containing the trace parameters for intermediate value computation
    :type trace_parameters: dict
    :return: Intermediate value
    :rtype: Any
    """
    if isinstance(trace_parameters['p'], torch.Tensor):
        return torch.index_select(aes.sbox, 0, (trace_parameters['p'] ^ keyguess).int())
    else:
        return aes.sbox.numpy()[trace_parameters['p'] ^ keyguess]