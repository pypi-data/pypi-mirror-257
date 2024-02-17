import torch
import optuna
import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../escapydl/')))

## Test functions in Optuna_models.py
def test_is_function_local():
    from escapydl.Optuna_models import is_function_local
    assert is_function_local(lambda x: x) == False, "expected output: {}, actual output: {}".format(False, is_function_local(lambda x: x))

def test_make_MLP():
    from escapydl.Optuna_models import objective_hp
    __DL_type__ = "make_MLP"
    study_name = "unit_test_make_MLP"
    db_name = "sqlite:///unit_test_make_MLP.db"

    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }

    trace_data = {"x_train":torch.randn(10,10),
                  "x_val":torch.randn(2,10),
                  "m_train":{"label":torch.randint(0, 2, (10,))},
                  "m_val":{"label":torch.randint(0, 2, (2,))},
                  }

    hp_search_s = {
        "activation_function_s": ['relu', 'tanh', 'selu'],
        "epochs": [1,1,1], 
        "bs": [32,128,32],
        "loss_function_s": ["crossentropy"],
        "n_neurons_s": [10,20,10], 
        "n_layers_s": [1,1,1], 
        "kernel_size_s": [3,8,1],
        "n_conv_block_s": [1,1,1],
        "optimizer_s": ["Adam"], 
        "lr_s": [1e-3,1e-3,'log']
    }

    metric, direction = "None", "minimize"
    objective = objective_hp(parameters=parameters,
                        hp_search_s=hp_search_s,
                        trace_data=trace_data,
                        verbose=1,
                        model_name=__DL_type__,
                        metric=metric
                    )
    pruner = optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5, interval_steps=1), patience=30)
    
    study = optuna.create_study(sampler=optuna.samplers.TPESampler(), 
                                direction=direction, 
                                pruner=pruner, 
                                study_name=study_name, 
                                storage=db_name)
    study.optimize(objective, n_trials=1, timeout=None)
    assert os.path.exists("unit_test_make_MLP.db") == True, "expected output: {}, actual output: {}".format(True, os.path.exists("unit_test_make_MLP.db"))
    os.remove("unit_test_make_MLP.db")

def test_make_CNN():
    from escapydl.Optuna_models import objective_hp
    __DL_type__ = "make_CNN"
    study_name = "unit_test_make_CNN"
    db_name = "sqlite:///unit_test_make_CNN.db"

    parameters = {
        "n_samples": 10,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }

    trace_data = {"x_train":torch.randn(10,1,10),
                  "x_val":torch.randn(2,1,10),
                  "m_train":{"label":torch.randint(0, 2, (10,))},
                  "m_val":{"label":torch.randint(0, 2, (2,))},
                  }

    hp_search_s = {
        "activation_function_s": ['relu', 'tanh', 'selu'],
        "epochs": [1,1,1], 
        "bs": [32,128,32],
        "loss_function_s": ["crossentropy"],
        "n_neurons_s": [10,20,10], 
        "n_layers_s": [1,1,1], 
        "kernel_size_s": [3,8,1],
        "n_conv_block_s": [1,1,1],
        "optimizer_s": ["Adam"], 
        "lr_s": [1e-3,1e-3,'log']
    }

    metric, direction = "None", "minimize"
    objective = objective_hp(parameters=parameters,
                        hp_search_s=hp_search_s,
                        trace_data=trace_data,
                        verbose=1,
                        model_name=__DL_type__,
                        metric=metric
                    )
    pruner = optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5, interval_steps=1), patience=30)
    
    study = optuna.create_study(sampler=optuna.samplers.TPESampler(), 
                                direction=direction, 
                                pruner=pruner, 
                                study_name=study_name, 
                                storage=db_name)
    study.optimize(objective, n_trials=1, timeout=None)
    assert os.path.exists("unit_test_make_CNN.db") == True, "expected output: {}, actual output: {}".format(True, os.path.exists("unit_test_make_CNN"))
    os.remove("unit_test_make_CNN.db")

def test_make_CNN_simpler():
    from escapydl.Optuna_models import objective_hp
    __DL_type__ = "make_CNN_simpler"
    study_name = "unit_test_make_CNN_simpler"
    db_name = "sqlite:///unit_test_make_CNN_simpler.db"

    parameters = {
        "n_samples": 1000,
        "num_classes": 2,
        "training_size": 10,
        "val_size": 2,
    }

    trace_data = {"x_train":torch.randn(10,1,1000),
                  "x_val":torch.randn(2,1,1000),
                  "m_train":{"label":torch.randint(0, 2, (10,))},
                  "m_val":{"label":torch.randint(0, 2, (2,))},
                  }

    hp_search_s = {
        "activation_function_s": ['relu', 'tanh', 'selu'],
        "epochs": [1,1,1], 
        "bs": [32,128,32],
        "loss_function_s": ["crossentropy"],
        "n_neurons_s": [10,20,10], 
        "n_layers_s": [1,1,1], 
        "kernel_size_s": [3,8,1],
        "n_conv_block_s": [1,1,1],
        "optimizer_s": ["Adam"], 
        "lr_s": [1e-3,1e-3,'log']
    }

    metric, direction = "None", "minimize"
    objective = objective_hp(parameters=parameters,
                        hp_search_s=hp_search_s,
                        trace_data=trace_data,
                        verbose=1,
                        model_name=__DL_type__,
                        metric=metric
                    )
    pruner = optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=5, interval_steps=1), patience=30)
    
    study = optuna.create_study(sampler=optuna.samplers.TPESampler(), 
                                direction=direction, 
                                pruner=pruner, 
                                study_name=study_name, 
                                storage=db_name)
    study.optimize(objective, n_trials=1, timeout=None)
    assert os.path.exists("unit_test_make_CNN_simpler.db") == True, "expected output: {}, actual output: {}".format(True, os.path.exists("unit_test_make_CNN_simpler"))
    os.remove("unit_test_make_CNN_simpler.db")

def test_objective_hp():
    assert True, "already covered"


if __name__ == "__main__":
    test_is_function_local()
    print("test_is_function_local passed")

    test_make_MLP()
    print("test_make_MLP passed")

    test_make_CNN()
    print("test_make_CNN passed")

    test_make_CNN_simpler()
    print("test_make_CNN_simpler passed")

    test_objective_hp()
    print("test_objective_hp passed")