import React, { useState } from "react";

const ChatBox = ({ setHighlightQuery }) => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const sendQuery = async () => {
    if (!query.trim()) return;

    const userMsg = { role: "user", text: query };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      // ✅ FIX: define data BEFORE using it
      const data = await res.json();

      // ✅ show bot response
      const botMsg = { role: "bot", text: data.answer };
      setMessages((prev) => [...prev, botMsg]);

      // ✅ update graph highlight AFTER response
      if (data.related_ids && data.related_ids.length > 0) {
        setHighlightQuery(data.related_ids.join(" "));
      } else {
        setHighlightQuery("");
      }

    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Server error. Please try again." },
      ]);
    }

    setQuery("");
  };

  const clearChat = () => {
    setMessages([]);
    setHighlightQuery("");
  };

  return (
    <div
      style={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        background: "#020617",
        color: "#fff",
      }}
    >
      {/* HEADER */}
      <div
        style={{
          padding: "10px",
          borderBottom: "1px solid #1e293b",
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <h3>Chat</h3>
        <button
          onClick={clearChat}
          style={{
            background: "#ef4444",
            border: "none",
            padding: "6px 10px",
            borderRadius: "6px",
            cursor: "pointer",
            color: "#fff",
          }}
        >
          Clear
        </button>
      </div>

      {/* MESSAGES */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "10px",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent:
                msg.role === "user" ? "flex-end" : "flex-start",
              marginBottom: "10px",
            }}
          >
            <div
              style={{
                background:
                  msg.role === "user" ? "#2563eb" : "#1e293b",
                padding: "10px 14px",
                borderRadius: "12px",
                maxWidth: "75%",
                fontSize: "14px",
                lineHeight: "1.4",
              }}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* INPUT */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          padding: "10px",
          borderTop: "1px solid #1e293b",
        }}
      >
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendQuery()}
          placeholder="Ask about orders, billing, delivery..."
          style={{
            flex: 1,
            padding: "10px",
            borderRadius: "8px",
            border: "none",
            background: "#1e293b",
            color: "#fff",
          }}
        />

        <button
          onClick={sendQuery}
          style={{
            padding: "10px 16px",
            background: "#22c55e",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            color: "#000",
            fontWeight: "bold",
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;