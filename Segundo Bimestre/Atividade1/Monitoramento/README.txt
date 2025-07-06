Sistema de Monitoramento de Log em Tempo Real
=============================================

DESCRIÇÃO:
Sistema de monitoramento que processa logs em tempo real utilizando pool de threads,
sockets e análise de padrões suspeitos.

ARQUIVOS:
- monitor_log.py: Monitora simula-log.log e envia dados via socket
- servidor_backup.py: Recebe dados via socket e grava em log-backup.log  
- analise_ameacas.py: Analisa log-backup.log em busca de padrões suspeitos
- simula-log.log: Arquivo de log original a ser monitorado
- log-backup.log: Arquivo de backup criado pelo servidor

COMO EXECUTAR:
==============

1. PRIMEIRO: Execute o servidor de backup
   > python servidor_backup.py
   
   O servidor ficará escutando na porta 9191 aguardando conexões.

2. SEGUNDO: Execute o monitor de logs (em outro terminal)
   > python monitor_log.py
   
   O monitor ficará observando mudanças no arquivo simula-log.log.

3. TERCEIRO: Execute a análise de ameaças (em outro terminal)
   > python analise_ameacas.py
   
   O analisador ficará monitorando o log-backup.log em busca de padrões.

4. TESTE: Adicione dados ao arquivo simula-log.log

FUNCIONALIDADES:
===============

✓ Monitoramento contínuo de arquivo de log
✓ Pool de threads (3 threads para envio, 4 para análise)
✓ Comunicação via sockets TCP
✓ Detecção de padrões suspeitos (dígitos repetidos)
✓ Processamento paralelo
✓ Backup automático dos logs

PADRÕES DETECTADOS:
==================
O sistema detecta sequências de dígitos repetidos como:
- 123333 (4 dígitos 3 repetidos)
- 556677 (dois pares de dígitos repetidos)  
- 999999 (6 dígitos 9 repetidos)

Quando detectado, exibe: "Usuario - RA - Possível Ameaça!"

OBSERVAÇÕES:
============
- Certifique-se que todas as portas estão livres (9191, 9190)
- Os arquivos de log são criados automaticamente se não existirem
- Use Ctrl+C para parar qualquer processo
- O sistema funciona em Windows e Linux

REQUISITOS:
===========
- Python 3.6+
- Módulos: socket, threading, concurrent.futures, re, os, time
- Todos os módulos são nativos do Python

DESENVOLVIDO PARA:
==================
Atividade 1 - Segundo Bimestre - Computação Distribuída e Paralela
Conceitos: Threads, Sockets, Monitoramento de Arquivos, Regex
