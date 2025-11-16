import React, {useState, useEffect} from "react";
import axios from 'axios'
import { useNavigate } from "react-router-dom";

interface UserForm {
    name: String;
    roll_no?: number;
    email: string;
  password: string;
  is_active: boolean;
  phone_number?: string; 
}

export default function CreateUser (){
    const navigate = useNavigate();
const [newUser, setNewUSer] = useState<UserForm>({

    name: "",
    roll_no: undefined,
    email: "",
    password: "",
  is_active: true,
  phone_number: "",

})
const [msg, setMsg] = useState("");

const handleChange = (field, value) =>{

    setNewUSer((prev) => ({...prev, [field]: value}))
}

const handleSubmit = (e) =>{
    e.preventDefault()

    try{
        const response = axios.post("http://127.0.0.1:8000/users/create", newUser);

        console.log("User created:", response.data);
      setMsg("User created successfully!");
      setNewUSer({
        name: "",
        roll_no: undefined,
        email: "",
        password: "",
        is_active: true,
        phone_number: "",
      });
      navigate('/dashboard')
    }
     catch (err: any) {
      console.error("Failed to create user:", err.response?.data || err);
      setMsg("Error creating user. See console for details.");
    }
}

return (

    <>
    <form onSubmit={handleSubmit}>
    <div>
        <label>NAme*</label>
        <input type="text" value={newUser.name} placeholder="name"  required onChange={(e)=>handleChange("name", e.target.value)} />

          </div>
          <div>
            <label>Number*</label>
        <input type="number" value={newUser.roll_no || ""}  placeholder="rollnumber"  required onChange={(e)=>handleChange("roll_no", e.target.value)} />

        </div>
        <div>
            <label>Email*</label>
        <input type="email" value={newUser.email} placeholder="email"  required onChange={(e)=>handleChange("email", e.target.value)} />
        </div>
        <div>
            <label>Password*</label>
        <input type="password" value={newUser.password} placeholder="password"  required onChange={(e)=>handleChange("password", e.target.value)} />
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={newUser.is_active}
              onChange={(e) => handleChange("is_active", e.target.checked)}
            />
            Active
          </label>
        </div>
        <div>
            <label>Phone</label>
        <input type="text" value={newUser.phone_number} placeholder="phone_no."  required onChange={(e)=>handleChange("phone_number", e.target.value)} />
        
        </div>
        <button type="submit">Create User</button>
        </form>
        </>
)

}