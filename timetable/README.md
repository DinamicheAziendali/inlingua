## Composizione
La composizione docker specificata in `docker-compose.yml` è quella base richiesta da odoo per funzionare, 
ed è quindi composta da 

- **odoo** app
- **postgesql** per la persistenza
- **postfix** per l'invio mail 

### Binding volumi
La composizione prevede il binding di
- odoo
    - `/var/lib/odoo` che contiene i dati di esercizio di odoo 
    - `/mnt/extra-addons` nella quale possiamo inserire le estensioni aggiuntive
    - `/etc/odoo` che contiene il file di configurazione preimpostato

- postgresql
    - `/var/lib/postgresql/data`

Nella composizione di default, considerando che `ROOT` corrisponda a `/opt/apps/odoo` il binding è il seguente: 

| container | host |
|:---------|:----|
|/var/lib/odoo|`ROOT`/odoo-data|
|/mnt/extra-addons|`ROOT`/addons|
|/etc/odoo|`ROOT`/conf|
|/var/lib/postgresql/data|`ROOT`/db|

### binding porte e networking
Anche le porte sono state rimappate, in particolar modo, la porta `8069` che è quella di default di odoo è stata
mappata con `10000` e la `5432` di postgre è stata mappata con `10001`.

_**NB** il mapping delle porte svolge la funzione di NAT pertanto vale solo nelle comunicazioni che provengono
 dall'esterno della rete della composizione, le macchine della composizione comunicano tra loro utilizzando le
 porte di default e gli alias definiti nella composizione_ 


## Ambiente locale
Per consentire un agevole sviluppo è possibile configurare la composizione in modo da rendere l'occorrente più
accessibile possibile, pertanto applicheremo alcune alterazioni alla composizione di base

### binding volumi [ local ]
per poter lavorare agevolmente è necessario che i file siano tutti raggiungibili dall'area di sviluppo, in modo
da poter tenere sotto controllo tutte le fasi di deploy. a tale scopo è necessario riviedere il binding dei volumi 
ad hoc.

| container | host |
|:---------|:----|
| /var/lib/odoo | ./_volumes/odoo-data |
| /mnt/extra-addons | ./addons|
| /etc/odoo | ./conf |
| /var/lib/postgresql/data | ./_volumes/db |


### Overload dei compose file [ local ]
eseguire l'overload della composizione docker con  la configurazione locale.
`docker-compose` consente questa operazione specificanto lo stack di file concatenandoli utilizzando il flag `-f`
ne risulta:

```bash
docker-compose -f docker-compose.yml -f docker-compose.local.yml up
```

### Accesso
http://localhost:1000

admin / admin

## Ambiente di produzione 
in maniera analoga
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

## Dipendenze
### croniter
Per esequire questa estensione è necessario installare il modulo `croniter` di python
```bash
pip install croniter
```
