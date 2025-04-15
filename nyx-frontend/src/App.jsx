import { useState } from 'react';
import Login from './login';

function App() {
  const [user, setUser] = useState(null); // { username, token }
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState(""); //track input field state

  const sendMessage = async(message) => {
    if(!message.trim()) return; //prevent sending empty messages

    const userMessage = { text: message };
    setMessages([...messages, { text: message, sender: "user" }]);
  
    try {
      const response = await fetch("https://nyx-backend-52886619499.europe-west2.run.app/chat", {  
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userMessage),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data.expressed_response, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "⚠️ Error: Could not reach backend.", sender: "bot" },
      ]);
    }
  
    setInput(""); // Clear input field
  };

  if(!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial", backgroundColor: "#111", color: "#0f0" }}>
      <h1>Cyberpunk Chatbot</h1>
      <div style={{ border: "1px solid #0f0", padding: "10px", minHeight: "300px" }}>
        {messages.map((msg, index) => (
          <p key={index} style={{ color: msg.sender === "user" ? "#0ff" : "#f0f" }}>
            {msg.text}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={input} //bind input field to input state
        onChange={(e) => setInput(e.target.value)} //update input state when typing
        onKeyDown={(e) => e.key === "Enter" && sendMessage(input)} //send message on Enter key press
        placeholder="Type a message..."
        style={{ width: "100%", padding: "10px", marginTop: "10px" }}
      />
    </div>
  );
}

export default App;
