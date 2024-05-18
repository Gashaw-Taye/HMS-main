import * as React from 'react';
import { createBrowserRouter,RouterProvider } from 'react-router-dom';

import { Box,  Stack, ThemeProvider, createTheme } from '@mui/material/';
import Sidebar from './components/Sidebar';
import Rightbar from './components/Rightbar';
import Feed from './components/Feed';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import PagesPage from './pages/PagesPage';
import GroupsPage from './pages/GroupsPage';
import SettingsPage from './pages/SettingsPage';
import InboxPage from './pages/InboxPage';
import Sample from './pages/Sample';
import Footer from './components/Footer';
import PatientsPage from './pages/PatientsPage';
import PageNot from './pages/PageNot';
function App() {
  const router=createBrowserRouter([
{
  path:'/',
  element:<Feed/>,
  errorElement:<PageNot/>
},
{
  path:'/home',
  element:<HomePage/>,
  errorElement:<PageNot/>
},

{
  path:'/Pages',
  element:<PagesPage/>,
  errorElement:<PageNot/>
},
{
  path:'/groups',
  element:<GroupsPage/>
},
{
  path:'/Settings',
  element:<SettingsPage/>,
  errorElement:<PageNot/>
},
{
  path:'/inbox',
  element:<InboxPage/>,
  errorElement:<PageNot/>
},
{
  path:'/sample',
  element:<Sample/>
},
{
  path:'/patient',
  element:<PatientsPage/>,
  errorElement:<PageNot/>
},
  ]);
  const [mode,setMode]=React.useState('light')
  const darkTheme=createTheme({
    palette:{
      mode:mode,
    },
  })

  return (
    <ThemeProvider theme={darkTheme}>
    <Box bgcolor={"background.default"} color={"text.primary"}>
      <Navbar/>
      <Stack direction="row" spacing={2} justifyContent="space-between">
        <Sidebar setMode={setMode} mode={mode}/>
       <RouterProvider router={router}/>
        <Rightbar/>
      </Stack>
      <Footer/>
    </Box>
    </ThemeProvider>
  );
}

export default App;