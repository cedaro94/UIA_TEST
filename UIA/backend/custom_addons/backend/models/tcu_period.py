from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


def get_year_selection(self):
    current_year = datetime.now().year
    return [(str(current_year + i), str(current_year + i)) for i in range(5)]


class TcuPeriod(models.Model):
    _name = 'tcu.period'
    _description = 'Periodo TCU'
    _rec_name = 'name'

    name = fields.Char(string='Nombre', required=True)

    active = fields.Boolean(string='Activo', default=True)

    year = fields.Selection(
        selection=get_year_selection,
        string='Año',
        required=True
    )

    start_date = fields.Date(string='Fecha Inicio', required=True)
    end_date = fields.Date(string='Fecha Final', required=True)

    student_ids = fields.One2many(
        'tcu.student',
        'period_id',
        string='Estudiantes'
    )

    @api.constrains('start_date', 'end_date')
    def validate_dates(self):
        for record in self:

            if record.start_date and record.end_date:

                if record.end_date < record.start_date:
                    raise ValidationError(
                        'La fecha final no puede ser menor a la fecha inicial'
                    )