import { Box } from '@mui/material';
// import React from 'react';
import PostP from '../components/PostP';

const PagesPage = () => {
  return (
    <Box  flex={4} padding={2} bgcolor="skyblue">
      <h2>Report Page</h2>
      <p>Welcome to Report Page!</p>
      <PostP/>
      <PostP/>
      <PostP/>
      <PostP/>
    </Box>
  );
}

export default PagesPage;