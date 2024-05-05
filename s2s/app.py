from flask import Flask, request, jsonify
from kubernetes import client, config
import yaml
import traceback
import os
from external.file_operations import save_yaml_to_file, backup_file

app = Flask(__name__)
BACKUP_DIR = "/tmp/backup_location"


config.load_kube_config()

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

SYSTEM_NAMESPACES = ["istio-system", "kube-node-lease", "kube-public", "kube-system", "kubernetes-dashboard"]

@app.route('/namespaces', methods=['GET'])
def get_all_namespaces():
    try:
        api_instance = client.CoreV1Api()
        namespaces = api_instance.list_namespace().items
        res = []
        for n in namespaces:
            res.append(n.metadata.name)
        return jsonify([x for x in res]) # if x not in SYSTEM_NAMESPACES])
    except Exception as e:
        print(f"Error getting namespaces: {e}")
        return []

@app.route('/namespaces/<namespace>/workloads', methods=['GET'])
def get_deployments_by_namespace(namespace):
    try:
        api_instance = client.AppsV1Api()
        deployments = api_instance.list_namespaced_deployment(namespace).items
        res = []
        for d in deployments:
            print()
            res.append({
                "workload": d.metadata.labels.get("app", ""),
                "service-account": d.spec.template.spec.service_account
            })
        return jsonify(res)
    except Exception as e:
        print(f"Error getting deployments: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9999)
