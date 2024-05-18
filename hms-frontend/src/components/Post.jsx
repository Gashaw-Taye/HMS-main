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

  
  


const Post = () => {
 
    
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
          image="https://cdn.shopify.com/s/files/1/0070/7032/files/homepage-design.png?v=1703001238"
          alt="Paella dish"
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
          First impressions matter, and for ecommerce brands, it can set the tone for your relationship with potential customers. Make a bad impression and you might lose a sale. Make a great one and you could gain a loyal customer for life.

Often a website homepage is one of the first opportunities to make such an impression. It’s where curious consumers land after seeing an Instagram ad or hearing about your brand through word of mouth.

Homepage design plays a big part in how that interaction plays out. The way you arrange site elements, the ease of your navigation, the colors and images you choose to represent your brand all matter here.

Ahead, understand the elements of website design and look to successful online brands and homepage design examples as inspiration for your own ecommerce business.
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

export default Post;