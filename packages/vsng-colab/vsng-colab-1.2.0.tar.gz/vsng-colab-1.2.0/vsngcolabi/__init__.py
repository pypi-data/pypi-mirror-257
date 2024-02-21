from google.colab import userdata , output
from IPython.display import HTML , Javascript 
from google.colab.output import clear as clear_output
import portpicker , requests 
from urllib.parse import urlencode, urljoin
import threading , os , time
from google.colab import userdata , drive



class vsng : 
    def __init__(self,port = portpicker.pick_unused_port() , ngrok_token = userdata.get('NGROK_TOKEN')  , folder = "/content/") : 
        self.port  = port 
        self.folder = os.path.abspath(folder) 
        self.ngrok_token = ngrok_token
        self.btn = None 

        self.install_vscode_server()
        self.install_ngrok()

    def __call__(self) : 
        self.code_server = threading.Thread(target = os.system  , args = (f"code-server  --port {self.port}  --disable-telemetry --auth none  & " , ))
        self.code_server.start()
        print()
        self.ngrok_server = threading.Thread(target = os.system , args = (f"ngrok config add-authtoken {self.ngrok_token} && ngrok http  {self.port}    > /dev/null " , ))
        self.ngrok_server.start()
        time.sleep(6)
        self.get_public_url()
        self.url = urljoin(self.domain, '?' + urlencode(dict(folder = self.folder)))
        clear_output()
        self.btn  = """
            <button onclick="window.open('{openpath}', '_blank');" style="width:100% ; height:75px ; color : #fff ; background-color: #2aaaff ; font-weight: bold; outline:none ; font-size : 24px ; border-radius : 16px ; border : none ; font-family: monospace, "Droid Sans Mono", "monospace", monospace;">open vs code web</button>
        """.format(openpath = self.url ).strip()
        display(Javascript(f"window.location.href  = '{self.url}' ; "))
        display(Javascript("window.open('{openpath}', '_blank')".format(openpath = self.url )))
        return self.url 

    def send(self,channel = "channel") : 
        display(Javascript(f'''
        const senderChannel = new BroadcastChannel('{channel}');
        senderChannel.postMessage('{self.btn}');
        '''))

    def get_public_url(self) : 
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        ngrok_url = data["tunnels"][0]["public_url"]
        self.domain = ngrok_url





    def install_ngrok(self) : 
        os.system("""    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
        | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
        | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
        """)

    def install_vscode_server(self) : 
        os.system("""
            VERSION=4.21.1
            curl -fOL https://github.com/coder/code-server/releases/download/v$VERSION/code-server_${VERSION}_amd64.deb
            sudo dpkg -i code-server_${VERSION}_amd64.deb
            sudo apt-get install jq
        """)

    def join(self) : 
        self.code_server.join()
        self.ngrok_server.join()
    

def configure(mount = True , folder = "/content/drive/MyDrive/home" ) : 
    if mount : 
        drive.mount('/content/drive')
    vs = vsng(folder = folder)
    url  = vs()
    vs.send()
    vs.join()