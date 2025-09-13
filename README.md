Para la conexión a la DB, debes crear el archivo .env dentro de la carpeta del proyecto si lo quieres ejecutar en un entorno de desarrollo. 
Para producción no es recomendado agregar éste archivo en la carpeta del proyecto, lo mejor es agregar las variables al entorno del sistema operativo.

Ej:

Editas el archivo .env
DB_CONFIG="mariadb+pymysql://usuario:password@localhost/base_de_datos?charset=utf8mb4"