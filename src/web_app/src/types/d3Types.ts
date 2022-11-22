/* eslint-disable @typescript-eslint/no-namespace */
export namespace d3Types {
    export type d3Node = {
      id: number,
      group: Array<number | boolean>
    };

    export type d3Link = {
      source: number,
      target: number,
    };

    export type d3Graph = {
      nodes: d3Node[],
      links: d3Link[]
    };
  }