from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import json
import logging

_logger = logging.getLogger(__name__)


class API(http.Controller):
    # =========================
    # HEALTH CHECK
    # =========================
    @http.route('/api/ping', type='http', auth='public', methods=['GET'], csrf=False)
    def ping(self, **kwargs):
        return request.make_response(
            json.dumps({
                'success': True,
                'message': 'TCU API running'
            }),
            headers=[('Content-Type', 'application/json')]
        )

    # =========================
    # CREAR ESTUDIANTE 
    # =========================
    @http.route(
        '/api/tcu/student',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def create_student(self, **kwargs):

        try:

            raw_data = request.httprequest.data

            _logger.info("RAW DATA: %s", raw_data)

            post = json.loads(raw_data)

            _logger.info("POST JSON: %s", post)

            required_fields = [
                'name',
                'identification',
                'student_card'
            ]

            for field in required_fields:
                if not post.get(field):
                    return request.make_response(
                        json.dumps({
                            'success': False,
                            'message': f'Campo requerido: {field}'
                        }),
                        headers=[
                            ('Content-Type', 'application/json')
                        ]
                    )

            vals = {
                'name': post.get('name'),
                'identification': post.get('identification'),
                'student_card': post.get('student_card'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'tcu_place': post.get('tcu_place'),
                'manager_name': post.get('manager_name'),
                'status': post.get('status', 'review'),
                'observations': post.get('observations'),
                'period_id': post.get('period_id'),
                'year': post.get('year'),
            }

            student = request.env[
                'tcu.student'
            ].sudo().create(vals)

            return request.make_response(
                json.dumps({
                    'success': True,
                    'student_id': student.id,
                    'message': 'Estudiante creado correctamente'
                }),
                headers=[
                    ('Content-Type', 'application/json')
                ]
            )

        except Exception as e:

            _logger.exception("ERROR CREATE STUDENT")

            return request.make_response(
                json.dumps({
                    'success': False,
                    'message': str(e)
                }),
                headers=[
                    ('Content-Type', 'application/json')
                ]
            )

    # =========================
    # LISTAR ESTUDIANTES
    # =========================
    @http.route('/api/tcu/students', type='http', auth='public', methods=['GET'], csrf=False)
    def list_students(self):

        students = request.env['tcu.student'].sudo().search([])

        data = []
        for s in students:
            data.append({
                'id': s.id,
                'name': s.name,
                'identification': s.identification,
                'student_card': s.student_card,
                'email': s.email,
                'phone': s.phone,
                'status': s.status,
                'year': s.year,
                'request_date': str(s.request_date)
            })

        return request.make_response(
            json.dumps({
                'success': True,
                'data': data
            }),
            headers=[('Content-Type', 'application/json')]
        )

    # =========================
    # ACTUALIZAR ESTADO 
    # =========================
    @http.route(
        '/api/tcu/student/status',
        type='json',
        auth='public',
        methods=['POST'],
        csrf=False
    )
    def update_status(self, **post):

        _logger.info("UPDATE STATUS POST: %s", post)

        try:

            student_id = post.get('id')
            status = post.get('status')
            observations = post.get('observations')

            student = request.env[
                'tcu.student'
            ].sudo().browse(student_id)

            if not student.exists():
                return {
                    'success': False,
                    'message': 'Student not found'
                }

            if status in ['pending', 'rejected'] and not observations:
                return {
                    'success': False,
                    'message': 'Observaciones requeridas'
                }

            student.write({
                'status': status,
                'observations': observations
            })
            student.action_send_email()
            return {
                'success': True,
                'message': 'Estado actualizado'
            }

        except Exception as e:

            _logger.exception("ERROR UPDATE STATUS")

            return {
                'success': False,
                'message': str(e)
            }
    # =========================
    # LISTAR PERIODOS
    # =========================
    @http.route(
        '/api/tcu/periods',
        type='http',
        auth='public',
        methods=['GET'],
        csrf=False
    )
    def list_periods(self, **kwargs):

        periods = request.env['tcu.period'].sudo().search([
            ('active', '=', True)
        ])

        data = []

        for p in periods:
            data.append({
                'id': p.id,
                'name': p.name,
                'year': p.year,
                'start_date': str(p.start_date),
                'end_date': str(p.end_date),
            })

        return request.make_response(
            json.dumps({
                'success': True,
                'data': data
            }),
            headers=[
                ('Content-Type', 'application/json')
            ]
        )