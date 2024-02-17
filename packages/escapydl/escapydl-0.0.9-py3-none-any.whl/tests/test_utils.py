import torch
import numpy as np
import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

## Test functions in Utils.py
def test_he_uniform_init_weights():
    from escapydl.Utils import he_uniform_init_weights    
    m = torch.nn.Linear(10, 10)
    he_uniform_init_weights(m)
    assert m.weight.shape == (10, 10), "expected output: {}, actual output: {}".format((10, 10), m.weight.shape)
    assert m.bias.shape == (10,), "expected output: {}, actual output: {}".format((10,), m.bias.shape)

def test_zero_init_weights():
    from escapydl.Utils import zero_init_weights
    m = torch.nn.Linear(10, 10)
    zero_init_weights(m)
    assert (m.weight == torch.zeros((10, 10))).all(), "expected output: {}, actual output: {}".format(torch.zeros((10, 10)), m.weight)
    assert (m.bias == torch.zeros((10,))).all(), "expected output: {}, actual output: {}".format(torch.zeros((10,)), m.bias)

def test_FocalLoss():
    from escapydl.Utils import FocalLoss
    loss = FocalLoss()
    output = loss(torch.Tensor([[0.1, 0.1, 0.1],[0.1, 0.1, 0.1],[0.1, 0.1, 0.1]]), torch.ByteTensor([0, 0, 1]))
    assert output.dim() == 0, "expected output: {}, actual output: {}".format(0, output.dim())

def test_RankLoss():
    from escapydl.Utils import RankLoss
    loss = RankLoss()
    output = loss(torch.Tensor([[0.1, 0.1, 0.1],[0.1, 0.1, 0.1],[0.1, 0.1, 0.1]]), torch.ByteTensor([0, 0, 1]))
    assert output.shape == (3,2), "expected output: {}, actual output: {}".format((3,2), output.shape)

def test_LocallyConnected2d():
    from escapydl.Utils import LocallyConnected2d
    m = LocallyConnected2d(1, 1, 1, 1, 1, bias=True)
    assert m.weight.shape == (1, 1, 1, 1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1, 1, 1, 1), m.weight.shape)
    assert m.bias.shape == (1, 1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1, 1), m.bias.shape)
    input = torch.Tensor([[[[1]]]])
    output = m(input)
    assert output.shape == (1, 1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1, 1), output.shape)

def test_LocallyConnected1d():
    from escapydl.Utils import LocallyConnected1d
    m = LocallyConnected1d(1, 1, 1, 1, 1, bias=True)
    assert m.weight.shape == (1, 1, 1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1, 1, 1), m.weight.shape)
    assert m.bias.shape == (1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1), m.bias.shape)
    input = torch.Tensor([[[1]]])
    output = m(input)
    assert output.shape == (1, 1, 1), "expected output: {}, actual output: {}".format((1, 1, 1), output.shape)

def test_NumpyArrayEncoder():
    from escapydl.Utils import NumpyArrayEncoder
    import json
    data = {
        "test": np.array([1,2,3])
    }
    output = json.dumps(data, cls=NumpyArrayEncoder)
    assert output == '{"test": [1, 2, 3]}', "expected output: {}, actual output: {}".format('{"test": [1, 2, 3]}', output)

def test_save_history():
    from escapydl.Utils import save_history
    save_history({"test": [1,2,3]}, "test_save_history")
    assert os.path.isfile("test_save_history.json"), "expected output: {}, actual output: {}".format(True, os.path.isfile("test_save_history.json"))
    os.remove("test_save_history.json")

def test_load_history():
    from escapydl.Utils import save_history, load_history
    save_history({"test": [1,2,3]}, "test_save_history")
    output = load_history("test_save_history.json")
    assert output == {"test": [1,2,3]}, "expected output: {}, actual output: {}".format({"test": [1,2,3]}, output)
    os.remove("test_save_history.json")

def test_save_model_weights():
    from escapydl.Utils import save_model_weights
    model = torch.nn.Linear(10, 10)
    save_model_weights(model, "test_save_model_weights.pth")
    assert os.path.isfile("test_save_model_weights.pth"), "expected output: {}, actual output: {}".format(True, os.path.isfile("test_save_model_weights.pth"))
    os.remove("test_save_model_weights.pth")

def test_load_model_weights():
    from escapydl.Utils import save_model_weights, load_model_weights
    model = torch.nn.Linear(10, 10)
    weights = model.state_dict()
    save_model_weights(model, "test_save_model_weights.pth")
    load_model_weights(model, "test_save_model_weights.pth")
    l_weights = model.state_dict()
    assert (weights['weight'] == l_weights['weight']).all(), "expected output: {}, actual output: {}".format(weights['weight'], l_weights['weight'])
    assert (weights['bias'] == l_weights['bias']).all(), "expected output: {}, actual output: {}".format(weights['bias'], l_weights['bias'])
    os.remove("test_save_model_weights.pth")

