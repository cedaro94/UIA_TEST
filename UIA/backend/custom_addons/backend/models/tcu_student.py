from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

def get_year_selection(self):
    current_year = datetime.now().year
    return [(str(current_year + i), str(current_year + i)) for i in range(5)]

class TcuStudent(models.Model):
    _name = 'tcu.student'
    _description = 'Estudiante TCU'
    _rec_name = 'name'
    _order = 'id desc'
    _sql_constraints = [

        (
            'unique_identification',
            'unique(identification)',
            'La identificación ya existe'
        ),

        (
            'unique_student_card',
            'unique(student_card)',
            'El carnet ya existe'
        )

    ]
    name = fields.Char(
        string='Nombre Completo',
        required=True
    )

    identification = fields.Char(
        string='Identificación',
        required=True
    )

    student_card = fields.Char(
        string='Carnet',
        required=True
    )

    email = fields.Char(
        string='Correo'
    )

    phone = fields.Char(
        string='Teléfono'
    )

    tcu_place = fields.Char(
        string='Lugar TCU'
    )

    manager_name = fields.Char(
        string='Encargado'
    )

    request_date = fields.Date(
        string='Fecha Solicitud',
        default=fields.Date.today
    )

    period_id = fields.Many2one(
        'tcu.period',
        string='Periodo TCU'
    )

    year = fields.Selection(
        selection=get_year_selection,
        string='Año'
    )

    status = fields.Selection(
        [
            ('review', 'En revisión'),
            ('pending', 'Pendiente'),
            ('rejected', 'Rechazado'),
            ('approved', 'Aprobado')
        ],
        string='Estado',
        default='review',
        required=True
    )

    observations = fields.Text(
        string='Observaciones'
    )

    acceptance_letter = fields.Binary(
        string='Carta de aceptación'
    )

    acceptance_letter_name = fields.Char(
        string='Nombre Archivo'
    )

    manual_enabled = fields.Boolean(
        string='Edición Manual',
        default=False
    )

    readonly_fields_message = fields.Char(
        compute='_compute_readonly_message'
    )

    @api.depends('manual_enabled')
    def _compute_readonly_message(self):

        for record in self:

            if record.manual_enabled:
                record.readonly_fields_message = 'Edición manual habilitada'
            else:
                record.readonly_fields_message = 'Datos provenientes desde Django API'

    @api.constrains('email')
    def validate_email(self):

        for record in self:

            if record.email:

                regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

                if not re.match(regex, record.email):
                    raise ValidationError(
                        'Correo electrónico inválido'
                    )

    @api.constrains('identification')
    def validate_identification(self):

        for record in self:

            if record.identification:

                if len(record.identification) < 5:
                    raise ValidationError(
                        'La identificación no es válida'
                    )

    @api.constrains('status', 'observations')
    def validate_observations(self):

        for record in self:

            if record.status in ['pending', 'rejected']:

                if not record.observations:
                    raise ValidationError(
                        'Debe ingresar observaciones para estados pendientes o rechazados'
                    )

    def action_enable_manual_edit(self):

        for record in self:
            record.manual_enabled = True

    def action_disable_manual_edit(self):

        for record in self:
            record.manual_enabled = False

    def action_send_email(self):

        _logger.info("START SEND EMAIL")

        for record in self:

            _logger.info("EMAIL DESTINATION: %s", record.email)

            if not record.email:
                raise ValidationError(
                    'El estudiante no tiene correo registrado'
                )

            status_label = dict(
                self._fields['status'].selection
            ).get(record.status)

            subject = f'Estado solicitud TCU: {status_label}'

            body_html = f"""
                <div>
                    <p>Hola {record.name}</p>
                    <p>Estado: {status_label}</p>
                </div>
            """

            mail_values = {
                'subject': subject,
                'body_html': body_html,
                'email_to': record.email,
                'email_from': 'tu_correo@gmail.com',
            }

            _logger.info("MAIL VALUES: %s", mail_values)

            mail = self.env['mail.mail'].sudo().create(mail_values)

            _logger.info("MAIL CREATED ID: %s", mail.id)

            mail.send()

            _logger.info("MAIL SENT")