import clamd
import requests
import json

"""
clamd is a portable Python module to use the ClamAV anti-virus engine on Windows, 
Linux, MacOSX and other platforms.
"""

class build():
    def __init__(self):
        # File location
        self.file = "/home/cuckoo/Documents/test"

    def run_clamd(self):
        # Test if server is reachable
        cd = clamd.ClamdUnixSocket()
        # Scan
        cd.scan(self.file)

        """
        output cd.scan(file)
        - if ok
            > {u'file': (u'OK', None)}
        - if detect something
            > {u'/tmp/EICAR': (u'FOUND', 'Eicar-Test-Signature')}             
        """

        result = cd.scan(self.file)
        print(result)
        if (result[self.file][0] == "OK"):
            # direct to cuckoo
            self.run_cuckoo()
        else:
            # file clean
            print("File ok") 

    def run_cuckoo(self):
        # By default it will bind the service on localhost:8090

        # POST /tasks/create/file: Adds a file to the list of pending tasks to be processed and analyzed.
        # Adds a file to the list of pending tasks. Returns the ID of the newly created task

        """
        Location : $CWD/conf/cuckoo.conf
        # The authentication token that is required to access the Cuckoo API, using
        # HTTP Bearer authentication. This will protect the API instance against
        # unauthorized access and CSRF attacks. It is strongly recommended to set this
        # to a secure value.
        api_token = xxxx
        """

        REST_URL = "http://localhost:8090/tasks/create/file"
        SAMPLE_FILE = self.file
        HEADERS = {"Authorization" : "Bearer xxxx"}

        with open(SAMPLE_FILE, "rb") as sample:
            files = {"file": ("temp_file_name", sample)}
            r = requests.post(REST_URL, headers=HEADERS, files=files)
            print ("Status code : " + str(r.status_code))

        # check task id
        task_id = r.json()["task_id"]
        print(task_id)

def main():
    buildproject = build()
    buildproject.run_clamd()
    #buildproject.run_cuckoo()

if __name__ == '__main__':
    main()
