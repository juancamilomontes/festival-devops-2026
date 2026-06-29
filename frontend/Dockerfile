FROM nginx:alpine

# Copiar archivos del frontend al directorio de Nginx
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css

# Exponer puerto 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
