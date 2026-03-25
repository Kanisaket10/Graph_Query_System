import dagre from "dagre";

export const getLayoutedElements = (nodes, edges) => {
  const g = new dagre.graphlib.Graph();

  g.setDefaultEdgeLabel(() => ({}));

  g.setGraph({
    rankdir: "LR",
    nodesep: 120,
    ranksep: 180,
  });

  nodes.forEach((node) => {
    g.setNode(node.id, { width: 180, height: 60 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes = nodes.map((node) => {
    const nodeWithPosition = g.node(node.id);

    return {
      ...node,
      position: {
        x: nodeWithPosition.x,
        y: nodeWithPosition.y,
      },
      sourcePosition: "right",
      targetPosition: "left",
    };
  });

  return { nodes: layoutedNodes, edges };
};