from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

TYPES = [
    ('project', 'Project'),
]


class TimeSheetWorkSheet(models.Model):
    _name = 'work.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Work Sheet'

    name = fields.Char('Name', required=True)
    date = fields.Date('Date', required=True)
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    work_id = fields.Many2one('timesheet.work')
    type = fields.Selection(string='Type', related='work_id.type')
    employee_ids = fields.Many2many('hr.employee')
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')
    type_id = fields.Many2one('project.time.type', 'Schedule', required=True)
    # Nuevo marzo 22:
    picking_ids = fields.One2many('stock.picking', 'work_sheet_id', string='Pickings')

    set_start_stop = fields.Boolean(related='work_id.set_start_stop', string='Set start & stop time')
    duration = fields.Float('Duration')
    partner_id = fields.Many2one('res.partner', string='Signed by')
    signature = fields.Binary("Signature")
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')

    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id
    )
    project_analytic_id = fields.Many2one(
        'account.analytic.account',
        string='Proj. Analytic',
        related='project_id.analytic_account_id'
    )
    project_so_id = fields.Many2one('sale.order', related='project_id.sale_order_id', store=True, string='Sale Order')

    project_service_ids = fields.One2many(
        'account.analytic.line',
        'work_sheet_id',
        domain=[('product_id','=',False),('work_sheet_so_line_id','=',False)],
        store=True,
        string='Imputaciones'
    )

    @api.depends('picking_ids')
    def get_project_products(self):
        for record in self:
            products = self.env['stock.move'].search([('picking_id','in',record.picking_ids.ids)])
            record.project_product_ids = [(6, 0, products.ids)]
    project_product_ids = fields.Many2many('stock.move', compute=get_project_products, store=False)


    task_sale_order_id = fields.Many2one('sale.order', related='task_id.sale_order_id', string='Sale Order')

    @api.depends('work_id')
    def get_projects(self):
        for record in self:
            projects = []
            partner = record.work_id.partner_id
            project = record.work_id.project_id
            if (partner.id) and (not project.id) and (record.type == 'project'):
                projects = self.env['project.project'].search([('partner_id', '=', partner.id)]).ids
            elif (not partner.id) and (project.id) and (record.type == 'project'):
                projects = self.env['project.project'].search([('id', '=', project.id)]).ids
            elif (partner.id) and (project.id) and (record.type == 'project'):
                projects = self.env['project.project'].search([('id', '=', project.id)]).ids
            elif (not partner.id) and not (project.id) and (record.type == 'project'):
                projects = self.env['project.project'].search([]).ids
            record.project_ids = [(6, 0, projects)]

    project_ids = fields.Many2many('project.project', compute=get_projects, store=False)

#    @api.depends('project_service_ids', 'project_product_ids', 'repair_service_ids', 'repair_product_ids','mrp_service_ids', 'mrp_product_ids')
    @api.depends('project_service_ids', 'project_product_ids')
    def get_workread_only(self):
        for record in self:
            isreadonly = False
#            if record.project_service_ids or record.project_product_ids or record.repair_service_ids.ids or record.repair_product_ids or record.mrp_service_ids or record.mrp_product_ids:
            if record.project_service_ids or record.project_product_ids:
                    isreadonly = True
            record['work_readonly'] = isreadonly

    work_readonly = fields.Boolean(string='Read only', compute=get_workread_only, store=True)

    @api.depends('signature')
    def get_signed_report(self):
        for record in self:
            if record.signature and not record.signature_status:
                # generate pdf from report, use report's id as reference
                report_id = 'hr_timesheet_work.work_sheet_report'
                pdf = self.env.ref(report_id)._render_qweb_pdf(record.ids[0])
                # pdf result is a list
                b64_pdf = base64.b64encode(pdf[0])
                main_attachment = self.env['ir.attachment'].sudo().search(
                   ['&', ('res_id', '=', record.id), ('name', '=', str(record.type_id.name) + '.pdf')]
                )
                main_attachment.unlink()
                # save pdf as attachment
                name = record.name + (str(record.type_id.name))
                record.attachment_id = self.env['ir.attachment'].sudo().create({
                    'name': name + '.pdf',
                    'type': 'binary',
                    'datas': b64_pdf,
                    'store_fname': name + '.pdf',
                    'res_model': 'work.sheet',
                    'res_id': record.id,
                    'mimetype': 'application/pdf'
                })
                body = "<p>iSet Signed & Approved</p>"
                record.message_post(body=body, attachment_ids=[record.attachment_id.id])
                #self.message_main_attachment_id = [(4, self.attachment_id.id)]
                record.signature_status = True
            else:
                record.signature_status = False

    signature_status = fields.Boolean(string='Signed & Approved',  compute=get_signed_report, store=True)

    def create_lot_worksheet_services(self):
        # Check required fields:
        for record in self:
            # Required start to concatenate later, required duration to change later if startstop:
            start = ""
            duration = record.duration

            # Chek time consumed:
            if (record.set_start_stop == False) and (record.duration == 0):
                raise ValidationError('Please, set the time consumed in Duration.')
            elif (record.set_start_stop == True) and ((record.stop - record.start) <= 0):
                raise ValidationError('Please review start & stop time consumed.')

            # Only if production or set_start_stop = True:
            if (record.set_start_stop == True):
                duration = (record.stop - record.start)
                # Calculate local time diference with UTC:
                date_today = datetime(year=record.date.year, month=record.date.month, day=record.date.day,
                                               hour=12, minute=0)

                date_utc = date_today.astimezone(pytz.timezone(self.env.user.tz))
                inc = date_utc.hour - date_today.hour

                # Change 'hour/min' in record.start to string format to include in fields "name":
                start = str(timedelta(hours=record.start))
                if (record.start >= 10):
                    start = start[:5]
                else:
                    start = " - " + start[:4]

            # CASE USER NOT ADMINISTRATOR, CAN'T SEE FIELD employee_ids => Self timesheet:
            if record.employee_ids.ids:
                employee_ids = record.employee_ids
            else:
                employee_ids = [self.env.user.employee_id]

            # CASE PROJECT:
            if (record.work_id.type == "project") and (record.project_id.id):
                for li in employee_ids:
                    name = record.name + start
                    new = self.env['account.analytic.line'].create(
                        {'work_sheet_id': record.id, 'name': name, 'project_id': record.project_id.id,
                         'task_id': record.task_id.id, 'date': record.date, 'account_id': record.project_analytic_id.id,
                         'company_id': record.company_id.id,
                         'employee_id': li.id, 'unit_amount': duration, 'type_id': record.type_id.id
                         })

