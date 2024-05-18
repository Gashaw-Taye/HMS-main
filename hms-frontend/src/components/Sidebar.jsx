// import React from 'react';
import PropTypes from 'prop-types';
import { Box, Divider, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Switch } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import ArticleIcon from '@mui/icons-material/Article';
import GroupsIcon from '@mui/icons-material/Groups';
import SettingsIcon from '@mui/icons-material/Settings';
import InboxIcon from '@mui/icons-material/Inbox';
import SickIcon from '@mui/icons-material/Sick';
import CreateNewFolderIcon from '@mui/icons-material/CreateNewFolder';
import ModeNightIcon from '@mui/icons-material/ModeNight';

const Sidebar = ({ setMode, mode }) => {
    return (
        <Box 
            flex={1}
            padding={2}
            sx={{ display: { xs: "block", sm: "block" } }}>
            <Box position="fixed">
                <Divider />
                <List>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='home'>
                            <ListItemIcon>
                                <HomeIcon />
                            </ListItemIcon>
                            <ListItemText primary="Dashboard" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='patient'>
                            <ListItemIcon>
                                <SickIcon />
                            </ListItemIcon>
                            <ListItemText primary="Patient" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='pages'>
                            <ListItemIcon>
                                <ArticleIcon />
                            </ListItemIcon>
                            <ListItemText primary="Report" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='groups'>
                            <ListItemIcon>
                                <GroupsIcon />
                            </ListItemIcon>
                            <ListItemText primary="Users" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='settings'>
                            <ListItemIcon>
                                <SettingsIcon />
                            </ListItemIcon>
                            <ListItemText primary="Settings" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='inbox'>
                            <ListItemIcon>
                                <InboxIcon />
                            </ListItemIcon>
                            <ListItemText primary="Inbox" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='sample'>
                            <ListItemIcon>
                                <CreateNewFolderIcon />
                            </ListItemIcon>
                            <ListItemText primary="Sample Crud" sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                        <ListItemButton component="a" href='#switch'>
                            <ListItemIcon>
                                <ModeNightIcon />
                            </ListItemIcon>
                            <ListItemText primary="Night Mode" sx={{ display: { xs: "none", sm: "block" } }} />
                            <Switch onChange={() => setMode(mode === "light" ? "dark" : "light")} sx={{ display: { xs: "none", sm: "block" } }} />
                        </ListItemButton>
                    </ListItem>
                </List>
                <Divider />
            </Box>
        </Box>
    );
};

Sidebar.propTypes = {
    setMode: PropTypes.func.isRequired,
    mode: PropTypes.string.isRequired,
};

export default Sidebar;
