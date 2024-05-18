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

  
  


const PostS = () => {
 
    
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
          image="https://icons.iconarchive.com/icons/dtafalonso/android-l/512/Settings-L-icon.png"
          alt="Paella dish"
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
          April 15, 2024 - If you’re a clinician with your inbox open for patient portal secure messaging, you need to make sure you have a good inbox management strategy in place.

Coming up against strong patient demand for secure direct messaging and unabating levels of administrative burden and provider burnout, healthcare practitioners need to consider the boundaries that will help them keep their workloads in balance.

Patient portal messaging has long been a pillar of patient engagement. The secure messaging functions embedded in patient portals have proven useful for engaging patients at home, answering questions, and even doing smaller tasks like booking appointments or refilling prescriptions.

But since the COVID-19 pandemic, patient portal messaging has reached a nexus point, with more patients than ever messaging their providers using the tool. According to one 2023 report in JAMIA, patient portal messaging has increased by 157 percent from pre-pandemic times.

That could be considered a good thing, as patients are now using a key modality for managing their care remotely. Patients who message using the portal are inherently more engaged in their care, and using the secure messaging tool helps to get patients answers to their healthcare questions.
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

export default PostS;