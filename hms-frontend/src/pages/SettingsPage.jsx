import { Box } from '@mui/material';
// import React from 'react';
import PostS from '../components/PostS';

const SettingsPage = () => {
  return (
    <Box  flex={4} padding={2} bgcolor="skyblue">
      <h2>Settings Page</h2>
      <p>Welcome to Settings Page!</p>
      <PostS/>
      <PostS/>
      <PostS/>
      <PostS/>
    </Box>
  );
}

export default SettingsPage;