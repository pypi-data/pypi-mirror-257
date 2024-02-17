import torch
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../escapydl/')))

traceset = {
    "plaintext" : torch.randint(0, 256, (2,16), dtype=torch.uint8),
    "key"       : torch.randint(0, 256, (2,16), dtype=torch.uint8),
    "offset"    : torch.randint(0, 256, (2,16), dtype=torch.uint8),
}
subkey = 0
index = 0

## Test all dataset functions

## AESRD
def test_aesrd_get_attack_parameters():
    from escapydl.datasets.aesrd import get_attack_parameters
    output = get_attack_parameters(traceset, subkey, index)
    assert output == {'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, "expected output: {}, actual output: {}".format({'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, output)

def test_aesrd_get_known_key():
    from escapydl.datasets.aesrd import get_known_key
    output = torch.Tensor(get_known_key(traceset, subkey, index))
    assert output == torch.Tensor(traceset["key"][index,subkey]), "expected output: {}, actual output: {}".format(torch.Tensor(traceset["key"][index,subkey]), output)

def test_aesrd_intermediate_value():
    from escapydl.datasets.aesrd import intermediate_value, get_attack_parameters, get_known_key
    output = intermediate_value(get_known_key(traceset, subkey, index), get_attack_parameters(traceset, subkey, index))
    assert output.shape == (1,), "expected output: {}, actual output: {}".format((1,), output.shape)

## ASCAD_fixed
def test_ascad_fixed_get_attack_parameters():
    from escapydl.datasets.ascad_fixed import get_attack_parameters
    output = get_attack_parameters(traceset, subkey, index)
    assert output == {'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, "expected output: {}, actual output: {}".format({'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, output)

def test_ascad_fixed_get_known_key():
    from escapydl.datasets.ascad_fixed import get_known_key
    output = torch.Tensor(get_known_key(traceset, subkey, index))
    assert output == torch.Tensor(traceset["key"][index,subkey]), "expected output: {}, actual output: {}".format(torch.Tensor(traceset["key"][index,subkey]), output)

def test_ascad_fixed_intermediate_value():
    from escapydl.datasets.ascad_fixed import intermediate_value, get_attack_parameters, get_known_key
    output = intermediate_value(get_known_key(traceset, subkey, index), get_attack_parameters(traceset, subkey, index))
    assert output.shape == (1,), "expected output: {}, actual output: {}".format((1,), output.shape)

## ASCAD_random
def test_ascad_random_get_attack_parameters():
    from escapydl.datasets.ascad_random import get_attack_parameters
    output = get_attack_parameters(traceset, subkey, index)
    assert output == {'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, "expected output: {}, actual output: {}".format({'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'subkey':subkey}, output)

def test_ascad_random_get_known_key():
    from escapydl.datasets.ascad_random import get_known_key
    output = torch.Tensor(get_known_key(traceset, subkey, index))
    assert output == torch.Tensor(traceset["key"][index,subkey]), "expected output: {}, actual output: {}".format(torch.Tensor(traceset["key"][index,subkey]), output)

def test_ascad_random_intermediate_value():
    from escapydl.datasets.ascad_random import intermediate_value, get_attack_parameters, get_known_key
    output = intermediate_value(get_known_key(traceset, subkey, index), get_attack_parameters(traceset, subkey, index))
    assert output.shape == (1,), "expected output: {}, actual output: {}".format((1,), output.shape)

## DPAv4
def test_dpav4_get_attack_parameters():
    from escapydl.datasets.dpav4 import get_attack_parameters
    output = get_attack_parameters(traceset, subkey, index)
    assert output == {'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'o':traceset["offset"][index,subkey], 'subkey':subkey}, "expected output: {}, actual output: {}".format({'p': traceset["plaintext"][index,subkey], 'k': traceset["key"][index,subkey], 'o':traceset["offset"][index,subkey], 'subkey':subkey}, output)

def test_dpav4_get_known_key():
    from escapydl.datasets.dpav4 import get_known_key
    output = torch.Tensor(get_known_key(traceset, subkey, index))
    assert output == torch.Tensor(traceset["key"][index,subkey]), "expected output: {}, actual output: {}".format(torch.Tensor(traceset["key"][index,subkey]), output)

def test_dpav4_intermediate_value():
    from escapydl.datasets.dpav4 import intermediate_value, get_attack_parameters, get_known_key
    output = intermediate_value(get_known_key(traceset, subkey, index), get_attack_parameters(traceset, subkey, index))
    assert output.shape == (1,), "expected output: {}, actual output: {}".format((1,), output.shape)

if __name__ == "__main__":
    test_aesrd_get_attack_parameters()
    print("test_aesrd_get_attack_parameters passed")

    test_aesrd_get_known_key()
    print("test_aesrd_get_known_key passed")

    test_aesrd_intermediate_value()
    print("test_aesrd_intermediate_value passed")

    test_ascad_fixed_get_attack_parameters()
    print("test_ascad_fixed_get_attack_parameters passed")

    test_ascad_fixed_get_known_key()
    print("test_ascad_fixed_get_known_key passed")

    test_ascad_fixed_intermediate_value()
    print("test_ascad_fixed_intermediate_value passed")

    test_ascad_random_get_attack_parameters()
    print("test_ascad_random_get_attack_parameters passed")

    test_ascad_random_get_known_key()
    print("test_ascad_random_get_known_key passed")

    test_ascad_random_intermediate_value()
    print("test_ascad_random_intermediate_value passed")

    test_dpav4_get_attack_parameters()
    print("test_dpav4_get_attack_parameters passed")

    test_dpav4_get_known_key()
    print("test_dpav4_get_known_key passed")

    test_dpav4_intermediate_value()
    print("test_dpav4_intermediate_value passed")