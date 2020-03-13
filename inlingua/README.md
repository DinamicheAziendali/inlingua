# Per avviare odoo ed aggiornare db e modulo

python /odoo10/OCB/odoo-bin -c /path/file_di_config -d nome_database -u nome_modulo

# Installazione
Eseguire lo script `./install.sh`
ed aggiungere le directory dei moduli indicate dallo script alla configurazione 

## Dipendenze pyton
* codicefiscale
* croniter

## Dipendenze odoo
* https://github.com/OCA/partner-contact.git
* https://github.com/OCA/l10n-italy.git
* https://github.com/OCA/project.git
* https://github.com/OCA/hr-timesheet.git
