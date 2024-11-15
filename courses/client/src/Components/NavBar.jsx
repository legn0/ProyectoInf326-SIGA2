import React from "react";
import {
  Box,
  Flex,
  HStack,
  Link,
  IconButton,
  Button,
  useDisclosure,
  Stack,
  useColorModeValue,
  Image,
} from "@chakra-ui/react";
import { HamburgerIcon, CloseIcon } from "@chakra-ui/icons";

import Logo from "../assets/LOGO.png";

export function Navbar() {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <Box bg={useColorModeValue("gray.100", "gray.900")} px={4}>
      <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
        <IconButton
          size={"md"}
          icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
          aria-label={"Open Menu"}
          display={{ md: "none" }}
          onClick={isOpen ? onClose : onOpen}
        />

        <HStack spacing={8} alignItems={"center"}>
          <Image src={Logo} alt="Logo" boxSize="300px" objectFit="contain" />
          <HStack as={"nav"} spacing={4} display={{ base: "none", md: "flex" }}>
            <Link
              href="#home"
              px={2}
              py={1}
              rounded={"md"}
              _hover={{ bg: "gray.200" }}>
              Inicio
            </Link>
            <Link
              href="#Payments"
              px={2}
              py={1}
              rounded={"md"}
              _hover={{ bg: "gray.200" }}>
              Pagos
            </Link>
            <Link
              href="#Couses"
              px={2}
              py={1}
              rounded={"md"}
              _hover={{ bg: "gray.200" }}>
              Cursos
            </Link>
            <Link
              href="#Grades"
              px={2}
              py={1}
              rounded={"md"}
              _hover={{ bg: "gray.200" }}>
              Calificaciones
            </Link>
          </HStack>
        </HStack>

        <Flex alignItems={"center"}>
          <Link
            href="#Profile"
            px={2}
            py={1}
            rounded={"md"}
            _hover={{ bg: "gray.200" }}>
            Perfil
          </Link>
        </Flex>
      </Flex>

      {/* Menú desplegable para dispositivos móviles */}
      {isOpen ? (
        <Box pb={4} display={{ md: "none" }}>
          <Stack as={"nav"} spacing={4}>
            <Link href="#home">Inicio</Link>
            <Link href="#Couses">Cursos</Link>
            <Link href="#Payments">Pagos</Link>
            <Link href="#Grades">Calificaciones</Link>
          </Stack>
        </Box>
      ) : null}
    </Box>
  );
}

export default Navbar;
