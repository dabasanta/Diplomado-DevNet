# DB

## Instalación del DBMS

Las instrucciones detallan el proceso de instalación del servidor en un sistema operativo Linux Debian.

```bash
sudo apt install mariadb-server
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled.png)

```bash
sudo mysql_secure_installation
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%201.png)

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%202.png)

**operator:******$**

![InkedUntitled.jpg](DB%20535cfe2e25174d5c9073e47320ab9bd0/InkedUntitled.jpg)

## Creacion base de datos

```sql
MariaDB [(none)]> CREATE DATABASE SACL;
Query OK, 1 row affected (0.000 sec)

MariaDB [(none)]> CREATE TABLE SACL.road_logs (
->   id INT PRIMARY KEY AUTO_INCREMENT,
->   latitud DECIMAL(10,6),
->   longitud DECIMAL(10,6),
->   fecha DATETIME,
->   velocidad FLOAT,
->   alerta ENUM('incidente', 'accidente')
-> );
Query OK, 0 rows affected (0.011 sec)
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%203.png)

### Tabla de datos del usuario

```sql
CREATE TABLE SACL.userdata (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(255),
  apellido VARCHAR(255),
  fecha_nacimiento DATE,
  numero_telefono CHAR(10),
  id_vehiculo INT(4),
  contacto_emergencia CHAR(10)
);
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%204.png)

```sql
MariaDB [SACL]> GRANT INSERT ON SACL.userdata TO 'operator'@'localhost';
Query OK, 0 rows affected (0.006 sec)
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%205.png)

## Tabla del sistema SACL-ESP32

```sql
CREATE TABLE SACL.road_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  latitud DECIMAL(10,6),
  longitud DECIMAL(10,6),
  fecha DATETIME,
  velocidad FLOAT,
  alerta ENUM('incidente', 'accidente')
);
```

### DATOS DE EJEMPLO

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%206.png)

```sql
INSERT INTO userdata (nombre, apellido, fecha_nacimiento, numero_telefono, id_vehiculo, contacto_emergencia)
VALUES ('Danilo', 'Basanta', '1998-05-02', '3233272006', 1, '3233272006');
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%207.png)

```sql
INSERT INTO road_logs (latitud, longitud, fecha, velocidad, alerta)
VALUES (10.9867, -74.8050, CURDATE(), 65.6, 'incidente');
```

```sql
INSERT INTO road_logs (latitud, longitud, fecha, velocidad, alerta)
VALUES (11.0311, -74.8502, DATE_SUB(CURDATE(), INTERVAL 1 DAY), 45.5, 'accidente');
```

## Ejecución del servicio DBMS en internet

```bash
netstat -tnlp
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%208.png)

Debemos configurar MYSQL para escuchar en todas las interfaces, para esto editamos el siguiente archivo, modificando la bandera bind-address a 0.0.0.0

```bash
/etc/mysql/mariadb.conf.d/50-server.cnf
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%209.png)

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%2010.png)

## Conexiones remotas

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%2011.png)

```sql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'152.201.160.25' IDENTIFIED BY 'tu_contraseña';
```

Login desde una ubicación remota:

```bash
└─$ mysql -h 34.71.210.97 -P 3306 -u operator -p
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 30
Server version: 10.5.19-MariaDB-0+deb11u2 Debian 11

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
MariaDB [(none)]> quit
Bye
```

![Untitled](DB%20535cfe2e25174d5c9073e47320ab9bd0/Untitled%2012.png)

