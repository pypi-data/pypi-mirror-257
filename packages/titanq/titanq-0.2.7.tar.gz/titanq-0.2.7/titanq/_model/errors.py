class TitanQError(Exception):
    """Base TitanQ error"""

class MaximumVariableLimitError(TitanQError):
    """Variable already defined in the model"""

class MissingVariableError(TitanQError):
    """Variable has not already been registered"""

class MissingObjectiveError(TitanQError):
    """Objective has not already been registered"""

class ObjectiveAlreadySetError(TitanQError):
    """An objective has already been set"""

class OptimizeError(TitanQError):
    """Error occur during optmization"""

class ServerError(TitanQError):
    """Error returned by the server"""