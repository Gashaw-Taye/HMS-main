// import React from 'react';
import { AppBar, Toolbar, Typography, styled } from '@mui/material';

const StyledToolbar = styled(Toolbar)({
  display: "flex",
  justifyContent: "center"
});

const Footer = () => {
  return (
    <AppBar position='fixed' color='primary' sx={{ top: 'auto', bottom: 0 }}>
      <StyledToolbar>
        <Typography variant='body2' align='center'>
          &copy; {new Date().getFullYear()} TENA HMS. All rights reserved.
        </Typography>
      </StyledToolbar>
    </AppBar>
  );
}

export default Footer;