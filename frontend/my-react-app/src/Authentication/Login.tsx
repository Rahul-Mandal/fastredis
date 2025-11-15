// import React, {useState, useEffect} from 'react'
// import axios from 'axios';

// function Login (){

//     const [user, updateUser] = useState({username:"",password:""})

//     const handleUpdate = (field, value) => {
//     updateUser((prev) => ({
//       ...prev,
//       [field]: value,
//     }));
//   };

  
//     const postdata  = async() => {
//       try{
//         const response = await axios.post('http://127.0.0.1:8000/token', user)
//       if (response){
//         console.log('Login successful:', response.data);
//         // updateUser((prev) =>({...prev, response.data}))
//       }
//       }
//       catch(err){
//         console.log(err)
//       }
//     }
    


// return(
//     <div>
//       <div>
//       <label htmlFor="username">Name:</label>
//         <input type='text' value={user.username} placeholder='username'
//         onChange={(e)=> handleUpdate("username",e.target.value)} />
//         </div>
//         <div>
//         <label htmlFor="username">Password:</label>
//         <input type='password' value={user.password} placeholder='password'
//         onChange ={(e) =>handleUpdate("password",e.target.value)} />
//         </div>

//         <button type='button' onClick={postdata}>Login</button>'
//     </div>
// )
// }
// export default Login;


import React, { useState } from 'react';
import axios from 'axios';

function Login() {
  const [user, updateUser] = useState({ username: "", password: "" });
  const [accessToken, setAccessToken] = useState<string | null>(null);

  const handleUpdate = (field: string, value: string) => {
    updateUser((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const postdata = async () => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/token',
        user,
        { withCredentials: true } // ensures HttpOnly refresh cookie is sent/received
      );

      if (response && response.data) {
        console.log('Login successful:', response.data);

        // Store access token in memory
        setAccessToken(response.data.access_token);

        // Refresh token is set by backend as HttpOnly cookie, cannot access via JS
        console.log('Refresh token should be in HttpOnly cookie.');
      }
    } catch (err) {
      console.log('Login failed:', err);
    }
  };

  return (
    <div>
      <div>
        <label htmlFor="username">Name:</label>
        <input
          type='text'
          value={user.username}
          placeholder='username'
          onChange={(e) => handleUpdate("username", e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="password">Password:</label>
        <input
          type='password'
          value={user.password}
          placeholder='password'
          onChange={(e) => handleUpdate("password", e.target.value)}
        />
      </div>

      <button type='button' onClick={postdata}>Login</button>
    </div>
  );
}

export default Login;
