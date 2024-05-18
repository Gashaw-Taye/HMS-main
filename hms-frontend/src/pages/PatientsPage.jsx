import { Box } from '@mui/material';
// import React from 'react';
import { useState,useEffect } from 'react'
import axios from 'axios'
import PostPt from '../components/PostPt';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
const PatientsPage = () => {
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
    <Box  flex={4} padding={2} bgcolor="skyblue" >
      <h2>Patients Page</h2>
      <p>Welcome to  Patients Page!</p>
      <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
          <TableCell align="left">ID</TableCell>
            <TableCell align="left">First Name</TableCell>
            <TableCell align="left">Middle  Name</TableCell>
            <TableCell align="left">Last Name</TableCell>            
            <TableCell align="left">Gender</TableCell>
            <TableCell align="left">person_type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {array.map((person) => (
            <TableRow  key={person.id}  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell align="left">{person.id}</TableCell>
              <TableCell align="left">{person.first_name}</TableCell>
              <TableCell align="left">{person.last_name}</TableCell>
              <TableCell align="left">{person.grand_father}</TableCell>
              <TableCell align="left">{person.gender}</TableCell>
              <TableCell component="th" scope="row">{person.person_type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
      <PostPt/>
      <PostPt/>
      <PostPt/>
    </Box>
  );
}

export default PatientsPage;