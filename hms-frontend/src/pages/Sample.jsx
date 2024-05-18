// import * as React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { 
  Box, 
  Button,
  IconButton,
  Table,
  TableCell,
  TableRow,
  TableHead,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Tooltip,
  Card,
  CardHeader,
  Avatar,
} from "@mui/material";
import {Add} from "@mui/icons-material"
import { DataGrid } from '@mui/x-data-grid';
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { red } from "@mui/material/colors";



export default function App() {

    const columns = [
        { field: 'id', headerName: 'ID', width: 90 },
        { field: 'name', headerName: 'Name', width: 150 },
        { field: 'sex', headerName: 'Sex', width: 150 },
        { field: 'age', headerName: 'Age', type: 'number', width: 110 },
        { field: 'phone', headerName: 'Phone', width: 150 },
        {
          field: 'edit',
          headerName: 'Edit',
          width: 120,
          renderCell: (params) => (
            <TableCell>
              <Tooltip
                title={`Hi, do you want to edit ${params.row.name}?`}
                arrow
              >
                <IconButton
                  onClick={() => fetchUser(params.row.id)}
                  variant="outlined"
                  color="primary"
                >
                  <EditIcon />
                </IconButton>
              </Tooltip>
            </TableCell>
          ),
        },
        {
          field: 'delete',
          headerName: 'Delete',
          width: 120,
          renderCell: (params) => (
            <TableCell>
              <Tooltip
                title={`Hi, do you want to delete ${params.row.name}?`}
                arrow
              >
                <IconButton
                  onClick={() => deleteUser(params.row.id)}
                  variant="outlined"
                  color="secondary"
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </TableCell>
          ),
        },
      ];
  // Drawer state
//   const [open, setOpen] = React.useState(false);  

  // State for users and user object
  const [users, setUsers] = useState([]);
  const [user, setUser] = useState({
    id: 0, // Initial state should be an empty string
    name: "",
    sex: "",
    age: 0,
    phone: "",
  });

  // Function to fetch all users
  const fetchUsers = async () => {
    const response = await axios.get("http://127.0.0.1:8000/students/");
    return setUsers(response.data);
  };

  // Fetch users on initial render
  useEffect(() => {
    fetchUsers();
  }, []);

  // Function to fetch a single user by id
  const fetchUser = async (id) => {
    const response = await axios.get(`http://127.0.0.1:8000/students/${id}`);
    return setUser(response.data);
  };

  // Function to create or edit a user
  const CreateorEdituser = async () => {
    if (!user.name || !user.sex || !user.age || !user.phone) {
      alert("Please fill in all required fields.");
      return;
    }
    if (user.id || user.id !== 0) {
      await axios.put(`http://127.0.0.1:8000/students/${user.id}`, user);
    } else {
      await axios.post(`http://127.0.0.1:8000/students/`, user);
    }
    await fetchUsers();
    setUser({ id: "", name: "", sex: "", age: 0, phone: "" });
  };

  // Function to delete a user by id
  const deleteUser = async (id) => {
    await axios.delete(`http://127.0.0.1:8000/students/${id}`);
    await fetchUsers();
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", padding:2 }} bgcolor="skyblue" height="100%">
             <h2>crud Page</h2>
      <p>Welcome to Sample Crud Page!</p>
        <Card sx={{ margin: 1 }}>
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
              P
            </Avatar>
          }         
          title="This is sample crud page practice"
          subheader="may 11, 2024"
        />
      <Box sx={{ display: { xs: "none", sm: "block" } }} >
        {/* Hidden input for user id */}
        <TextField value={user.id} type="hidden" style={{ display: "none" }} />

        {/* Form table */}
        <Table aria-label="simple table">
          <TableHead>
            {/* Table header row */}
            <TableRow>
              <TableCell>
                {/* Name input */}
                <TextField
                  value={user.name}
                  onChange={(e) => setUser({ ...user, name: e.target.value })}
                  id="standard-basic1"
                  label="Name"
                  variant="standard"
                />
              </TableCell>
              {/* Sex input */}
              <TableCell>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                  <InputLabel id="standard-basic">Sex</InputLabel>
                  <Select
                    labelId="standard-basic2"
                    id="standard-basic"
                    value={user.sex}
                    onChange={(e) => setUser({ ...user, sex: e.target.value })}
                    label="Sex"
                  >
                    <MenuItem value={"Male"}>Male</MenuItem>
                    <MenuItem value={"Female"}>Female</MenuItem>
                  </Select>
                </FormControl>
              </TableCell>
              {/* Age input */}
              <TableCell>
                <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
                  <InputLabel id="standard-basic">Age</InputLabel>
                  <Select
                    labelId="standard-basic3"
                    id="standard-basic"
                    value={user.age}
                    onChange={(e) => setUser({ ...user, age: e.target.value })}
                    label="Age"
                  >
                    <MenuItem value={20}>20</MenuItem>
                    <MenuItem value={30}>30</MenuItem>
                    <MenuItem value={40}>40</MenuItem>
                    <MenuItem value={50}>50</MenuItem>
                    <MenuItem value={60}>60</MenuItem>
                    <MenuItem value={70}>70</MenuItem>
                  </Select>
                </FormControl>
              </TableCell>
              {/* Phone input */}
              <TableCell>
                <TextField
                  value={user.phone}
                  onChange={(e) => setUser({ ...user, phone: e.target.value })}
                  id="standard-basic4"
                  label="Phone"
                  variant="standard"
                />
              </TableCell>
              {/* Submit button */}
              <TableCell>
                <Tooltip title="Hi you can add or edit the record here" arrow>
                  <Button
                  startIcon={<Add/>}
                    onClick={() => CreateorEdituser()}
                    variant="contained"
                  >
                    
                    Save
                  </Button>
                </Tooltip>
              </TableCell>
            </TableRow>
          </TableHead>
        </Table>





    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={users}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 5 },
          },
        }}
        pageSizeOptions={[3,5, 10,25,50,100]}
        checkboxSelection
      />
    </div>

        {/* Table for displaying users
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Sex</TableCell>
              <TableCell>Age</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Edit</TableCell>
              <TableCell>Delete</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((row) => (
              <TableRow key={row.id}>
                <TableCell>{row.id}</TableCell>
                <TableCell>{row.name}</TableCell>
                <TableCell>{row.sex}</TableCell>
                <TableCell>{row.age}</TableCell>
                <TableCell>{row.phone}</TableCell>
                <TableCell>
                  <Tooltip
                    title={"Hi, do you want to edit " + row.name + "?"}
                    arrow
                  >
                    <IconButton
                      onClick={() => fetchUser(row.id)}
                      variant="outlined"
                      color="primary"
                    >
                      <EditIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
                <TableCell>
                  <Tooltip
                    title={"Hi, do you want to delete " + row.name + "?"}
                    arrow
                  >
                    <IconButton
                      onClick={() => deleteUser(row.id)}
                      variant="outlined"
                      color="secondary"
                    >
                      <DeleteIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table> */}
      </Box>
      </Card>
    </Box>
  );
}