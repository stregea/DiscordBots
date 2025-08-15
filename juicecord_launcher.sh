GITHUB_USERNAME="stregea"
GITHUB_TOKEN=""

echo "This is supposed to setup the Juicecord discord bot on server startup. Not yet complete."
if [ ! -d "bots" ]; then
    git reset --hard
    git fetch
    git pull
    pip install virtualenv
    virtualenv bots
    source bots/bin/activate
    pip install --upgrade pip

    pip install -r requirements.txt
    echo "$GITHUB_TOKEN"

    rm -r "bots" # remove later
fi
