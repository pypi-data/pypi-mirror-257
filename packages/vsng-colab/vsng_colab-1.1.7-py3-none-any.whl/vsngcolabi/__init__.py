from google.colab import userdata , output
from IPython.display import HTML , Javascript 
from google.colab.output import clear as clear_output
import portpicker , requests 
from urllib.parse import urlencode, urljoin
import threading , os , time
from google.colab import userdata



class vsng : 
    def __init__(self,port = portpicker.pick_unused_port() , ngrok_token = userdata.get('NGROK_TOKEN')  , folder = "/content/") : 
        self.port  = port 
        self.folder = os.path.abspath(folder) 
        self.ngrok_token = ngrok_token

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
        vs_code_btn  = """
        <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Section with Button</title> <style> body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }} .section {{background-color: #fff; padding: 50px; text-align: center; }} .button {{display: inline-block; padding: 20px 40px; /* Adjust padding to make the button bigger */ font-size: 25px; /* Increase font size */ background-color: #007bff; color: #fff; border: none; border-radius: 5px; cursor: pointer; width: 80%; font-weight: 400; letter-spacing: 2px ; }} </style> </head> <body> <section class="section"> <button onclick="window.open('{openpath}', '_blank');" class = "button" >Open vs-code .</button> </section> </body> </html>
        """.format(openpath = self.url )
        display(Javascript(f"window.location.href  = '{self.url}' ; "))
        display(Javascript("window.open('{openpath}', '_blank')".format(openpath = self.url )))
        return self.url 



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
    

vs = vsng()
url = vs()
vs.join()