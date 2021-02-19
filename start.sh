SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


if [ -d "${SCRIPTPATH}/venv" ] 
then
	source ${SCRIPTPATH}/venv/bin/activate
else
	echo "no venv found, using system packages instead"
fi

if [ -f "${SCRIPTPATH}/.env" ]
then
	nohup bash -c "exec -a Mikebot python3 ${SCRIPTPATH}/Main.py" &
	disown
	deactivate
else
	printf "DISCORD_TOKEN = \"\" \nDISCORD_GUILD = \nTICTACTOE = " > ${SCRIPTPATH}/.env
	echo "Add in values into .env"
fi

