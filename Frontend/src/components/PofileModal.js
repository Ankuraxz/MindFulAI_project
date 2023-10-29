import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  Text,
  Box,
} from "@chakra-ui/react";

const ProfileModal = ({ isOpen, onClose, user }) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="md">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Profile Details</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          {user && (
            <Box>
              <Text fontWeight="bold">Full Name:</Text>
              <Text>{user.user_metadata.full_name}</Text>
              <Text fontWeight="bold">Email:</Text>
              <Text>{user.email}</Text>
              {/* Add more user details as needed */}
            </Box>
          )}
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};

export default ProfileModal;
