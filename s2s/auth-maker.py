import yaml

def create_authorization_policies(yaml_content):
    authorization_policies = []

    for document in yaml.safe_load_all(yaml_content):
        if document['kind'] == 'AuthorizationPolicy':
            authorization_policies.append(document)

    return authorization_policies

def write_to_yaml(authorization_policies, filename):
    with open(filename, 'w') as file:
        yaml.dump_all(authorization_policies, file)

# Example YAML content
yaml_content = """
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: flask-app-get-allow
  namespace: namespace-a
spec:
  selector:
    matchLabels:
      app: flask-app
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["flask-app-caller-service-account"]
    - source:
        namespaces: ["namespace-b"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/data1"]
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: flask-app-b-get-allow
  namespace: namespace-a
spec:
  selector:
    matchLabels:
      app: flask-app-b
  action: DENY
  rules:
  - from:
    - source:
        principals: ["flask-app-caller-service-account"]
    - source:
        namespaces: ["namespace-b"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/api/data1"]
"""

# Create AuthorizationPolicy objects
authorization_policies = create_authorization_policies(yaml_content)

# Write AuthorizationPolicy objects to YAML file
write_to_yaml(authorization_policies, 'authorization_policies.yaml')
