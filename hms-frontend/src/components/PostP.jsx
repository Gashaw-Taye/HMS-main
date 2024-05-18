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

  
  


const PostP = () => {
 
    
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
          image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZDnOt2kVZcO52TJ7Bol7-1_opCRu-3v52dyGI1IkYow&s"
          alt="Paella dish"
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
          Stubborn inflation, high interest rates, geopolitical and economic uncertainty, and labor shortages exacted a toll on private equity markets in 2023, and healthcare private equity was not immune. Healthcare buyout values fell but despite those challenges were in line with pre-Covid norms, as demographic trends and the wave of innovation unleashed during the pandemic fueled deal activity. Now there are signals that momentum is picking up, as evidenced by a rising deal volume relative to 2022. Buyers and sellers have a vested interest in bridging valuation gaps to make 2024 a year for catching up. 

This year’s report focuses on the forces creating major opportunities for investors and their portfolio companies, from generative AI to the burgeoning Indian market to innovation in life sciences.
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

export default PostP;