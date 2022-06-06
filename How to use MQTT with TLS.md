# How to use MQTT with TLS

This example is based on the following post: https://openest.io/en/services/mqtts-how-to-use-mqtt-with-tls/ 

## *Raspberry Pi - Certificate Authority (CA)*
Create a working folder:
```
mkdir certs
```
```
cd certs
```
```
mkdir ca
```
```
cd ca
```
We use OpenSSL to create a Certificate Authority (CA)
```
openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt
```

Output: (PEM pass phrase = 1234)
```
Generating a RSA private key
.......................................+++++
.+++++
writing new private key to 'ca.key'
Enter PEM pass phrase:
Verifying - Enter PEM pass phrase:
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:AT
State or Province Name (full name) [Some-State]:Austria
Locality Name (eg, city) []:Graz
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Campus02_AT_TestCA
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:Automatisierungstechnik
Email Address []:test@campus02.at
```
Use OpenSSL to print the certificate in text form:
```
openssl x509 -in ca.crt -text -noout
```

## *Raspberry Pi - Certificates for the MQTT broker*
Create a working folder:
```
cd ..
```
```
mkdir broker
```
```
cd broker
```
Generate a broker RSA key
```
openssl genrsa -out broker.key 2048
```

Now, we create a signing request file from this key
```
openssl req -out broker.csr -key broker.key -new
```
Output:
```
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:AT
State or Province Name (full name) [Some-State]:Austria
Locality Name (eg, city) []:Graz
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Campus02 AT
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:Raspi MQTT Broker
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

Now we can pass the Certificate Signing Request (csr) file to our validation authority:
```
openssl x509 -req -in broker.csr -CA ../ca/ca.crt -CAkey ../ca/ca.key -CAcreateserial -out broker.crt -days 2000
```

Use OpenSSL to print the certificate in text form:
```
openssl x509 -in broker.crt -text -noout
```

## *Raspberry Pi - Certificates for the MQTT clients*
Create a working folder:
```
cd ..
```
```
mkdir client
```
```
cd client
```
Generate a client RSA key
```
openssl genrsa -out client.key 2048
```
Now, we create a signing request file from this key
```
openssl req -out client.csr -key client.key -new
```
Output:
```
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:AT
State or Province Name (full name) [Some-State]:Austria
Locality Name (eg, city) []:Graz
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Campus 02 AT
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:MQTT Client Raspi
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

Now we can pass the Certificate Signing Request (csr) file to our validation authority:
```
openssl x509 -req -in client.csr -CA ../ca/ca.crt -CAkey ../ca/ca.key -CAcreateserial -out client.crt -days 2000
```

# Certificaton - Overview
By now you should have all these files:
```
cd ..
```
```
tree .
```
Output:
```
.
|-- broker
|   |-- broker.crt
|   |-- broker.csr
|   `-- broker.key
|-- ca
|   |-- ca.crt
|   |-- ca.key
|   `-- ca.srl
`-- client
    |-- client.crt
    |-- client.csr
    `-- client.key
```