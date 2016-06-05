#Debido a que cuando el servidor de desarrollo se apaga los datos e la ndb se pierden se entiende que
#cada vez que se quiera iniciar el trabajo en el proyecto deberán ejecutarse las siguiéntes órdenes.

echo -e "\n### ¡¡ Run ALL !! ###\n"
cat << "EOF"
 ▄▄▄▄▄▄▄▄▄▄▄  ▄▄       ▄▄  ▄▄▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░░▌     ▐░░▌▐░░░░░░░░░░░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌░▌   ▐░▐░▌▐░█▀▀▀▀▀▀▀▀▀
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▐░▌ ▐░▌▐░█▄▄▄▄▄▄▄▄▄
▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀█░▌▐░▌   ▀   ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌
 ▄▄▄▄▄▄▄▄▄█░▌▐░▌       ▐░▌ ▄▄▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀
EOF

echo "Runing SMS-Back-End"
. SMS-Back-End/run.sh &

sleep 5

echo "Runing SMS-Front-End"
. SMS-Front-End/run.sh &

sleep 5

echo "3. Arrancando mysql"
sudo /etc/init.d/mysql start

echo "5. Aprovisionando sistema con datos de ejemplo"
cd aprovisionador
. aprovisionadorDatosEjemplo.sh
cd ..


echo -e "\n\nEn caso de encontrar algún error por favor revise el script .runAll.sh e intente ejecutar la parte fallida"
