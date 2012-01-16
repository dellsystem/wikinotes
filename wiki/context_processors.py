from settings import COMPILE_LESS

def less_compilation(request):
    return {'compile_less': COMPILE_LESS}
