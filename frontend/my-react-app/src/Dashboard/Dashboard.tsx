// // Dashboard.tsx
// import { useAuthStore } from "../Store/useAuthStore";
// import { useEffect, useState } from "react";
// import axios from 'axios';
// // axios with interceptors

// export default function Dashboard() {
//   const token = useAuthStore((s) => s.accessToken);
//   const [users, setUsers] = useState([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     if (!token) {
//       console.log("No access token → redirect to login");
//       // window.location.href = "/login";
//       return;
//     }

//     const fetchUsers = async () => {
//       try {
//         const res = await axios.get("/users/list");  // your FastAPI route
//         setUsers(res.data);
//         setLoading(false);
//       } catch (err) {
//         console.error("Failed to fetch users:", err);
//       }
//     };

//     fetchUsers();
//   }, [token]);

//   if (loading) return <div>Loading...</div>;
//   return (
//     <div>
//       <h1>Dashboard</h1>

//       <h2>User List</h2>
//       {users.map((u) => (
//         <div key={u.id}>
//           {u.email} — {u.name}
//         </div>
//       ))}
//     </div>
//   );
// }

import { useAuthStore } from "../Store/useAuthStore";
import { use, useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

interface User {
  id: number;
  name: string;
  email: string;
  roll_no: number;
  phone_number: string | null;
  is_active: boolean;
}

export default function Dashboard (){
  const navigate = useNavigate()
  const token = useAuthStore((s) => s.accessToken)
  const logout = useAuthStore((s) => s.logout)
  const [users, setUsers] = useState<User []>([])
  const [editData, setEditData] = useState<Partial<User>>({})
  const [editedid, setEditid] = useState<number | null >(null)

  useEffect(() =>{
    if (!token){
      navigate("/Dashboard")
      return
    }

    const fetchData = async() =>{
      try {
        const res = await axios.get('http://127.0.0.1:8000/users/list', {
          headers:{'Authorization': `Bearer ${token}`},
          withCredentials: true
        })
        if(Array.isArray(res.data)){
          setUsers(res.data)
        }
        else{
            console.log("Unexpected Api error", res.data)
            setUsers([])
        }
      }
      catch (err){
        console.log('failed to fetch data')
        setUsers([])
      }
    }
    fetchData()
  }, [token, navigate])

  const handleEdit = (user: User) => {
    setEditData({...user})
    setEditid(user.id)
  }

  const handleEditData = (field: keyof User, value: any) =>{
    setEditData((prev) => ({...prev, [field]: value}))
  }

  const handleCancle = () =>{
    setEditData({})
    setEditid(null)
  }

  const handleUpdate = async(id: number) => {
    try {
      const res = await axios.put(`http://127.0.0.1:8000/users/${id}`, editData,{
        headers:{'Authorization' : `Bearer ${token}`}

      })
      console.log("User updated:", res.data);
      if (res){
        setUsers(users.map((u) => (u.id === id? res.data : u)))
        // setUsers(users.map((u) => (u.id === id ? res.data : u)));
      }
    }
    catch(err){
      console.log(err)
    }
  }

  const handleDelete = async(id:Number) =>{
    try{
      const res = await axios.delete(`http://127.0.0.1:8000/users/del/${id}`,{
        headers: {"Authorization" : `Bearer ${token}`}
      })
      if (res) {
        setUsers(users.filter((d) => (d.id !== id )))
        // setUsers((prev) => prev.filter((u) => u.id !== id));
      }
    }
    catch(err){
      console.log(err)
    }
  }

  return(

   
    <div>
      <button onClick={() => navigate("/create-user")}>Add New User</button>
<div className="p-4 bg-blue-500 text-white rounded">
  Hello Tailwind 🚀
</div>

      {users.map((user) =>(
        <div key={user.id} style={{margin: "10px"}}>
           
           {editedid == user.id ? (
        <>
        <input type="test" value={editData.name || ""}
        onChange={(e)=>handleEditData('name', e.target.value)}/>
        <input type="test" value={editData.email || ""}
        onChange={(e)=>handleEditData('email', e.target.value)}/>
        <input type="test" value={editData.roll_no || ""}
        onChange={(e)=>handleEditData('roll_no', Number(e.target.value))}/>
        <button onClick={()=> handleUpdate(user.id)}>Save</button>
        <button onClick={handleCancle}>Cancle</button>
        </>
           ):(
            <>
          <div>{user.name}</div>
          <div>{user.email}</div>
          <div>{user.roll_no}</div>
          <button onClick={()=>handleEdit(user)}>Edit</button>
          <button onClick={()=>handleDelete(user.id)}>Delete</button>
           </>
           )
           
           }
          
           </div>
      ))}
    </div>
   
  )
}
// export default function Dashboard() {
//   const token = useAuthStore((s) => s.accessToken);
//   const logout = useAuthStore((s) => s.logout);
//   const [users, setUsers] = useState<User[]>([]);
//   const [editingId, setEditingId] = useState<number | null>(null);
//   const [editData, setEditData] = useState<Partial<User>>({});
//   const navigate = useNavigate();

//   useEffect(() => {
//     if (!token) {
//       navigate("/login");
//       return;
//     }

//     const fetchUsers = async () => {
//       try {
//         const res =await axios.get("http://127.0.0.1:8000/users/list", {
//   headers: {
//     Authorization: `Bearer ${token}`,
//   },
//   withCredentials: true
// });
//         console.log("API response:", res.data);

//         // Backend returns array → safe
//         if (Array.isArray(res.data)) {
//           setUsers(res.data);

//         } else {
//           console.warn("Unexpected API response:", res.data);
//           setUsers([]);
//         }
//       } catch (err) {
//         console.error("Failed to fetch users:", err);
//         setUsers([]);
//       }
//     };

//     fetchUsers();
//   }, [token, navigate]);

//   const startEdit = (user: User) => {
//     setEditingId(user.id);
//     setEditData({ ...user });
//   };

//   const cancelEdit = () => {
//     setEditingId(null);
//     setEditData({});
//   };
//   const handleChange = (field: keyof User, value: any) => {
//     setEditData((prev) => ({ ...prev, [field]: value }));
//   };

//   const saveEdit = async (id: number) => {
//     try {
//       const res = await axios.put(
//         `http://127.0.0.1:8000/users/${id}`,
//         editData,
//         { headers: { Authorization: `Bearer ${token}` } }
//       );
//       console.log("User updated:", res.data);

//       // Update local state
//       setUsers(users.map((u) => (u.id === id ? res.data : u)));
//       cancelEdit();
//     } catch (err) {
//       console.error("Update failed:", err);
//     }
//   };

//   return (
//     <div>
//       <h1>Dashboard</h1>
//       <h2>User List</h2>
//       {users.map((user) => (
//         <div key={user.id} style={{ marginBottom: "10px", border: "1px solid #ccc", padding: "10px" }}>
//           {editingId === user.id ? (
//             <>
//               <input
//                 type="text"
//                 value={editData.name || ""}
//                 onChange={(e) => handleChange("name", e.target.value)}
//               />
//               <input
//                 type="email"
//                 value={editData.email || ""}
//                 onChange={(e) => handleChange("email", e.target.value)}
//               />
//               <input
//                 type="number"
//                 value={editData.roll_no || ""}
//                 onChange={(e) => handleChange("roll_no", Number(e.target.value))}
//               />
//               <button onClick={() => saveEdit(user.id)}>Save</button>
//               <button onClick={cancelEdit}>Cancel</button>
//             </>
//           ) : (
//             <>
//               <div>Name: {user.name}</div>
//               <div>Email: {user.email}</div>
//               <div>Roll No: {user.roll_no}</div>
//               <button onClick={() => startEdit(user)}>Edit</button>
//             </>
//           )}
//         </div>
//       ))}

//       <button onClick={logout}>Logout</button>
//     </div>
//   );
// }

//   return (
//     <div>
//       <h1>Dashboard</h1>
//       <h2>User List</h2>
//       {Array.isArray(users) && users.length > 0 ? (
//         users.map((u) => (
//           <div key={u.id}>
//             {u.email} — {u.name} — Roll: {u.roll_no} — Active: {u.is_active ? "Yes" : "No"}
//           </div>
//         ))
        
//       ) : (
//         <div>No users found.</div>
//       )}
//       <button onClick={() => navigate("/create-user")}>Add New User</button>
//     </div>
//   );
// }
