from bashi import bash , printerror
from pyngrok import ngrok
from urllib.parse import urlencode, urljoin
from google.colab import userdata
import threading 


def configure(install = True, port  = 5000 ,folder = "/content" ,kill = True ) : 
    install_vscode = bash("""
    curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' --output vscode_cli.tar.gz
    tar -xf vscode_cli.tar.gz
    rm vscode_cli.tar.gz
    mv code /usr/bin/
    """  )
    if not install_vscode.ok :
        printerror(install_vscode.stderr)
    if kill : ngrok.kill()
    ngrok.set_auth_token(userdata.get('NGROK_TOKEN'))
    http_tunnel = ngrok.connect(port, "http")
    url = urljoin(http_tunnel.public_url, '?' + urlencode(dict(folder = folder))
    server = threading.Thread(target = bash ,args = (f"""
    code  serve-web --without-connection-token --accept-server-license-terms --port {port}
    """,))
    server.start()
    printok( url)
    return collections.namedtuple('vsngcolabi', ['url', 'server'])(url = url ,server = server )
    return urljoin(http_tunnel.public_url, '?' + urlencode(dict(folder = folder))))


