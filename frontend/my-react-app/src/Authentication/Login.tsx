// import React, {useState, useEffect} from 'react'
// import axios from 'axios';

// function Login (){

//     const [user, updateUser] = useState({email:"",password:""})

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
//       <label htmlFor="email">Name:</label>
//         <input type='text' value={user.email} placeholder='email'
//         onChange={(e)=> handleUpdate("email",e.target.value)} />
//         </div>
//         <div>
//         <label htmlFor="email">Password:</label>
//         <input type='password' value={user.password} placeholder='password'
//         onChange ={(e) =>handleUpdate("password",e.target.value)} />
//         </div>

//         <button type='button' onClick={postdata}>Login</button>'
//     </div>
// )
// }
// export default Login;


import React, { useState , useEffect} from 'react';
import axios from 'axios';
import { useAuthStore } from '../Store/useAuthStore';
import { useNavigate } from "react-router-dom";


function Login() {
  const navigate = useNavigate();
  const [user, updateUser] = useState({ email: "", password: "" });
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const setAccessTokens = useAuthStore.getState().setAccessToken;


  const handleUpdate = (field: string, value: string) => {
    updateUser((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const postdata = async () => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/auth/login',
        user,
        { withCredentials: true } // ensures HttpOnly refresh cookie is sent/received
      );

      if (response && response.data) {
        console.log('Login successful:', response.data);

        // Store access token in memory
        setAccessTokens(response.data.access_token);
        // setAccessToken(res.data.access_token);

        // Read latest value
        console.log("Token set to:", useAuthStore.getState().accessToken);

        // Refresh token is set by backend as HttpOnly cookie, cannot access via JS
        console.log('Refresh token should be in HttpOnly cookie.');
      }
      navigate("/dashboard"); 
    } catch (err) {
      console.log('Login failed:', err);
    }
  };


  //  useEffect(() => {
  //   console.log("Access token changed:", accessToken);
  // }, [accessToken]);

  // return accessToken;


const accessTokens = useAuthStore((s) => s.accessToken);

// Watch the token
useEffect(() => {
  console.log("ACCESS TOKEN UPDATED:", accessTokens);
}, [accessToken]);


  return (
    <div>
      <div>
        <label htmlFor="email">Name:</label>
        <input
          type='text'
          value={user.email}
          placeholder='email'
          onChange={(e) => handleUpdate("email", e.target.value)}
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
