import React, { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import {
  Container,
  Text,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Grid,
  GridItem,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from "@chakra-ui/react";

export default function Home() {
  const { user } = useContext(AuthContext);
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    gender: "",
    age: "",
    marital_status: "false",
    employment_status: "false",
    education: "true",
  });
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async () => {
    // Create the data payload for the cURL request
    const data = new URLSearchParams(formData);

    try {
      const response = await fetch(
        "https://backend-mindfulai.azurewebsites.net/mongo_db/add_personal_information_by_email",
        {
          method: "POST",
          headers: {
            accept: "application/json",
            "email-id": user.email,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: data,
        }
      );

      if (response.ok) {
        setSuccessMessage("Data sent successfully.");
        setErrorMessage("");
      } else {
        setSuccessMessage("");
        setErrorMessage("Failed to send data to the server.");
      }
    } catch (error) {
      setSuccessMessage("");
      setErrorMessage("An error occurred: " + error.message);
    }
  };

  return (
    <Container>
      <Text fontSize="2xl" textAlign="center" mt="4" mb="5">
        Welcome to MindFulAI
      </Text>
      {user ? (
        <div>
          {successMessage && (
            <Alert status="success" mt="4">
              <AlertIcon />
              <AlertTitle mr={2}>Success!</AlertTitle>
              <AlertDescription>{successMessage}</AlertDescription>
            </Alert>
          )}
          {errorMessage && (
            <Alert status="error" mt="4">
              <AlertIcon />
              <AlertTitle mr={2}>Error!</AlertTitle>
              <AlertDescription>{errorMessage}</AlertDescription>
            </Alert>
          )}
          <form>
            <Grid templateColumns="repeat(2, 1fr)" gap={4}>
              <GridItem>
                <FormControl>
                  <FormLabel>First Name</FormLabel>
                  <Input
                    type="text"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    borderColor="black"
                  />
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Last Name</FormLabel>
                  <Input
                    type="text"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    borderColor="black"
                  />
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Gender</FormLabel>
                  <Select
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Age</FormLabel>
                  <Input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    borderColor="black"
                  />
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Marital Status</FormLabel>
                  <Select
                    name="marital_status"
                    value={formData.marital_status}
                    onChange={handleInputChange}
                  >
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Employment Status</FormLabel>
                  <Select
                    name="employment_status"
                    value={formData.employment_status}
                    onChange={handleInputChange}
                  >
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem>
                <FormControl>
                  <FormLabel>Education</FormLabel>
                  <Select
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                  >
                    <option value="true">True</option>
                    <option value="false">False</option>
                  </Select>
                </FormControl>
              </GridItem>
              <GridItem colSpan={2} textAlign="center">
                <Button
                  mt="1rem"
                  onClick={handleSubmit}
                  colorScheme="teal"
                  variant="outline"
                >
                  Submit
                </Button>
              </GridItem>
            </Grid>
          </form>
        </div>
      ) : (
        <Text fontSize="xl" textAlign="center" mt="4">
          Please sign in to view this content.
        </Text>
      )}
    </Container>
  );
}
