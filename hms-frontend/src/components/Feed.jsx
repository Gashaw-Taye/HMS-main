import {
    Box,
  
  } from "@mui/material";
  
//   import * as React from 'react';
  import Post from "./Post"
    
  
  
  const Feed = () => {
   
      
    return (
      <Box  flex={4} padding={2} bgcolor="#CCD1D1">
     <Post/>
     <Post/>
     <Post/>
     <Post/>
     <Post/>
     </Box>
    );
  };
  
  export default Feed;