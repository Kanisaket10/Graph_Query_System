import { useState } from "react";
import GraphView from "./components/GraphView";
import ChatBox from "./components/ChatBox";

function App() {
  const [highlightQuery, setHighlightQuery] = useState("");

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        background: "#020617",
        color: "#fff",
      }}
    >
      {/* LEFT: GRAPH */}
      <div style={{ flex: 2, padding: "20px" }}>
        <h2 style={{ marginBottom: "10px" }}>Graph View</h2>
        <GraphView highlightQuery={highlightQuery} />
      </div>

      {/* RIGHT: CHAT */}
      <div
        style={{
          flex: 1,
          borderLeft: "1px solid #1e293b",
          padding: "10px",
        }}
      >
        <ChatBox setHighlightQuery={setHighlightQuery} />
      </div>
    </div>
  );
}

export default App;