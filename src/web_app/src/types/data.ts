// eslint-disable-next-line @typescript-eslint/no-namespace
export namespace Types {
    export type AG_hyper_parameters = {
      nb_epochs: number
      pop_size: number
      crossover_rate: number
      mutation_rate: number
    }

    export type DRL_hyper_parameters = {
      nb_epochs: number
      learning_rate : number
      batch_size: number
      momentum : number
    }
}