Essa atividade foi proposta com objetivo de entender e desenvolver os conceitos de RMI (Remote Method Invocation), para aumentar o domínio sobre o conceito de invocação remota. Para a execução desse sistema, deve-se estar primeiramente localizado na pasta "Atividade2". 

Deve-se usar o seguintes comandos em dois terminais diferentes:

Para inicializar o servidor:

```
    python -m server.server
```

Para inicializar o cliente:

```
    python -m client.client
```

Após a inicialização deles deve-se seguir os fluxos dispostos na execução do terminal cliente:

1 - Definir senha e usuário (verificar no users.json do server)
2 - Definir o tipo de protocolo que será utilizado (R, RR, RRA)
3 - Definir se a comunicação será por demanda ou com sincronismo automático