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