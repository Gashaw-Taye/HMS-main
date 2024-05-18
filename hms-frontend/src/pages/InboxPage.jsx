import { Box } from '@mui/material';
// import React from 'react';
import PostI from '../components/PostI';

const InboxPage = () => {
  return (
    <Box  flex={4} padding={2} bgcolor="skyblue">
      <h2>Inbox Page</h2>
      <p>Welcome to Inbox Page!</p>
      <PostI/>
      <PostI/>
      <PostI/>
      <PostI/>
    </Box>
  );
}

export default InboxPage;