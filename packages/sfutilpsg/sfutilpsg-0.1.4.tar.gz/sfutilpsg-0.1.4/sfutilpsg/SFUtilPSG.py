

import requests
import json

from graphviz import Source

class SFUtilPSG:
    def __init__(self, credentials_file, api_version='59.0', output='psg_graph'):
        self.api_version = api_version
        self.credentials_file = credentials_file
        self.access_token, self.instance_url = self.read_credentials()
        self.output = output
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.spec =  """  graph [  
              rankdir="RL"  
              bgcolor="#efeffd"  
              label="Salesforce ERD - Kalam "  
              labeljust="r"  
              nodesep="0.18"  
              ranksep="0.46"        
              fontname="Courier"  
              fontsize="9"  
            ]; 
            node [  
              fontname="Courier"  
              fontsize="12"  
              shape="box"  
              color="#99ccff" 
              
            ]; 
            edge [ arrowsize="0.8"   ];
            
            """
    


    def read_credentials(self):
        try:
            with open(self.credentials_file, "r") as file:
                credentials = json.load(file)
                access_token = credentials.get("access_token")
                instance_url = credentials.get("instance_url")
                return access_token, instance_url
        except FileNotFoundError:
            print(f"Error: Credentials file '{self.credentials_file}' not found.")
            return None, None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in credentials file '{self.credentials_file}'.")
            return None, None
        
    def fetch_user_related_objects(self, user_id):
        query = f"SELECT Id, ProfileId, Profile.Name, Name FROM User WHERE Id = '{user_id}'"
        url = f"{self.instance_url}/services/data/v{self.api_version}/query?q={query}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            #print (response.json())
            if response.json()['totalSize'] > 0:
                user_data = response.json()["records"][0]
                profile_id = user_data["ProfileId"]
                profile_name = user_data["Profile"]["Name"]
                user_name = user_data["Name"]


                return profile_id, profile_name, user_name
            else:
                return None, None, None
        else:
            print("Error fetching user data:")
            print(response.text)
            return None, None, None

  
    def fetch_permission_set_groups(self, user_id):
        query = f"SELECT PermissionSetId, PermissionSet.Name FROM PermissionSetGroup WHERE DeveloperName = '{user_id}'"
        url = f"{self.instance_url}/services/data/v{self.api_version}/query?q={query}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching permission set groups:")
            print(response.text)
            return None

    def fetch_permission_sets(self, user_id):
        query = f"SELECT PermissionSetId, PermissionSet.Name, PermissionSetGroupId, PermissionSetGroup.DeveloperName FROM PermissionSetAssignment WHERE Assignee.Id = '{user_id}'"
        url = f"{self.instance_url}/services/data/v{self.api_version}/query?q={query}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching permission set groups:")
            print(response.text)
            return None
        
    def generate_dot(self, user_name, profile_name, permission_sets):
        dot = 'digraph SalesforceRelationships {\n'
        dot += self.spec
        dot += f'  "Profile" -> "User: ({user_name})" [label=" Profile",shape="box", dir=back];\n'
        dot += f'  "Profile" [label="Profile\\n({profile_name})", shape="box"];\n'
        if permission_sets:
            for ps in permission_sets["records"] :
                if  ps["PermissionSetGroup"] == None:
                    dot += f'  "User: ({user_name})" -> "{ps["PermissionSet"]["Name"]}" [label="  PS", shape="box", dir=back];\n'
                if ps["PermissionSetGroup"] != None: 
                    dot += f'  "User: ({user_name})" -> "{ps["PermissionSetGroup"]["DeveloperName"]}" [label="  PSG", shape="box" dir=back];\n'
        dot += "}\n"
        return dot

   
    def draw_relationship_graph(self, user_id):
        profile_id, profile_name, user_name  = self.fetch_user_related_objects(user_id)
        if profile_id:
            permission_sets = self.fetch_permission_sets(user_id)
            dot = self.generate_dot(user_name, profile_name, permission_sets)
            graph = Source(dot)
            graph.format = 'svg'
            graph.render(self.output, cleanup=True)

