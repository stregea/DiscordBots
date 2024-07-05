GITHUB_USERNAME="stregea"
GITHUB_TOKEN="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"

echo "hello, world!"
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
