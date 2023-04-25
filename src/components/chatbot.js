import React, { useState } from 'react';
import { sendMessage } from '../utils/api';

function Chatbot() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleInput = (event) => {
    setInput(event.target.value);
  }

  const handleKeyDown = async (event) => {
    if (event.key === 'Enter') {
      const inputJSON = JSON.stringify({ description: input, utterances: [ `patient: ${input}` ] });
      const response = await sendMessage(inputJSON);
      setMessages(messages => [...messages, { text: input }, { text: response, isBot: true }]);
      setInput('');
    }
  }
  

  return (
    <div className="container">
      {messages.map((message, index) => (
        <div key={index} className={message.isBot ? 'bot-message message' : 'user-message message'}>
          <p>{message.text}</p>
        </div>
      ))}
      <input type='text' value={input} onChange={handleInput} onKeyDown={handleKeyDown} placeholder="Type a message"/>
    </div>
  );
}


export default Chatbot;
