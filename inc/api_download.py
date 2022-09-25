import os
import logging
import requests
import json
import apie

class download(external):
    def __init__(this, name="download"):
        super().__init__(name)

        this.supportedMethods = ['GET']

        # The secondary_field is used if the first request *this makes returns a json describing the file to be downloaded. In such a case, a second request is made to the url provided by the field specified in the json of the response to the first request.
        # If the secondary_field is None, the response to the first request is returned.
        this.optionalKWArgs['secondary_field'] = None

        this.helpText = '''\
Download any file by offloading the retrieval work to another API.
This does not (currently) have access to the local filesystem.

Per the parent 'external':
'''
        this.helpText += super().helpText

    def MakeRequest(this):

        #TODO: does stream=True work? Can we pass a stream through requests to flask?

        if (this.secondary_field is None):
            this.externalResponse = requests.request(**this.externalRequest, stream=True)
            return

        firstResponse = requests.request(**this.externalRequest)
        frJson = json.loads(firstResponse.content.decode('ascii'))

        this.externalResponse = requests.get(frJson[this.secondary_field], stream=True)

    # All we're doing here is setting a 2-stage download process.
    # We can use the external Call() method.