/* eslint-disable @typescript-eslint/no-namespace */
export namespace Types {
  export type Hyper_parameters = {
    type: string,
    params:{
        nb_epochs: number,
        pop_size?:number,
        mutation_rate?: number,
        seed?: number,
        learning_rate?: number,
        batch_size?: number,
        momentum?: number
    },
    override: boolean,
    bench_id: string,
    snapshot_rate: number
  }

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

  export type Point = {
    id: number
    NODE_COORD_X : number
    NODE_COORD_Y : number
    is_station : boolean
  }

  export type Link = {
    source : number,
    target : number
  }

  export type Received_data = {
    "time" : number,
    "fitness" : number
  }

  export type Log = {
    "id" : string,
    "method" : string,
    "logs": Array<Received_data>
  }
}