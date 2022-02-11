# Copyright
# License LGPL-3.0 or later (http =//www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class SuasorInvoice(models.Model):
    _name = 'suasor.invoice'
    _description = 'Export to Suasor'

    invoice_id = fields.Many2one(
            'account.move',
        )

    name = fields.Char('DESCRIPCIÓN')
    fecha_emision = fields.Char('FECHA')
    fecha_emision_filtro = fields.Date('FECHA EMISIÓN FILTRO')
    tipo_factura = fields.Char('tipo_factura')
    n_documento = fields.Char('REG.')
    total_factura = fields.Char('TOTAL FACTURA')
    cuenta = fields.Char('CUENTA')
    nif = fields.Char('NIF')
    nombre = fields.Char('NOMBRE')
    provincia = fields.Char('PROVINCIA')
    pais = fields.Char('PAIS')
    grupo = fields.Char('GRUPO CONTABLE')
    pago_automatico = fields.Char('PAGO AUTOMÁTICO')
    operacion_arrendamiento = fields.Char('OPERACIÓN ARRENDAMIENTO')
    concurso_acreedores = fields.Char('CONCURSO ACREEDORES')
    cod_seccion_analitica = fields.Char('CÓD. SECCIÓN ANALÍTICA')
    cod_proyecto_analitica = fields.Char('CÓD. PROYECTO ANALÍTICA')
    ruta_imagen = fields.Char('RUTA IMAGEN')

    base_iva1 = fields.Char('BASE')
    iva_percent1 = fields.Char('%IVA')
    iva_tax1 = fields.Char('IMPORTE IVA')
    imp_irpf1 = fields.Char('IMPORTE RET')
    irpf_percent1 = fields.Char('%RET')
    imp_recargo1 = fields.Char('IMPORTE REC. EQUIV.')
    req_percent1 = fields.Char('%REQ. EQUIV.')
    servicios1 = fields.Char('SERVICIOS')
    bien_inversion1 = fields.Char('BIEN INVERSIÓN')
    cta_contrapartida1 = fields.Char('CONTRAPARTIDA')
    base_iva2 = fields.Char('BASE 2')
    iva_percent2 = fields.Char('%IVA 2')
    iva_tax2 = fields.Char('IMPORTE IVA 2')
    imp_irpf2 = fields.Char('IMPORTE RET 2')
    irpf_percent2 = fields.Char('%RET 2')
    imp_recargo2 = fields.Char('IMPORTE REC. EQUIV. 2')
    req_percent2 = fields.Char('%REQ. EQUIV. 2')
    servicios2 = fields.Char('SERVICIOS 2')
    bien_inversion2 = fields.Char('BIEN INVERSIÓN 2')
    cta_contrapartida2 = fields.Char('CONTRAPARTIDA 2')
    base_iva3 = fields.Char('BASE 3')
    iva_percent3 = fields.Char('%IVA 3')
    iva_tax3 = fields.Char('IMPORTE IVA 3')
    imp_irpf3 = fields.Char('IMPORTE RET 3')
    irpf_percent3 = fields.Char('%RET 3')
    imp_recargo3 = fields.Char('IMPORTE REC. EQUIV. 3')
    req_percent3 = fields.Char('%REQ. EQUIV. 3')
    servicios3 = fields.Char('SERVICIOS 3')
    bien_inversion3 = fields.Char('BIEN INVERSIÓN 3')
    cta_contrapartida3 = fields.Char('CONTRAPARTIDA 3')

    fecha_operacion = fields.Char('FECHA OPERACIÓN')
    fecha_registro = fields.Char('FECHA REGISTRO')
    forma_pago = fields.Char('FORMA DE PAGO')
    terminos_pago = fields.Char('TERMINOS DE PAGO')
    omitir_fuera_plazo = fields.Char('OMITIR FUERA DE PLAZO')

    cod_iva1 = fields.Char('CÓD. IVA')
    cod_reten1 = fields.Char('CÓD. RETENCIÓN')
    base_retencion1 = fields.Char('BASE RETENCIÓN')
    clave_operacion1 = fields.Char('CLAVE OPERACION')
    det_oper_intracomunitaria1 = fields.Char('DET. OPER. INTRACOMUNITARIA')

    cod_iva2 = fields.Char('CÓD. IVA 2')
    cod_reten2 = fields.Char('CÓD. RETENCIÓN 2')
    base_retencion2 = fields.Char('BASE RETENCIÓN 2')
    clave_operacion2 = fields.Char('CLAVE OPERACION 2')
    det_oper_intracomunitaria2 = fields.Char('DET. OPER. INTRACOMUNITARIA 2')

    cod_iva3 = fields.Char('CÓD. IVA 3')
    cod_reten3 = fields.Char('CÓD. RETENCIÓN 3')
    base_retencion3 = fields.Char('BASE RETENCIÓN 3')
    clave_operacion3 = fields.Char('CLAVE OPERACION 3')
    det_oper_intracomunitaria3 = fields.Char('DET. OPER. INTRACOMUNITARIA 3')
