export type Node = {
  "id": string,
  "data" : {
    "node": number,
    "x": number,
    "y": number
  }[]
};

export type Link = {
      source: number,
      target: number,
    };

export type d3Graph = {
      nodes: Node[],
      links: Link[]
    };
