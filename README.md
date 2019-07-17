# birthday-app
A python flask app deployed on GKE
Description of files:
main.py: Actual file which includes coding and logic for the application.
requirements.txt: depencies of main.py.
DockerFile: Docker file to create the container.
kube-deployment.yaml: To deploy the app on kuberenetes cluster
rolling-update.yaml: no down-time deplyment of update or second version.
