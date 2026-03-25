import React, { useState } from "react";
import { Handle, Position } from "reactflow";

const CustomNode = ({ data }) => {
  const [hover, setHover] = useState(false);

  const getColor = (type) => {
    switch (type) {
      case "customer":
        return "#3b82f6";
      case "order":
        return "#22c55e";
      case "delivery":
        return "#f59e0b";
      case "billing":
        return "#a855f7";
      case "payment":
        return "#ef4444";
      default:
        return "#6b7280";
    }
  };

  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        padding: "10px",
        borderRadius: "12px",
        background: getColor(data.type),
        color: "#fff",
        minWidth: "140px",
        textAlign: "center",
        position: "relative",
        cursor: "pointer",
      }}
    >
      {/* 🔥 LEFT HANDLE (incoming edge) */}
      <Handle
        type="target"
        position={Position.Left}
        style={{ background: "#fff" }}
      />

      {/* NODE CONTENT */}
      <div style={{ fontWeight: "600" }}>{data.label}</div>
      <div style={{ fontSize: "10px", opacity: 0.8 }}>
        {data.type}
      </div>

      {/* 🔥 RIGHT HANDLE (outgoing edge) */}
      <Handle
        type="source"
        position={Position.Right}
        style={{ background: "#fff" }}
      />

      {/* TOOLTIP */}
      {hover && (
        <div
          style={{
            position: "absolute",
            top: "-60px",
            left: "50%",
            transform: "translateX(-50%)",
            background: "#111",
            padding: "8px",
            borderRadius: "8px",
            fontSize: "10px",
            whiteSpace: "nowrap",
            zIndex: 1000,
          }}
        >
          {data.label} ({data.type})
        </div>
      )}
    </div>
  );
};

export default CustomNode;