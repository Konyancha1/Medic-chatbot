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
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index} className={message.isBot ? 'bot-message' : 'user-message'}>
            <p>{message.text}</p>
          </div>
        ))}
      </div>
      <input type='text' value={input} onChange={handleInput} onKeyDown={handleKeyDown} />
    </div>
  );
}

export default Chatbot;
