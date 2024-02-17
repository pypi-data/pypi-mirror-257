import torch
import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../escapydl/')))

## Test functions in Models.py

def test_MLP():
    from escapydl.Models import MLP
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }
    Hparams = {
        "num_epochs": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = MLP(parameters=parameters, Hparams=Hparams)
    input = torch.randn(10, 10)
    output = m(input)
    assert output.shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output.shape)
    trainset = torch.utils.data.TensorDataset(torch.randn(10,10), torch.randint(0, 2, (10,)))
    valset = torch.utils.data.TensorDataset(torch.randn(2,10), torch.randint(0, 2, (2,)))
    h = m.fit(trainset=trainset, 
                valset=valset, 
                parameters=parameters, 
                Hparams = Hparams,
                verbose=1,)
    assert isinstance(h,dict), "expected output: {}, actual output: {}".format(dict, type(h))

def test_CNN():
    from escapydl.Models import CNN
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }
    Hparams = {
        "num_epochs": 3,
        "n_conv_block": 1,
        "kernel_size_0": 3, 
        "c_out_0": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = CNN(parameters=parameters, Hparams=Hparams)
    input = torch.randn((10, 1, 10))
    output = m(input)
    assert output.shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output.shape)
    trainset = torch.utils.data.TensorDataset(torch.randn(10,1,10), torch.randint(0, 2, (10,)))
    valset = torch.utils.data.TensorDataset(torch.randn(2,1,10), torch.randint(0, 2, (2,)))
    h = m.fit(trainset=trainset, 
                valset=valset, 
                parameters=parameters, 
                Hparams = Hparams,
                verbose=1,)
    assert isinstance(h,dict), "expected output: {}, actual output: {}".format(dict, type(h))

def test_payAttentionNN():
    from escapydl.Models import payAttentionNN
    parameters = {
        "n_samples": 100,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }
    Hparams = {
        "num_epochs": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = payAttentionNN(parameters=parameters, Hparams=Hparams)
    input = torch.randn(10, 1, 100)
    output = m(input)
    assert output.shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output.shape)
    trainset = torch.utils.data.TensorDataset(torch.randn(10,1,100), torch.randint(0, 2, (10,)))
    valset = torch.utils.data.TensorDataset(torch.randn(2,1,100), torch.randint(0, 2, (2,)))
    h = m.fit(trainset=trainset, 
                valset=valset, 
                parameters=parameters, 
                Hparams = Hparams,
                verbose=1,)
    assert isinstance(h,dict), "expected output: {}, actual output: {}".format(dict, type(h))

def test_MLP_byte():
    from escapydl.Models import MLP_byte
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }
    Hparams = {
        "num_epochs": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = MLP_byte(parameters=parameters, Hparams=Hparams)
    input = torch.randn(10, 10)
    output = m(input)
    assert output.shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output.shape)

def test_CNN_multi_bytes():
    from escapydl.Models import CNN_multi_bytes
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }
    Hparams = {
        "num_epochs": 3,
        "n_conv_block": 1,
        "kernel_size_0": 3, 
        "c_out_0": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = CNN_multi_bytes(parameters=parameters, Hparams=Hparams)
    input = torch.randn((10, 1, 10))
    output = m(input)
    assert output.shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output.shape)

def test_fit():
    assert True, "Already covered"

def test_CNN_multi_bytes():
    from escapydl.Models import CNN_multi_bytes
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
        "subkey": [0,1],
    }
    Hparams = {
        "num_epochs": 3,
        "n_conv_block": 1,
        "kernel_size_0": 3, 
        "c_out_0": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = CNN_multi_bytes(parameters=parameters, Hparams=Hparams)
    input = torch.randn((10, 1, 10))
    output = m(input)
    assert len(output) == 2, "expected output: {}, actual output: {}".format(2, len(output))
    assert output[0].shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output[0].shape)
    assert output[1].shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output[1].shape)
    trainset = torch.utils.data.TensorDataset(torch.randn(10,1,10), torch.randint(0, 2, (10,2)))
    valset = torch.utils.data.TensorDataset(torch.randn(2,1,10), torch.randint(0, 2, (2,2)))
    m.fit(trainset=trainset, 
            valset=valset, 
            parameters=parameters, 
            Hparams = Hparams,
            verbose=1,)
    
def test_MLP_multi_bytes():
    from escapydl.Models import MLP_multi_bytes
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
        "subkey": [0,1],
    }
    Hparams = {
        "num_epochs": 3,
        "n_layers": 1,
        "n_units_l0": 10,
    }
    m = MLP_multi_bytes(parameters=parameters, Hparams=Hparams)
    input = torch.randn(10, 10)
    output = m(input)
    assert len(output) == 2, "expected output: {}, actual output: {}".format(2, len(output))
    assert output[0].shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output[0].shape)
    assert output[1].shape == (10,2), "expected output: {}, actual output: {}".format((10,2), output[1].shape)
    trainset = torch.utils.data.TensorDataset(torch.randn(10,10), torch.randint(0, 2, (10,2)))
    valset = torch.utils.data.TensorDataset(torch.randn(2,10), torch.randint(0, 2, (2,2)))
    m.fit(trainset=trainset, 
            valset=valset, 
            parameters=parameters, 
            Hparams = Hparams,
            verbose=1,)
    
def test_multi_criterion():
    from escapydl.Models import multi_criterion
    loss_function = torch.nn.CrossEntropyLoss()
    outputs = torch.randn(2,10,2)
    labels = torch.randint(0, 2, (10,2))
    loss = multi_criterion(loss_function, outputs, labels)
    assert loss.dim() == 0, "expected output: {}, actual output: {}".format(0, loss.dim())

def test_multi_fit():
    assert True, "Already covered"

if __name__ == "__main__":
    test_MLP()
    print("test_MLP passed")

    test_CNN()
    print("test_CNN passed")

    test_payAttentionNN()
    print("test_payAttentionNN passed")

    test_MLP_byte()
    print("test_MLP_byte passed")

    test_fit()
    print("test_fit passed")

    test_CNN_multi_bytes()
    print("test_CNN_multi_bytes passed")

    test_MLP_multi_bytes()
    print("test_MLP_multi_bytes passed")

    test_multi_criterion()
    print("test_multi_criterion passed")

    test_multi_fit()
    print("test_multi_fit passed")