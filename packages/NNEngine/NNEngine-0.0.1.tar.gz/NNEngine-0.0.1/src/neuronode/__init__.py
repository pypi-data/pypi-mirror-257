try:
    get_ipython().config
except NameError:
    raise RuntimeError("Incompatible environment: Notebook environment required for running this code.")

