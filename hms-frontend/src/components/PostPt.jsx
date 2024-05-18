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

  
  


const PostPt = () => {
 
    
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
          image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGhK1vqR6t4ASRiLkdJrR5bh42tV8zJC2yybRmyGIlPw&s"
          alt="Paella dish"
        />
        <CardContent>
          <Typography variant="body2" color="text.secondary">
          The doctor–patient relationship has sometimes been characterized as silencing the voice of patients. It is now widely agreed that putting patients at the centre of healthcareby trying to provide a consistent, informative and respectful service to patients will improve both outcomes and patient satisfaction.

When patients are not at the centre of healthcare, when institutional procedures and targets eclipse local concerns, then patient neglect is possible. Incidents, such as the Stafford Hospital scandal, Winterbourne View hospital abuse scandal and the Veterans Health Administration controversy of 2014 have shown the dangers of prioritizing cost control over the patient experience. Investigations into these and other scandals have recommended that healthcare systems put patient experience at the center, and especially that patients themselves are heard loud and clear within health services.

There are many reasons for why health services should listen more to patients. Patients spend more time in healthcare services than regulators or quality controllers, and can recognize problems such as service delays, poor hygiene, and poor conduct. Patients are particularly good at identifying soft problems, such as attitudes, communication, and that are difficult to capture with institutional monitoring.

One important way in which patients can be placed at the centre of healthcare is for health services to be more open about patient complaints. Each year many hundreds of thousands of patients complain about the care they have received, and these complaints contain valuable information for any health services which want to learn about and improve patient experience.
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

export default PostPt;