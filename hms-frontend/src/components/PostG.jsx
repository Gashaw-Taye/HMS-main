import {
    Avatar,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  CardMedia,
  Checkbox,
  IconButton,
  Typography,
} from "@mui/material";
import { red } from '@mui/material/colors';
import ShareIcon from '@mui/icons-material/Share';
import MoreVertIcon from '@mui/icons-material/MoreVert';
// import React from "react";
import { Favorite, FavoriteBorder } from "@mui/icons-material";

  
  


const PostG = () => {
 
    
  return (
      <Card sx={{ margin: 1 }}>
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
              G
            </Avatar>
          }
          action={
            <IconButton aria-label="settings">
              <MoreVertIcon />
            </IconButton>
          }
          title="Gashaw Taye"
          subheader="may 11, 2024"
        />
        <CardMedia
          component="img"
          height="20%"
          image="https://static.prod01.ue1.p.pcomm.net/blackbaud/user_content/photos/000/006/6783/a6132a5cd55abcae190bc82567ca8a47-original-users.png"
          alt="Paella dish"
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
          April 23, 2024 - Data have become increasingly valuable across industries as technologies like the Internet and smartphones have become commonplace. These data can be used to understand users, build business strategies and deliver services more efficiently.

However, healthcare data are some of the most precious — and most targeted — sources of information in the digital age. When used by health systems, providers and patients, these data can help significantly improve care delivery and outcomes, especially when incorporated into advanced analytics tools like artificial intelligence (AI).

Healthcare AI has generated major attention in recent years, but understanding the basics of these technologies, their pros and cons, and how they shape the healthcare industry is vital.

This list details — in alphabetical order — the top 12 ways that AI has and will continue to impact healthcare.
          </Typography>
        </CardContent>
        <CardActions disableSpacing>
          <IconButton aria-label="add to favorites">
          <Checkbox icon={<FavoriteBorder />} checkedIcon={<Favorite sx={{color:"red"}}/>} />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
     
        
        </CardActions>
        
      </Card>
  );
};

export default PostG;