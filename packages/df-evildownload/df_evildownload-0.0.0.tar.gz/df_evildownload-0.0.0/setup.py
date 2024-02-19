class EvilException(Exception):
    pass

raise EvilException("Running the setup.py! <nothing evil actually happens>")
