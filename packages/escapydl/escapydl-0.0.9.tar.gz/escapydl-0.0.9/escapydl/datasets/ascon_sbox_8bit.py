import os
import torch
import helpers.ascon_helper as ascon

sbox_chunk_size = 8
parameters = {
    "dataset_name"        : "data/ascon_cw_unprotected.h5",
    "dataset_size"        : 100000,
    "training_size"       : 50000,
    "val_size"            : 10000,
    "subkey"              : 1,
    "num_key_hypotheses"  : 2**sbox_chunk_size,
    "n_samples"           : 772,#Random key
    "r"                   : 0.8,
    "n_repeat"            : 50,
    "ge_rate"             : 5,
    "shuffle"             : True,
    "chunk_size"          : sbox_chunk_size,
}

model = {
    "loss_function"       : torch.nn.CrossEntropyLoss(),
    "lr"                  : 1e-05,
    "bs"                  : 128,
    "num_epochs"          : 500,
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
    return {'nonce0':traceset["nonce0"][index], 
            'nonce1':traceset["nonce1"][index], 
            'k':traceset["key"][index],
            'subkey':subkey}

def get_known_key(traceset, subkey, index):
    return ascon.select_subkey_sbox_chunk(subkey, traceset['key'][index], parameters["chunk_size"])

def intermediate_value(keyguess, trace_parameters):
    return ascon.intermediate_value_sbox_chunk(keyguess,trace_parameters, parameters["chunk_size"])