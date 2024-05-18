import { useState } from 'react';
import { Box, AppBar, Toolbar, Typography, styled, InputBase, Avatar, MenuItem, Menu, Badge } from '@mui/material';
import MailIcon from '@mui/icons-material/Mail';
import NotificationsIcon from '@mui/icons-material/Notifications';
import MenuIcon from '@mui/icons-material/Menu';

const StyledToolbar = styled(Toolbar)({
    display: "flex",
    justifyContent: "space-between"
});

const Search = styled("div")(({ theme }) => ({
    backgroundColor: "white",
    padding: "0 10px",
    borderRadius: theme.shape.borderRadius,
    width: "400px"
}));

const Icons = styled(Box)(({ theme }) => ({
    display: "none",
    gap: "20px",
    alignItems: "center",
    [theme.breakpoints.up("sm")]: {
        display: "flex",
    }
}));

const UserBox = styled(Box)(({ theme }) => ({
    display: "flex",
    gap: "10px",
    alignItems: "center",
    [theme.breakpoints.up("sm")]: {
        display: "none",
    }
}));

const Navbar = () => {
    const [open, setOpen] = useState(false);

    return (
        <AppBar position='sticky'>
            <StyledToolbar>
                <Typography
                    variant='h6'
                    sx={{ display: { xs: "none", sm: "block" } }}
                >
                    TENA HMS
                </Typography>
                <MenuIcon sx={{ display: { xs: "block", sm: "none" } }} />
                <Search><InputBase placeholder='Search...' /></Search>
                <Icons>
                    <Badge badgeContent={4} color="error">
                        <MailIcon />
                    </Badge>
                    <Badge badgeContent={2} color="error">
                        <NotificationsIcon />
                    </Badge>
                    <Avatar
                        sx={{ width: 30, height: 30 }}
                        alt="Remy Sharp"
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj5w7hYktD4byIBek2BULUelcM6ybvsS5JBA3PzmA8pA&s"
                        onClick={() => setOpen(true)}
                    />
                </Icons>
                <UserBox onClick={() => setOpen(true)}>
                    <Avatar
                        sx={{ width: 30, height: 30 }}
                        alt="Remy Sharp"
                        src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj5w7hYktD4byIBek2BULUelcM6ybvsS5JBA3PzmA8pA&s"
                    />
                    <Typography variant='span'>John</Typography>
                </UserBox>
            </StyledToolbar>
            <Menu
                id="demo-positioned-menu"
                aria-labelledby="demo-positioned-button"
                open={open}
                onClose={() => setOpen(false)}
                anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                }}
            >
                <MenuItem>Profile</MenuItem>
                <MenuItem>My account</MenuItem>
                <MenuItem>Logout</MenuItem>
            </Menu>
        </AppBar>
    );
};

export default Navbar;
