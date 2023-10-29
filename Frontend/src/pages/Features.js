import React from 'react';
import { Box, SimpleGrid, Icon, Text, Stack, Flex } from '@chakra-ui/react';
import { FaBrain,FaRobot,FaUserFriends , FaPhone ,FaShieldAlt ,FaComment} from 'react-icons/fa';

function Features({ title, text, icon }) {
    return (

        <Stack>
            <Box
                p={7}
                borderWidth="2px" // Add a border around the entire card
                borderColor="red.300" // Specify the border color
                borderRadius="xl"
                boxShadow="xl" // Add a shadow to the box
                height="100%" // Add rounded corners
                bg="whitesmoke"
            >
                <Flex
                    w={16}
                    h={16}
                    align={'center'}
                    justify={'center'}
                    color={'white'}
                    rounded={'full'}
                    bg={'red.400'}
                    mb={1}
                >
                    {icon}
                </Flex>
                <Text fontWeight={920}>{title}</Text>
                <Text color={'gray.600'}>{text}</Text>
            </Box>
        </Stack>

    );
}

export default function SimpleThreeColumns() {
    return (
        <Box p={75} marginTop={70}>
            <SimpleGrid columns={{ base: 1, md: 2 }} spacing={90}>
                <Features
                    icon={<Icon as={FaBrain} w={10} h={10} />}
                    title={'Mental Heath Assessment'}
                    text={
                        'At Mindful AI, we offer a comprehensive mental health assessment tool. This tool helps you gain insights into your mental well-being by answering a series of questions. Its the first step towards understanding yourself better.'
                    }
                />
                <Features
                    icon={<Icon as={FaRobot} w={10} h={10} />}
                    title={'ChatBot Support'}
                    text={
                        'Our AI chatbot is here to offer real-time mental health support. Whether you have questions, need someone to talk to, or require assistance with specific issues like stress, anxiety, or depression, our chatbot is available to listen and provide guidance.'
                    }
                />
                <Features
                    icon={<Icon as={FaUserFriends} w={10} h={10} />}
                    title={'Personalized Guidance'}
                    text={
                        'Based on the results of your assessment, we provide you with personalized mindfulness exercises, relaxation techniques, and coping strategies. These recommendations are designed to help you manage stress, anxiety, and other mental health challenges effectively.'
                    }
                />
                <Features
                    icon={<Icon as={FaPhone} w={10} h={10} />}
                    title={'Crisis Helplines and Resources'}
                    text={
                        'We understand that sometimes you might need immediate help. Thats why we offer a list of crisis helplines and local mental health resources. These are invaluable in emergencies and when you need the support of human professionals.'
                    }
                />
                <Features
                    icon={<Icon as={FaShieldAlt} w={10} h={10} />}
                    title={'Data Privacy and Security'}
                    text={
                        'Your privacy is a top priority for us. Your assessment data and personal information are stored securely, following strict data protection regulations, ensuring your confidentiality.'
                    }
                />
                <Features
                    icon={<Icon as={FaComment} w={10} h={10} />}
                    title={'Feedback-Driven Improvement'}
                    text={
                        'We value your input. Your feedback drives the continuous enhancement of our platform, making it even more useful for you and others.'
                    }
                />

            </SimpleGrid>
        </Box>
    );
}