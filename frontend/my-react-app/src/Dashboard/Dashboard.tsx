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
import { useEffect, useState } from "react";
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

export default function Dashboard() {
  const token = useAuthStore((s) => s.accessToken);
  const [users, setUsers] = useState<User[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchUsers = async () => {
      try {
        const res = await axios.get("/users/list");
        console.log("API response:", res.data);

        // Backend returns array → safe
        if (Array.isArray(res.data)) {
          setUsers(res.data);
        } else {
          console.warn("Unexpected API response:", res.data);
          setUsers([]);
        }
      } catch (err) {
        console.error("Failed to fetch users:", err);
        setUsers([]);
      }
    };

    fetchUsers();
  }, [token, navigate]);

  return (
    <div>
      <h1>Dashboard</h1>
      <h2>User List</h2>
      {Array.isArray(users) && users.length > 0 ? (
        users.map((u) => (
          <div key={u.id}>
            {u.email} — {u.name} — Roll: {u.roll_no} — Active: {u.is_active ? "Yes" : "No"}
          </div>
        ))
      ) : (
        <div>No users found.</div>
      )}
    </div>
  );
}
