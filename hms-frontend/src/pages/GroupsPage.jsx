import { Box } from '@mui/material';
// import React from 'react';
import PostP from '../components/PostP';

const GroupsPage = () => {
  return (
    <Box  flex={4} padding={2} bgcolor="skyblue">
      <h2>Users Page</h2>
      <p>Welcome to Users Page!</p>
      <PostP/>
      <PostP/>
      <PostP/>
    </Box>
  );
}

export default GroupsPage;