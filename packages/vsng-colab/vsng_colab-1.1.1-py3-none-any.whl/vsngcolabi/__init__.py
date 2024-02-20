from bashi import bash 
from google.colab import userdata
bash("""
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
    ngrok config add-authtoken "_________________________"

    VERSION=4.21.1

    curl -fOL https://github.com/coder/code-server/releases/download/v$VERSION/code-server_${VERSION}_amd64.deb
    sudo dpkg -i code-server_${VERSION}_amd64.deb
    sudo apt-get install jq
    code-server  --port ******  --auth none --disable-telemetry &


    ngrok http  ****** > /dev/null &

    # Wait for ngrok to generate tunnel URL
    sleep 6

    # Get ngrok tunnel URL
    NGROK_URL=$(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

    echo "Code Server can be accessed at: $NGROK_URL/?folder=/content"
""".replace('_________________________',userdata.get('NGROK_TOKEN')).replace("******",str(port)))
