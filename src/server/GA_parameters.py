class GA_parameters:
    def __init__(self, 
        nb_epochs: int,
        pop_size: int,
        crossover_rate: float,
        mutation_rate: float) :
        self.__nbEpochs = nb_epochs
        self.__popSize = pop_size
        self.__crossoverRate = crossover_rate
        self.__mutationRate = mutation_rate

    def get_parameters(self):
        return {
            "nbEpochs" : self.__nbEpochs,
            "popSize" : self.__popSize,
            "crossoverRate" : self.__crossoverRate,
            "mutationRate" : self.__mutationRate
        }
    
    def set_parameters(self, params):
        self.__nbEpochs = params["nb_epochs"]
        self.__popSize = params["pop_size"]
        self.__crossoverRate = params["crossover_rate"]
        self.__mutationRate = params["mutation_rate"]

