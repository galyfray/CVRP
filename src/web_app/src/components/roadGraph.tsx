import {Component} from "react";
import {GraphView} from "react-digraph";
import * as d3Types from "../types/d3Types";

const GraphConfig = {
    NodeTypes: {
        empty: { // Required to show empty nodes
            typeText: "None",
            shapeId : "#empty",
            shape:
          <symbol viewBox="0 0 100 100" id="empty" key="0">
              <circle cx="50" cy="50" r="45"></circle>
          </symbol>

        },
        custom: { // Required to show empty nodes
            typeText: "Custom",
            shapeId : "#custom", // Relates to the type property of a node
            shape:
          <symbol viewBox="0 0 50 25" id="custom" key="0">
              <ellipse cx="50" cy="25" rx="50" ry="25"></ellipse>
          </symbol>

        }
    },
    NodeSubtypes: {},
    EdgeTypes   : {
        emptyEdge: { // Required to show empty edges
            shapeId: "#emptyEdge",
            shape:
          <symbol viewBox="0 0 50 50" id="emptyEdge" key="0">
              <circle cx="25" cy="25" r="8" fill="currentColor"> </circle>
          </symbol>

        }
    }
};

const NODE_KEY = "id"; // Allows D3 to correctly update DOM

  interface Props {
    width: number;
    height: number;
    graph: d3Types.d3Graph;
  }

  interface State {
    graph: d3Types.d3Graph
  }

class RoadGraph extends Component<Props, State> {


    constructor(props: Props) {
        super(props);
        this.state = {graph: this.props.graph};
    }


    render() {
        const nodes = this.state.graph.nodes;
        const edges = this.state.graph.links;

        const NodeTypes = GraphConfig.NodeTypes;
        const NodeSubtypes = GraphConfig.NodeSubtypes;
        const EdgeTypes = GraphConfig.EdgeTypes;

        return (
            <div id="graph">
                <GraphView ref="GraphView"
                    nodeKey={NODE_KEY}
                    nodes={nodes}
                    edges={edges}
                    nodeTypes={NodeTypes}
                    nodeSubtypes={NodeSubtypes}
                    edgeTypes={EdgeTypes}
                    allowMultiselect={false} // True by default, set to false to disable multi select.
                />
            </div>
        );
    }

}

export default RoadGraph;