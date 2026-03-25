import React, { useEffect, useState, useMemo } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

import {
  forceSimulation,
  forceManyBody,
  forceLink,
  forceCenter,
} from "d3-force";

import CustomNode from "./CustomNode";

const nodeTypes = { custom: CustomNode };

const GraphView = ({ highlightQuery }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  // -----------------------------
  // FETCH GRAPH
  // -----------------------------
  useEffect(() => {
    fetch("http://127.0.0.1:8000/graph")
      .then((res) => res.json())
      .then((data) => {
        const simNodes = data.nodes.map((n) => ({
          id: String(n.id),
          label: String(n.label),
          type: n.type,
        }));

        const simLinks = data.edges.map((e) => ({
          source: String(e.source),
          target: String(e.target),
        }));

        const simulation = forceSimulation(simNodes)
          .force("charge", forceManyBody().strength(-350))
          .force(
            "link",
            forceLink(simLinks)
              .id((d) => d.id)
              .distance(90)
          )
          .force("center", forceCenter(600, 400))
          .stop();

        for (let i = 0; i < 400; i++) simulation.tick();

        const formattedNodes = simNodes.map((node) => ({
          id: node.id,
          type: "custom",
          position: { x: node.x, y: node.y },
          data: {
            label: node.label,
            type: node.type,
          },
        }));

        const formattedEdges = data.edges.map((edge, i) => ({
          id: `${edge.source}-${edge.target}-${i}`,
          source: String(edge.source),
          target: String(edge.target),
          type: "smoothstep",
          style: { stroke: "#475569", strokeWidth: 1 },
          markerEnd: { type: MarkerType.ArrowClosed },
        }));

        setNodes(formattedNodes);
        setEdges(formattedEdges);
      });
  }, []);

  // -----------------------------
  // 🔥 FIXED HIGHLIGHT LOGIC
  // -----------------------------
  const graph = useMemo(() => {
    if (!highlightQuery || highlightQuery.trim() === "") {
      return { nodes, edges };
    }

    const ids = highlightQuery.split(" ").map((x) => x.trim());
    const idSet = new Set(ids);

    const matchedNodes = new Set();

    nodes.forEach((n) => {
      const label = String(n.data?.label || "").toLowerCase();

      if (
        idSet.has(n.id) ||                 // exact ID match
        ids.includes(label) ||             // label match
        label.includes(ids[0])             // partial match
      ) {
        matchedNodes.add(n.id);
      }
    });

    // ❗ IMPORTANT: if nothing matched → DO NOT dim graph
    if (matchedNodes.size === 0) {
      return { nodes, edges };
    }

    const updatedNodes = nodes.map((n) => {
      const active = matchedNodes.has(n.id);

      return {
        ...n,
        style: {
          opacity: active ? 1 : 0.1,
          border: active ? "2px solid #22c55e" : "none",
        },
      };
    });

    const updatedEdges = edges.map((e) => {
      const active =
        matchedNodes.has(e.source) ||
        matchedNodes.has(e.target);

      return {
        ...e,
        animated: active,
        style: {
          stroke: active ? "#22c55e" : "#334155",
          strokeWidth: active ? 2 : 1,
        },
      };
    });

    return { nodes: updatedNodes, edges: updatedEdges };
  }, [nodes, edges, highlightQuery]);

  // -----------------------------
  // UI
  // -----------------------------
  return (
    <div style={{ height: "90vh", background: "#020617", position: "relative" }}>
      <ReactFlow
        nodes={graph.nodes}
        edges={graph.edges}
        nodeTypes={nodeTypes}
        fitView
        onNodeClick={(_, node) => setSelectedNode(node)}
        minZoom={0.1}
        maxZoom={3}
        zoomOnScroll
        zoomOnPinch
        zoomOnDoubleClick
        panOnScroll
        panOnDrag
        defaultViewport={{ x: 0, y: 0, zoom: 0.6 }}
      >
        <MiniMap
          nodeColor={(n) => {
            switch (n.data.type) {
              case "order":
                return "#22c55e";
              case "delivery":
                return "#f59e0b";
              case "billing":
                return "#a855f7";
              case "payment":
                return "#ef4444";
              default:
                return "#64748b";
            }
          }}
        />
        <Background color="#1e293b" gap={20} />
        <Controls />
      </ReactFlow>

      {/* Node details */}
      {selectedNode && (
        <div
          style={{
            position: "absolute",
            right: 20,
            top: 20,
            background: "#111",
            color: "#fff",
            padding: "15px",
            borderRadius: "10px",
            width: "220px",
            border: "1px solid #334155",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <h4 style={{ margin: 0 }}>Node Details</h4>
            <button
              onClick={() => setSelectedNode(null)}
              style={{ background: "none", border: "none", color: "#aaa" }}
            >
              ✕
            </button>
          </div>

          <hr style={{ borderColor: "#334155" }} />

          <p><b>ID:</b> {selectedNode.id}</p>
          <p><b>Type:</b> {selectedNode.data.type}</p>
        </div>
      )}
    </div>
  );
};

export default GraphView;