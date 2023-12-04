import React, { useState } from 'react';
import axios from 'axios';

type ChatGPTProps = {
    user_city: string;
  };

const ChatGPT: React.FC<ChatGPTProps> = ({ user_city }) => {
    console.log("User city in Chat frontend: ", user_city)
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:5328/api/chatgpt', { 
                prompt: input,
                user_city: user_city
            });
            console.log(response.data)
            setResponse(response.data.text);
        } 
        catch (error) {
            console.error(error);
            setResponse('An error occurred while processing your request.');
        }
    };

    return (
        <div className="flex flex-col items-start">
            <form onSubmit={handleSubmit} className="mb-2">
                <button 
                    type="submit" 
                    className="font-bold text-xl">
                    Generate
                </button>
            </form>
            <div>
                <p>{response}</p>
            </div>
        </div>
    );
};

export default ChatGPT;