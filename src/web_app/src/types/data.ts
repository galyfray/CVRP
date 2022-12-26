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

export type Point = {
  generation : number
  fitness : number
}

export type Link = {
  source : number,
  target : number
}

export type individual = {
  "fitness" : number,
  "solution" : [],
}

export type Log = {
  "bench_id" : string,
  "log_id": string,
  "method" : string,
  "snapshots": {
    "time" : number,
    "individuals": [individual]
  }
}

export type Snapshot = {
  "has_next" : boolean,
  "generation" : number,
  "snapshot": [individual]
}