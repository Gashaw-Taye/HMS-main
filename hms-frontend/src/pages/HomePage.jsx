import { Box } from '@mui/material';
// import React from 'react';
import Post from '../components/Post';

const HomePage = () => {
  return (
    <Box  flex={4} padding={2} bgcolor="skyblue" >
      <h2>Home Page</h2>
      <p>Welcome to Home Page!</p>
      <Post/>
      <Post/>
      <Post/>
    </Box>
  );
}

export default HomePage;