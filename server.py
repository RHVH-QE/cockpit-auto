import os
from flask import Flask, request, redirect
from utils.rhel_system import RHEL
app = Flask(__name__)
CURRENT_RUNNING = False


@app.route('/goaway', methods=['GET'])
def goaway():
    return "automation test already running, please goaway"


@app.route('/cockpit-ovirt', methods=['POST'])
def runtest():
    global CURRENT_RUNNING
    if request.method == 'POST':
        msg = request.get_json()
        package_url = msg['package_url']
        if not CURRENT_RUNNING:
            CURRENT_RUNNING = True
            # update RHEL
            if not RHEL.update_system():
                return "Failed to update the system"

            # install package
            if not RHEL.install_ovirt(package_url):
                return "Failed to install the cockpit-ovirt package"

            os.system("python run.py -t rhel_tier")
        else:
            return redirect('/goaway')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
