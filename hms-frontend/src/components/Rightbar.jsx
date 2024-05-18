import { Avatar, AvatarGroup, Box, Card, Divider,  List, ListItem, ListItemAvatar, ListItemText, Typography } from '@mui/material';
import React from 'react';
const Rightbar=()=>{
    return(
        <Box 
         flex={1.5}
          padding={2}
          sx={{display:{xs:"none",sm:"block"}}}>
            <Card sx={{ margin: 2 }}>
            <Box  position="fixed" width={250}>              
              <Typography variant='h6' fontWeight={200}>
                Online Friends
              </Typography>
              <Divider  />
              <AvatarGroup max={4}>
                <Avatar alt="Remy Sharp" src="https://t3.ftcdn.net/jpg/02/43/12/34/360_F_243123463_zTooub557xEWABDLk0jJklDyLSGl2jrr.jpg" />
                <Avatar alt="Travis Howard" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSQKaS7LP80SEcKgz9-d_ORjkh1B9hPSUqkeI_mLSnDg&s" />
                <Avatar alt="Cindy Baker" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLwHN4Hzhu1VZsZnS9fbD0om5tyE2TsVIJErhs0RhIJQ&s" />
                <Avatar alt="Agnes Walker" src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
                <Avatar alt="Trevor Henderson" src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1888&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" />
                </AvatarGroup>
          
                <Typography variant='h6' fontWeight={100} mt={2} mb={2}>
                latest Conversation
              </Typography>
              <Divider />
              <List sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar alt="Remy Sharp" src="https://t3.ftcdn.net/jpg/02/43/12/34/360_F_243123463_zTooub557xEWABDLk0jJklDyLSGl2jrr.jpg" />
        </ListItemAvatar>
        <ListItemText
          primary="Belachew"
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                Belete Awoke
              </Typography>
              {" — I'll be in your neighborhood doing errands this…"}
            </React.Fragment>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li"/>
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar alt="Travis Howard" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSQKaS7LP80SEcKgz9-d_ORjkh1B9hPSUqkeI_mLSnDg&s" />
        </ListItemAvatar>
        <ListItemText
          primary="abenezer"
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                abenezer belachew
              </Typography>
              {" — Wish I could come, but I'm out of town this…"}
            </React.Fragment>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar alt="Cindy Baker" src="https://t3.ftcdn.net/jpg/02/43/12/34/360_F_243123463_zTooub557xEWABDLk0jJklDyLSGl2jrr.jpg" />
        </ListItemAvatar>
        <ListItemText
          primary="Adamu"
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                adamu munye
              </Typography>
              {' — Do you have Addis recommendations? Have you ever…'}
            </React.Fragment>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
      <ListItem alignItems="flex-start">
        <ListItemAvatar>
          <Avatar alt="Cindy Baker" src="https://static9.depositphotos.com/1687987/1171/i/450/depositphotos_11715353-stock-photo-young-woman-portrait.jpg" />
        </ListItemAvatar>
        <ListItemText
          primary="Aster"
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component="span"
                variant="body2"
                color="text.primary"
              >
                Aster munye
              </Typography>
              {' — Do you have Addis recommendations? Have you ever…'}
            </React.Fragment>
          }
        />
      </ListItem>
      <Divider variant="inset" component="li" />
      
    </List>
    {/* <Card>
          <Typography variant='h6' fontWeight={100} mt={2} mb={2}>
                latest photos
              </Typography>
              <ImageList sx={{ width: 500, height: 450 }} cols={3} rowHeight={164} gap={5}> 
               <ImageListItem>
                <img alt="Remy Sharp" src="https://t3.ftcdn.net/jpg/02/43/12/34/360_F_243123463_zTooub557xEWABDLk0jJklDyLSGl2jrr.jpg"  loading="lazy" w={164} h={164} fit="crop" auto="format"/>
                <img alt="Travis Howard" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSQKaS7LP80SEcKgz9-d_ORjkh1B9hPSUqkeI_mLSnDg&s" w={164} h={164} fit="crop" auto="format" />
                <img alt="Cindy Baker" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLwHN4Hzhu1VZsZnS9fbD0om5tyE2TsVIJErhs0RhIJQ&s" w={164} h={164} fit="crop" auto="format"/>
                      </ImageListItem> 
                 </ImageList>
                 </Card> */}
                </Box>
                </Card>
          </Box>
    )
}

export default Rightbar