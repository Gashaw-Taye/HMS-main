import { useState,useEffect } from 'react'

import axios from 'axios'
import './App.css'

function App() {
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
  
      <h1>sample pateint records</h1>
      <div className="card">
     
        <table style={{ border:1}}>
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
     
    </>
  )
}

export default App
