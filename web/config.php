<?php
$db_address = "localhost";          #indirizzo database
$db_user = "root";                  #username database
$db_pass = "";                      #password database
$db_name = "spring";                #nome database
$db_table = "meteo";                #nome tabella dati
$sensor_timeout = 1200;             #dopo quanti secondi il sensore può considerarsi offline (per mandare gli allarmi)
$enable_old_record_clear = true;    #se attivato elimina i record più vecchi di $old_record_clear_offset giorni
$old_record_clear_offset = 1;       #dopo quanti giorni cancellare i record vecchi (il valore minimo è due)