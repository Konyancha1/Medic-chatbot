export async function sendMessage(message) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/chatbot', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error(error);
    return 'Sorry, there was an error with the chatbot.';
  }
}
