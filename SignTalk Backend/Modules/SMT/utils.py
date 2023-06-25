import dill

def load_model(filename):
    with open(filename, 'rb') as f:
        model = dill.load(f)
    return model