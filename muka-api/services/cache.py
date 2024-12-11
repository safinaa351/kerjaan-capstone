MODEL_CACHE = None

def get_cached_model():
    global MODEL_CACHE
    if MODEL_CACHE is None:
        from services.model import load_model
        MODEL_CACHE = load_model()
    return MODEL_CACHE

def set_cached_model(model):
    global MODEL_CACHE
    MODEL_CACHE = model
