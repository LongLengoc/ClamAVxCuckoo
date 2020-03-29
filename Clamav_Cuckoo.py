import clamd
import requests
import json

"""
clamd is a portable Python module to use the ClamAV anti-virus engine on Windows, 
Linux, MacOSX and other platforms.
"""

class build():
    @staticmethod
    def run_clamd():

        # test if server is reachable
        cd = clamd.ClamdUnixSocket()
        # file or directory you want to check
        file1 = ""
        # scan
        cd.scan(file1)

        """
        output cd.scan(file)
        - if ok
            > {u'file': (u'OK', None)}
        - if detect something
            > {'/tmp/EICAR': ('FOUND', 'Eicar-Test-Signature')}             
        """

        result = cd.scan(file1)
        if (result['file1'][0] == "FOUND"):
            # direct to cuckoo
            run_cuckoo(file1)
        else:
            # file clean
            return 

    @staticmethod
    def run_cuckoo(file1):
        # By default it will bind the service on localhost:8090

        # POST /tasks/create/file: Adds a file to the list of pending tasks to be processed and analyzed.
        # Adds a file to the list of pending tasks. Returns the ID of the newly created task

        """
        To allow only authenticated access to the API, the api_token in cuckoo.conf must be set to a secret value. 
        In new Cuckoo installations, a random token is automatically generated for you. 
        To access the API, you must send the Authorization: Bearer <token> header with all your requests using the token defined in the configuration.
        Note that if you want to access the API over an insecure network such as the Internet, 
        you should run the API server behind nginx described in the next section and enable HTTPS.
        """
        
        """
        # The authentication token that is required to access the Cuckoo API, using
        # HTTP Bearer authentication. This will protect the API instance against
        # unauthorized access and CSRF attacks. It is strongly recommended to set this
        # to a secure value.
        api_token = TeYLAFvaeYVr01dBQ4VybQ
        """

        REST_URL = "http://localhost:8000/tasks/create/file"
        #REST_URL = "http://localhost:8000/submit/api/filetree/"
        #REST_URL1 = "http://localhost:8000/submit/api/submit"
        SAMPLE_FILE = file1
        HEADERS = {"Authorization" : "Bearer TeYLAFvaeYVr01dBQ4VybQ"}

        with open(SAMPLE_FILE, "rb") as sample:
            files = {"file": ("temp_file_name", sample)}
            r = requests.post(REST_URL, headers=HEADERS, files=files)
            print (r.status_code) 
            #r1 = requests.post(REST_URL1, headers=HEADERS, files=files)
            #print (r1.status_code)

        # check task id
        #task_id = r.json()["task_id"]
        #print(task_id)

def main():
    buildproject = build()
    buildproject.run_clamd()

if __name__ == '__main__':
    main()
