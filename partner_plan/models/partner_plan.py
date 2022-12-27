from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PartnerStatus(models.Model):
    _name = 'partner.status'
    _description = 'Partner Status'

    name = fields.Char('Name')
    type = fields.Selection(
        [('delegacion', 'Delegación'),
         ('competencia', 'Competencia'),
         ('potencialanual', 'Potencial Anual'),
         ('actividad', 'Actividad'),
         ('negociación', 'Negociación'),
         ('catalogo', 'Catálogos'),
         ('nlocales', 'Número de locales'),
         ('zonainfluencia', 'Zona de influencia'),
         ('situacionfinanciera', 'Situación financiera'),
         ('valorado', 'Lo más valorado'),
         ('externaliza', 'Externaliza'),
         ('negocio', 'Uds. de negocio'),
         ], required=True, string='Type')
    active = fields.Boolean('Active', default=True, store=True)