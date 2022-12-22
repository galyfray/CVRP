export type Node = {
  "id": number,
  "group": string
  "coord": Array<number>
};

export type Link = {
      source: number,
      target: number,
    };

export type d3Graph = {
      nodes: Node[],
      links: Link[]
    };
