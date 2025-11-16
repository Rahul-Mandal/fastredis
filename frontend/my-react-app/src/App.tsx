import './App.css'
import Login from './Authentication/Login'
import Dashboard from './Dashboard/Dashboard'
import { useAuthStore } from './Store/useAuthStore'

function App() {
  const token = useAuthStore((s) => s.accessToken);

  return (
    <div>
      {token ? <Dashboard /> : <Login />}
    </div>
  )
}

export default App