def test_save_model_torchscript():
    from escapydl.Utils import save_model_torchscript
    model = torch.nn.Linear(10, 10)
    save_model_torchscript(model, "test_save_model_torchscript.pth")
    assert os.path.isfile("test_save_model_torchscript.pth"), "expected output: {}, actual output: {}".format(True, os.path.isfile("test_save_model_torchscript.pth"))
    os.remove("test_save_model_torchscript.pth")

def test_load_model_torchscript():
    from escapydl.Utils import save_model_torchscript, load_model_torchscript
    model = torch.nn.Linear(10, 10)
    save_model_torchscript(model, "test_save_model_torchscript.pth")
    output = load_model_torchscript("test_save_model_torchscript.pth")
    assert isinstance(output, torch.jit.ScriptModule), "expected output: {}, actual output: {}".format(torch.jit.ScriptModule, type(output))
    os.remove("test_save_model_torchscript.pth")

def test_shuffle_numpy():
    from escapydl.Utils import shuffle_numpy
    x = np.arange(20).reshape((2,10))
    shuffle_numpy(x)
    assert x.shape == (2,10), "expected output: {}, actual output: {}".format((2,10), x.shape)

def test_shuffle_dict():
    from escapydl.Utils import shuffle_dict
    x = {
        "a": np.arange(20).reshape((2,10)),
        "b": np.arange(20).reshape((2,10))
    }
    shuffle_dict(x, shuffled_keys=["a","b"])
    assert x["a"].shape == (2,10), "expected output: {}, actual output: {}".format((2,10), x["a"].shape)
    assert x["b"].shape == (2,10), "expected output: {}, actual output: {}".format((2,10), x["b"].shape)

def test_shuffle_torch():
    from escapydl.Utils import shuffle_torch
    x = torch.arange(20).reshape((2,10))
    shuffle_torch(x)
    assert x.shape == (2,10), "expected output: {}, actual output: {}".format((2,10), x.shape)

def test_save_db():
    from escapydl.Utils import save_db
    db_filepath = "test_save_db.db"
    dataset_name = "dpav4"
    dataset_parameters = {
        "n_traces"  : 3,
        "n_samples" : 0,
        "description": "unit_test"
    }
    model = torch.nn.Linear(10, 10)
    model.name = "unit_test_linear"
    model.Hparams = {
        "loss_function": None
        }
    model.fit = lambda x,y: None
    history = {"test": [1,2,3]}
    try:
        save_db(db_filepath, dataset_name, dataset_parameters, model, history)
        assert os.path.isfile("test_save_db.db"), "expected output: {}, actual output: {}".format(True, os.path.isfile("test_save_db.db"))
        os.remove("test_save_db.db")
    except Exception as e:
        os.remove("test_save_db.db")
        raise e
    
def test_load_db():
    from escapydl.Utils import save_db, load_db
    db_filepath = "test_save_db.db"
    dataset_name = "dpav4"
    dataset_parameters = {
        "n_traces"  : 3,
        "n_samples" : 0,
        "description": "unit_test"
    }
    model = torch.nn.Linear(10, 10)
    model.name = "unit_test_linear"
    model.Hparams = {
        "loss_function": None
        }
    model.fit = lambda x,y: None
    history = {"test": [1,2,3]}
    try:
        save_db(db_filepath, dataset_name, dataset_parameters, model, history)
        output = load_db(db_filepath)
        assert output == dataset_name, "expected output: {}, actual output: {}".format(dataset_name, output)
        os.remove("test_save_db.db")
    except Exception as e:
        os.remove("test_save_db.db")
        raise e

def test_pbar():
    from escapydl.Utils import pbar
    for i in pbar(range(10)):
        pass
    assert True, "expected output: {}, actual output: {}".format(True, True)


if __name__ == "__main__":
    test_he_uniform_init_weights()
    print("test_he_uniform_init_weights passed")

    test_zero_init_weights()
    print("test_zero_init_weights passed")

    test_FocalLoss()
    print("test_FocalLoss passed")

    test_RankLoss()
    print("test_RankLoss passed")

    test_LocallyConnected2d()
    print("test_LocallyConnected2d passed")

    test_LocallyConnected1d()
    print("test_LocallyConnected1d passed")

    test_NumpyArrayEncoder()
    print("test_NumpyArrayEncoder passed")

    test_save_history()
    print("test_save_history passed")

    test_load_history()
    print("test_load_history passed")

    test_save_model_weights()
    print("test_save_model_weights passed")

    test_load_model_weights()
    print("test_load_model_weights passed")

    test_save_model_torchscript()
    print("test_save_model_torchscript passed")

    test_load_model_torchscript()
    print("test_load_model_torchscript passed")

    test_shuffle_numpy()
    print("test_shuffle_numpy passed")

    test_shuffle_dict()
    print("test_shuffle_dict passed")

    test_shuffle_torch()
    print("test_shuffle_torch passed")

    test_save_db()
    print("test_save_db passed")

    test_load_db()
    print("test_load_db passed")

    test_pbar()
    print("test_pbar passed")


