# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pc_delegacion_id   = fields.Many2one('partner.plan', string='Delegación', domain=[('type','=','delegacion')])
    pc_competencia_ids = fields.Many2many('partner.plan', string='Competencia', domain=[('type','=','competencia')])
    pc_potencialanual_id = fields.Many2one('partner.plan', string='Potencial anual', domain=[('type','=','potencialanual')])
    pc_actividad_id    = fields.Many2one('partner.plan', string='Actividad', domain=[('type','=','actividad')])
    pc_negociacion_id  = fields.Many2one('partner.plan', string='Negociación', domain=[('type','=','negociacion')])
    pc_catalogo_ids    = fields.Many2many('partner.plan', string='Catálogo', domain=[('type','=','catalogo')])
    pc_nlocal_id       = fields.Many2one('partner.plan', string='Número locales', domain=[('type','=','nlocales')])
    pc_zonainfluencia_id = fields.Many2one('partner.plan', string='Zona de influencia', domain=[('type','=','zonainfluencia')])
    pc_situacionfinanciera_id = fields.Many2one('partner.plan', string='Situación financiera', domain=[('type','=','situacionfinanciera')])
    pc_valorado_id     = fields.Many2one('partner.plan', string='Lo más valorado', domain=[('type','=','valorado')])
    pc_externaliza_ids = fields.Many2many('partner.plan', string='Externaliza', domain=[('type','=','externaliza')])
    pc_negocio_ids     = fields.Many2one('partner.plan', string='Uds. de negocio', domain=[('type','=','negocio')])
