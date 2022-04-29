# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api
from pydub import AudioSegment
import base64
import tempfile
from odoo.exceptions import ValidationError

class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def update_ogg2mp3(self):
        strname = str(self.name)
        print("PATH", self._full_path(self.store_fname))
        path = self._full_path(self.store_fname)
        strlen = len(strname)
        ext = strname[(strlen - 3)] + strname[(strlen - 2)] + strname[(strlen - 1)]

        if ext == 'ogg' and self.datas:
            # De ogg a mp3
            print("import")
            #song = AudioSegment.from_ogg(base64.b64decode(self.datas))
            data = base64.b64decode(self.datas)
            print(self._storage)
            with open("/tmp/audio.ogg", "wb") as file:
                file.write(data)
            print("export")


            AudioSegment.from_ogg("/tmp/audio.ogg").export('/tmp/result.mp3', format='mp3')

            #song.export(('/tmp/odoo/%s.mp3',self.name), format="mp3")
            #f = open(('/tmp/odoo/%s.mp3',self.name), 'rb')
            #file_content = f.read()
            #f.close()
            #self.datas = file_content
        print("DEBUG")
        print(strname)
        print(ext)

