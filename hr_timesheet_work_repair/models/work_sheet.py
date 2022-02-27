from odoo import _, api, fields, models
from datetime import datetime, timezone, timedelta
import pytz
import base64
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

TYPES = [
    ('project', 'Project'),
    ('repair', 'Repair'),
    ('production', 'Production'),
]


class Isets(models.Model):
    _name = 'work.sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Work Sheet'

    name = fields.Char('Name', required=True)
    date = fields.Date('Date', required=True)
    start = fields.Float('Start')
    stop = fields.Float('Stop')
    work_id = fields.Many2one('work.work')
    type = fields.Selection(string='Type', related='work_id.type')
    employee_ids = fields.Many2many('hr.employee')
    repair_id = fields.Many2one('repair.order', string="Repair Order")
    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')
    workorder_id = fields.Many2one('mrp.workorder')
    mrp_id = fields.Many2one('mrp.production', string='Production')

    production_loss_id = fields.Many2one('mrp.workcenter.productivity.loss', related='work_id.production_loss_id')
    repair_location_id = fields.Many2one('stock.location', related='repair_id.location_id', string='Origin Location')
    type_id = fields.Many2one('working.type', 'Schedule', required=True)

    set_start_stop = fields.Boolean(related='work_id.set_start_stop', string='Set start & stop time')
    duration = fields.Float('Duration')
    partner_id = fields.Many2one('res.partner', string='Signed by')
    signature = fields.Binary("Signature")
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    #active = fields.Boolean('Active')

    @api.depends('repair_id')
    def get_service_id(self):
        self.repair_service_id = self.work_id.repair_service_id.id
    repair_service_id = fields.Many2one('product.product', readonly=False, compute='get_service_id', store=True)

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
    mrp_is_locked = fields.Boolean(string='MRP is Locked', related='mrp_id.is_locked')
    mrp_state = fields.Selection(
        string='MRP State', related='mrp_id.state', store=False)
    mrp_date_planned_start = fields.Datetime(
        string='MRP Planned Start',
        store='False',
        related='mrp_id.date_planned_start'
    )
    mrp_date_deadline = fields.Datetime(
        string='MRP deadline',
        store='False',
        related='mrp_id.date_deadline'
    )
    mrp_location_src_id = fields.Many2one('stock.location', string='MRP Location src', store=False, related='mrp_id.location_src_id')
    mrp_location_id = fields.Many2one('stock.location', store=False, related='mrp_id.production_location_id')
    mrp_picking_type_id = fields.Many2one('stock.picking.type', related='mrp_id.picking_type_id', store=False)

    project_service_ids = fields.One2many(
        'account.analytic.line',
        'work_sheet_id',
        domain=[('product_id','=',False),('work_sheet_so_line_id','=',False)],
        store=True,
        string='Imputaciones'
    )
    project_product_ids = fields.One2many(
        'account.analytic.line',
        'work_sheet_id',
        domain=['|',('product_id','!=',False),('work_sheet_so_line_id','!=',False)],
        store=True,
        string='Productos'
    )
    task_sale_order_id = fields.Many2one('sale.order', related='task_id.sale_order_id', string='Sale Order')

    repair_service_ids = fields.One2many('repair.fee', 'work_sheet_id', string='Tech. Services')
    repair_product_ids = fields.One2many('repair.line', 'work_sheet_id', string='Parts')
    mrp_product_ids = fields.One2many('stock.move', 'work_sheet_id', string='Products')
    mrp_service_ids = fields.One2many('mrp.workcenter.productivity', 'work_sheet_id', string='Time consumed')

    @api.depends('work_id')
    def get_productions(self):
        for record in self:
            partner = record.work_id.partner_id
            sale = record.work_id.production_sale_id
            productions = []
            if (partner.id) and (not sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([
                    ('partner_id', '=', partner.id), ('state', 'not in', ['draft', 'done', 'cancel'])
                ]).ids
            elif (not partner.id) and (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([
                    ('sale_id', '=', sale.id), ('state', 'not in', ['draft', 'done', 'cancel'])
                ]).ids
            elif (partner.id) and (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([
                    ('sale_id', '=', sale.id), ('state', 'not in', ['draft', 'done', 'cancel'])
                ]).ids
            elif (not partner.id) and not (sale.id) and (record.type == 'production'):
                productions = self.env['mrp.production'].search([('state', 'not in', ['draft', 'done', 'cancel'])]).ids
            record.production_ids = [(6, 0, productions)]

    production_ids = fields.Many2many('mrp.production', compute=get_productions, store=False)

    @api.depends('work_id')
    def get_repairs(self):
        for record in self:
            repairs = []
            partner = record.work_id.partner_id
            if (partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([('partner_id', '=', partner.id), ('state', 'not in', ['draft', 'done', 'cancel'])]).ids
            elif (not partner.id) and (record.type == 'repair'):
                repairs = self.env['repair.order'].search([('state', 'not in', ['draft', 'done', 'cancel'])]).ids
            record.repair_ids = [(6, 0, repairs)]

    repair_ids = fields.Many2many('repair.order', compute=get_repairs, store=False)

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

    @api.depends('project_service_ids', 'project_product_ids', 'repair_service_ids', 'repair_product_ids','mrp_service_ids', 'mrp_product_ids')
    def get_workread_only(self):
        for record in self:
            isreadonly = False
            if record.project_service_ids or record.project_product_ids or record.repair_service_ids.ids or record.repair_product_ids or record.mrp_service_ids or record.mrp_product_ids:
                isreadonly = True
            record['work_readonly'] = isreadonly

    work_readonly = fields.Boolean(string='Read only', compute=get_workread_only, store=True)

    @api.depends('work_id')
    def get_production_loss(self):
        for record in self:
            record.production_loss_id = record.work_id.production_loss_id.id

    production_loss_id = fields.Many2one('mrp.workcenter.productivity.loss', string='Loss', readonly=False,
                                         compute=get_production_loss)

    @api.depends('signature')
    def get_signed_report(self):
        for record in self:
            if record.signature and not record.signature_status:
                # generate pdf from report, use report's id as reference
                report_id = 'work_base.work_sheet_report'
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

    def create_lot_services_iset(self):
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
            if (record.type == 'production') or (record.set_start_stop == True):
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

            # CASE REPAIR:
            elif (record.work_id.type == "repair") and (record.repair_id.id):
                if (record.work_id.repair_service_id.id):
                    product_id = record.work_id.repair_service_id
                    for li in employee_ids:
                        name = product_id.name + start + " - " + li.name
                        new = self.env['repair.fee'].create({'work_sheet_id': record.id, 'product_id': product_id.id,
                                                        'name': name, 'repair_id': record.repair_id.id,
                                                        'company_id': record.company_id.id,
                                                        'create_uid': li.user_id.id, 'product_uom_qty': duration,
                                                        'price_unit': product_id.list_price,
                                                        'product_uom': product_id.uom_id.id,
                                                        'type_id': record.type_id.id, 'employee_id': li.id,
                                                        'date': record.date
                                                        })
                else:
                    raise ValidationError(
                        'Se requiere definir el PRODUCTO en el tipo de asistencia para poder crear las imputaciones !!')

            # CASE PRODUCTION:
            elif (record.work_id.type == "production") and (record.workorder_id.id):

                date_start = datetime(year=record.date.year, month=record.date.month, day=record.date.day,
                                               hour=int(record.start - inc),
                                               minute=int((record.start - int(record.start)) * 60))
                date_end = datetime(year=record.date.year, month=record.date.month, day=record.date.day,
                                             hour=int(record.stop - inc),
                                             minute=int((record.stop - int(record.stop)) * 60))
                for li in employee_ids:
                    name = record.workorder_id.name + start + " - " + li.name
                    new = self.env['mrp.workcenter.productivity'].create(
                        {'work_sheet_id': record.id, 'description': name, 'production_id': record.mrp_id.id,
                         'workorder_id': record.workorder_id.id, 'workcenter_id': record.workorder_id.workcenter_id.id,
                         'company_id': record.company_id.id,
                         'loss_id': record.production_loss_id.id, 'date_start': date_start, 'date_end': date_end,
                         'type_id': record.type_id.id,
                         'user_id': li.user_id.id
                         })





