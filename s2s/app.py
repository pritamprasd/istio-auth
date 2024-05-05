from flask import Flask, request
from kubernetes import client, config
# from istio_client import AuthorizationPolicyV1Alpha1Api
import yaml
import traceback
import os
from external.file_operations import save_yaml_to_file, backup_file

app = Flask(__name__)
BACKUP_DIR = "/tmp/backup_location"


config.load_kube_config()
v1 = client.AppsV1Api()

@app.route('/apply-yaml', methods=['POST'])
def apply_yaml():
    try:
        yaml_content = request.data.decode('utf-8')
        filename = save_yaml_to_file(yaml_content)
        if filename is None:
            return "Error saving YAML to file", 500

        os.system(f"kubectl apply -f {filename}")
        backup_file(filename)
        return {'status': 'success'}, 200
    except Exception as e:
        traceback.print_exception(e)
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
