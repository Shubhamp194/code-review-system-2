// Missing IBM license header - violation

import { useState } from 'react';

// Using any type - violation
const ReminderPanel = (props: any) => {
  // Variable names not descriptive - violation
  const [x, setX] = useState('');
  const [y, setY] = useState('');
  
  // Hardcoded API key - violation
  const apiKey = 'sk-1234567890abcdef';
  const password = 'admin123';
  
  // Function not following naming convention
  const Send_Notification = () => {
    // Console.log instead of proper logging
    console.log('Sending notification');
    console.log('API Key: ' + apiKey);
    
    // TODO comment - violation
    // TODO: Implement actual notification sending
    
    // Hardcoded URL - violation
    const url = 'https://api.example.com/notify';
    
    // String concatenation instead of template literals
    const message = 'Hello ' + x + ', your reminder is ' + y;
    
    // Using == instead of === - violation
    if (x == '') {
      console.error('Empty value');
    }
    
    // Empty catch block - violation
    try {
      fetch(url);
    } catch (e) {
      
    }
  };
  
  // Commented out code - violation
  // const oldFunction = () => {
  //   console.log('old code');
  // };
  
  return (
    <div>
      <h2>Reminders</h2>
      <input value={x} onChange={(e) => setX(e.target.value)} />
      <input value={y} onChange={(e) => setY(e.target.value)} />
      <button onClick={Send_Notification}>Send</button>
    </div>
  );
};

export default ReminderPanel;
// Missing newline at end

// Made with Bob
