import torch
import numpy as np
import sys,os
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

## Test functions in Callbakcs.py
def test_get_attack_parameters():
    from escapydl.Callbacks import get_attack_parameters
    assert get_attack_parameters(0,0,0) == None

def test_get_known_key():
    from escapydl.Callbacks import get_known_key
    assert get_known_key(0,0,0) == None

def test_intermediate_value():
    from escapydl.Callbacks import intermediate_value
    assert intermediate_value(0,0) == None

def test_callback():
    from escapydl.Callbacks import Callback
    callback = Callback()
    assert callback.on_train_begin() == None
    assert callback.on_train_end() == None
    assert callback.on_epoch_begin() == None
    assert callback.on_epoch_end() == None
    assert callback.on_batch_begin() == None
    assert callback.on_batch_end() == None
    assert callback.on_loss_begin() == None
    assert callback.on_loss_end() == None
    assert callback.on_step_begin() == None
    assert callback.on_step_end() == None
    assert callback.reset() == None

def test_ModelCheckpoint():
    from escapydl.Callbacks import ModelCheckpoint
    path = "model_checkpoint_unit_test"
    period = 1
    callback = ModelCheckpoint(path, period=period)
    assert os.path.exists(path) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(path))
    callback.reset()
    model = torch.nn.Linear(10, 10)
    callback.on_epoch_end(model,epoch=1)
    assert os.path.exists(os.path.join(path, 'model_{:03d}epochs.pt'.format(1))) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(os.path.join(path, 'model_{:03d}epochs.pt'.format(0))))
    os.remove(os.path.join(path, 'model_{:03d}epochs.pt'.format(1)))
    callback.on_train_end(model)
    assert os.path.exists(os.path.join(path, 'model.pt')) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(os.path.join(path, 'model.pt')))
    os.remove(os.path.join(path, 'model.pt'))
    os.rmdir(path)

def test_TensorboardCallback():
    from escapydl.Callbacks import TensorboardCallback
    callback = TensorboardCallback()
    callback.reset()
    callback.on_epoch_end()
    #There is nothing to test here, since the callback is empty, but it should pass without errors
    path = "tensorboard_callback_unit_test"
    callback = TensorboardCallback(path=path,callbacks_param={"training_loss":"True", "validation_loss":"True", "training_accuracy":"True", "validation_accuracy":"True"})
    assert os.path.exists(path) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(path))
    callback.reset()
    callback.on_epoch_end(epoch=0, history={"loss":[1], "accuracy":[1], "val_loss":[1], "val_accuracy":[1]})
    assert True
    shutil.rmtree(path)

def test_GuessingEntropyCallback():
    from escapydl.Callbacks import GuessingEntropyCallback
    from escapydl import Callbacks
    Callbacks.get_known_key = lambda traceset, subkey, index: traceset["key"][index]
    Callbacks.intermediate_value = lambda key, attack_parameters: key
    traceset = {
        "x_val" : torch.randn(10, 10),
        "m_val" : {
            "key": torch.ByteTensor([0,0,0,0,0,0,0,0,0,0]),
            "label": torch.randint(0, 2, (10, 1))
        }
    }
    exp_path = "guessing_entropy_callback_unit_test"
    writer_path = "guessing_entropy_callback_unit_test_writter"
    callback = GuessingEntropyCallback(traceset=traceset, 
                                       subkey=[0],
                                       number_of_key_hypothesis=2,
                                       epochs=3,
                                       rate = 1,
                                       n_repeat=1,
                                       r = 0.6,
                                       Hparams={"num_classes":2}, 
                                       exp_path=exp_path, 
                                       writer_path=writer_path)
    assert os.path.exists(exp_path) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(exp_path))
    assert os.path.exists(writer_path) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(writer_path))
    callback.reset()
    assert callback.on_train_begin() == 0
    model = torch.nn.Linear(10, 2)
    callback.on_epoch_end(model, epoch=0)
    callback.on_train_end()
    assert os.path.exists(os.path.join(exp_path, 'GE.npy')) == True, "expected output: {}, actual output: {}".format(True, os.path.exists(os.path.join(exp_path, 'GE.npy')))
    shutil.rmtree(exp_path)
    shutil.rmtree(writer_path)
    fit_value = callback.get_fit_value()
    assert fit_value == 0, "expected output: {}, actual output: {}".format(0, fit_value)
    ge = callback.get_guessing_entropy()
    assert ge.shape == (1,3,4), "expected output: {}, actual output: {}".format((1,3,4), ge.shape)

def test_init_callbacks():
    from escapydl.Callbacks import init_callbacks
    from escapydl import Callbacks
    Callbacks.get_known_key = lambda traceset, subkey, index: traceset["key"][index]
    Callbacks.intermediate_value = lambda key, attack_parameters: key
    traceset = {
        "x_val" : torch.randn(10, 10),
        "m_val" : {
            "key": torch.ByteTensor([0,0,0,0,0,0,0,0,0,0]),
            "label": torch.randint(0, 2, (10, 1))
        }
    }
    Hparams = {"num_classes":2,
               "num_epochs": 3,}
    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
        "subkey": [0,1],
        "num_key_hypotheses": 2,
    }
    exp_path = "init_callbacks_unit_test"
    writer_path = "init_callbacks_unit_test_writter"
    callbacks_params = {
        "modelcheckpoint": {
            "path": exp_path,
            "period": 1
        },
        "tensorboard": {
            "path": writer_path,
            "callbacks_param": {
                "training_loss": "True", 
                "validation_loss": "True", 
                "training_accuracy": "True", 
                "validation_accuracy": "True"
            }
        },
        "guessingentropy": {
            "ge_rate": 1,
            "n_repeat": 1,
            "r": 0.6,
        }
    }
    callbacks = init_callbacks(callbacks_params, 
                               traceset=traceset, 
                               Hparams=Hparams, 
                               parameters=parameters, 
                               exp_path=exp_path, 
                               writer_path=writer_path)
    assert len(callbacks) == 3, "expected output: {}, actual output: {}".format(3, len(callbacks))
    shutil.rmtree(exp_path)
    shutil.rmtree(writer_path)

if __name__ == "__main__":
    test_get_attack_parameters()
    print("test_get_attack_parameters passed")

    test_get_known_key()
    print("test_get_known_key passed")

    test_intermediate_value()
    print("test_intermediate_value passed")

    test_callback()
    print("test_callback passed")

    test_ModelCheckpoint()
    print("test_ModelCheckpoint passed")

    test_TensorboardCallback()
    print("test_TensorboardCallback passed")

    test_GuessingEntropyCallback()
    print("test_GuessingEntropyCallback passed")

    test_init_callbacks()
    print("test_init_callbacks passed")