# ses-email

Las credenciales de AWS necesarias para mandar los correos se obtienen
desde las variables de entorno:

- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`

Luego se puede llamar al script pasando la cuenta de correo que va a 
recibir los mismos, y la tasa de envío por hora. Por defecto, la
tasa de envío esta configurada para mandar 100 correos por hora.

Además, es necesario instalar las dependencias del script 
a través de `pip`.

```bash
pip install -r requirements.txt
```

Luego podemos ejecutar el script.

```bash
python ./ses-email.py example@mail.com 10
```

Por comodidad, también se incluye la posibilidad de ejecutarlo con
`docker`.

## Docker

### Build

Al momento de crear la imagen podemos configurar las credenciales,
de manera de no tener que incluirlas al momento de correr los 
contenedores.

```bash
docker build \
  --build-arg aws_access_key=$AWS_ACCESS_KEY \
  --build-arg aws_secret_access_key=$AWS_SECRET_ACCESS_KEY \
  -t ses-email .
```

### Run

El script espera la cuenta que recibira los mensajes, y la tasa de mensajes
por hora, en ese orden. La tasa de mensajes esta configurada por defecto a 
100 mensajes.

```bash
docker run -it --rm ses-email "mail@example.com" 10
```
