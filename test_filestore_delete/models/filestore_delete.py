import os

from odoo import api, fields, models, _
import paramiko
from os import listdir
import base64
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

STATE = [
    ('draft', 'Draft'),
    ('error', 'Error'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class ResCompany(models.Model):
    _inherit = 'res.company'


    def check_attachment_data(self):
        path="/opt/odoo14/.local/share/Odoo/filestore/14_general"
        contador = 0
        todos = 0
        for folder in os.listdir(path):
            #print("FODLER", folder)
            for file in os.listdir(path + '/' + folder):
                todos += 1
                print("NAME", folder+"/"+file)
                attachment = self.env['ir.attachment'].search([('store_fname','ilike',file),('mimetype','in',['application/pdf'])])
                print(attachment)
                if attachment:
                    contador += 1

                #else:
                    #print("$=$ NOT FOUND")
        raise ValidationError("Todos " + str(todos) + "-" + "CONTADOR " + str(contador))


    def get_n43_list(self):
        imported_n43_ids = self.env['account.bank.statement.cbi'].sudo().search([])
        imported_n43_list = []
        for n43 in imported_n43_ids:
            imported_n43_list.append(n43.name)
        return imported_n43_list

    def move_file_to_downloaded_dir(self, sftpclient, file):
        try:
            sftpclient.rename(file, 'Historico/%s' % file)  # At this point, you are in remote_path in either case
        except IOError:
            _logger.debug("ERROR", IOError)

    def automated_ftp_get_n43_files(self):
        company_ids = self.env['res.company'].sudo().search([])
        for company_id in company_ids:
            if company_id.ftp_url_cbi and company_id.ftp_port_cbi and company_id.ftp_user_cbi and company_id.ftp_passwd_cbi:
                try:
                    sftpclient = self.create_sftp_client(company_id.ftp_url_cbi, company_id.ftp_port_cbi,
                                                         company_id.ftp_user_cbi, company_id.ftp_passwd_cbi, None, 'DSA')
                    # List files in the default directory on the remote computer.
                    dirlist = sftpclient.listdir('.')
                    imported_n43_list = self.get_n43_list()
                    for d in dirlist:
                        path = "/%s" % d
                        result = sftpclient.chdir(path=path)
                        filelist = sftpclient.listdir('.')
                        for f in filelist:
                            if f != 'Historico':
                                if f not in imported_n43_list:
                                    file = sftpclient.file(f, mode='r', bufsize=-1)
                                    file_first = file.readline()
                                    bsa_bank_number = file_first[2:20]
                                    #rename = sftpclient.rename(f,(str(bank_number) + str(f)+ '.n43'))
                                    sftpclient.get(f, '/tmp/%s' % f)

                                    try:
                                        journal = self.env['account.journal'].sudo().search([])
                                        for journal_id in journal:
                                            if journal_id.bank_account_id.acc_number:
                                                bank_account_number = journal_id.bank_account_id.acc_number
                                                bank_mnt_account_number = bank_account_number.replace(' ', '')
                                                first_bank_sequence = bank_mnt_account_number[4:12]
                                                second_bank_secuence = bank_mnt_account_number[14:]
                                                bank_account_number = first_bank_sequence + second_bank_secuence
                                                if bank_account_number == bsa_bank_number:
                                                    with open('/tmp/%s' % f, "r+b") as file:
                                                        data = file.read()
                                                        file.close()
                                                        attachment_id = self.env['ir.attachment'].sudo().create({
                                                            'name': f,
                                                            'type': 'binary',
                                                            'datas': base64.b64encode(data),
                                                            'store_fname': f,
                                                            'res_model': 'account.bank.statement.cbi',
                                                            # 'res_id': self.id,
                                                            'mimetype': 'text/plain'
                                                        })

                                                    self.env['account.bank.statement.cbi'].sudo().create({
                                                        'name': f,
                                                        'journal_id': journal_id.id,
                                                        'bank_statement_attachment_id': attachment_id.id,
                                                        'company_id': journal_id.company_id.id,
                                                    })
                                                    self.move_file_to_downloaded_dir(sftpclient, f)

                                    except Exception as e:
                                        raise ValidationError('Server Error: %s' % e)

                    sftpclient.close()
                    time = datetime.now()
                    company_id.cbi_last_connection_date = time

                except Exception as e:
                    _logger.debug('Server Error: %s' % e)

            if company_id.cbi_autoimport:
                self.automated_import_files()

    def import_files(self):
        for record in self:
            if record.state != 'completed':
                if record.journal_id:
                    record = record.with_context(journal_id=record.journal_id.id, company_id=record.company_id.id)

                    bank_statement = record.env['account.statement.import'].create({
                        'statement_file': record.bank_statement_attachment_id.datas,
                        'display_name': record.bank_statement_attachment_id.name,
                        'statement_filename': record.bank_statement_attachment_id.name,
                    })

                    try:
                        bank_statement.import_file_button()
                        record.state = 'completed'
                        #bank_statement.name = str(bank_statement.date)
                    except Exception as e:
                        record.state = 'error'
                        record.error_logger = e
                        raise ValidationError('Server Error: %s' % e)

    def automated_import_files(self):
        imported_n43_ids = self.env['account.bank.statement.cbi'].search([['state', '=', 'draft']])
        for bsa in imported_n43_ids:

            if bsa.journal_id:
                bsa = bsa.with_context(journal_id=bsa.journal_id.id, company_id=bsa.journal_id.company_id.id, user_id=2)

                bank_statement = bsa.env['account.statement.import'].create({
                    'statement_file': bsa.bank_statement_attachment_id.datas,
                    'display_name': bsa.bank_statement_attachment_id.name,
                    'statement_filename': bsa.bank_statement_attachment_id.name,
                })

                try:
                    bank_statement.import_file_button()
                    bsa.state = 'completed'
                    # bank_statement.name = str(bank_statement.date)
                except Exception as e:
                    bsa.state = 'error'
                    bsa.error_logger = e
                    _logger.debug('Server Error: %s' % e)
