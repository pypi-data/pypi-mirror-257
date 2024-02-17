import os
import torch
import helpers.aes_helper as aes

#Dataset parameters (dpav4 containing mask encryption leakage of all 16 bytes)
parameters = {
    "dataset_name"        : 'data/encryption_dpav42_10000.trs',
    "dataset_size"        : 4500,
    "training_size"       : 3500,
    "val_size"            : 1000,
    "subkey"              : [k for k in range(16)],
    "num_key_hypotheses"  : 256,
    "n_samples"           : 40000,
    "shuffle"             : True,
    "pre_trained_model"   : 'experiments/dpav4_n/CNN/20231219_093134/last_models/last_model.pt',
}

model = {
    "num_epochs"          : 10,
    "loss_function"       : torch.nn.CrossEntropyLoss(),
    "bs"                  : 128,
    "lr"                  : 1e-3,
    "n_conv_blocks"       : 2,
    "kernel_size_0": 11, 
    "c_out_0": 8,
    "kernel_size_1": 11,
    "c_out_1": 16,
    "n_layers": 2,
    "n_units_l0": 100,
    "n_units_l1": 100,
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

#the mask is fixed and public. a random number "offset" is drawn at the beggining (here known here) and shift the mask.
#AES RSM schedule is : x = plaintext ^ mask_offset and then add the round key and do the masked subbytes: sbox[x ^ key ^ M_i] ^ M_i+1, where i is offset+subkey+round (here round is 0)
mask = torch.ByteTensor([
    0x03, 0x0c, 0x35, 0x3a, 0x50, 0x5f, 0x66, 0x69, 0x96, 0x99, 0xa0, 0xaf, 0xc5, 0xca, 0xf3, 0xfc
])

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
            'o':traceset["offset"][index,subkey], 
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
        return torch.index_select(aes.sbox, 0, (trace_parameters['p'] ^ keyguess).int()) ^ torch.index_select(mask, 0, ((trace_parameters['o']+1)%16).int())
    else:
        return aes.sbox.numpy()[(trace_parameters['p'] ^ keyguess)] ^ mask.numpy()[(trace_parameters['o']+1)%16]
