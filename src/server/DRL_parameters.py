class DRL_parameters:
    def __init__(self,
        nb_epochs: int,
        learning_rate: float,
        batch_size: int,
        momentum: float) :
        self.__nbEpochs = nb_epochs
        self.__learningRate = learning_rate
        self.__batchSize = batch_size
        self.__momentum = momentum

    def get_parameters(self):
        return {
            "nbEpochs" : self.__nbEpochs,
            "learningRate" : self.__learningRate,
            "batchSize" : self.__batchSize,
            "momentum" : self.__momentum
        }
    
    def set_parameters(self, params):
        self.__nbEpochs = params["nb_epochs"]
        self.__learningRate = params["learning_rate"]
        self.__batchSize = params["batch_size"]
        self.__momentum = params["momentum"]

