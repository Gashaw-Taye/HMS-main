import { useState,useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import axios from 'axios'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [array,setArray]=useState([]);

  const fetchAPI=async()=>{
    const response=await axios.get("http://localhost:9000/persons")
    console.log(response.data.persons);
    setArray(response.data.persons);
  };
  useEffect(()=>{
    fetchAPI();

  },[]);
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <table>
      <thead>
        <tr>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Gender</th>
          <th>Person Type</th>
        </tr>
      </thead>
      <tbody>
        {
          array.map((person, index) => (
            <tr key={index}>
              <td>{person.first_name}</td>
              <td>{person.last_name}</td>
              <td>{person.gender}</td>
              <td>{person.person_type}</td>
            </tr>
          ))
        }
      </tbody>
    </table>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
