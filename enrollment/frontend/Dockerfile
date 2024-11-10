# Usar una imagen oficial de Node.js como base
FROM node:18-alpine

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar las dependencias del proyecto
RUN npm install

# Copiar el resto del proyecto al contenedor
COPY . .

# Exponer el puerto que usa React
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["npm", "start"]