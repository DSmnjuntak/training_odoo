# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class training_odoo(models.Model):
#     _name = 'training_odoo.training_odoo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class Kursus(models.Model):
    _name = 'training.kursus'

    name = fields.Char(string="Judul", required=True)
    description = fields.Text()
    session_ids = fields.One2many('training.sesi', 'course_id', string="Sesi")
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null',
                                     string="Penanggung Jawab",
                                     index=True)


class Sesi(models.Model):
    _name = 'training.sesi'

    name = fields.Char(required=True)
    # start_date = fields.Date()
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Durasi Hari")
    seats = fields.Integer(string="Jumlah Kursi")
    taken_seats = fields.Float(string="Kursi Terisi", compute='_taken_seats')
    instructor_id = fields.Many2one('res.partner',
                                    string="Instruktur",
                                    domain=[('instructor', '=', True)])
    course_id = fields.Many2one('training.kursus',
                                ondelete='cascade',
                                string="Kursus",
                                required=True)
    attendee_ids = fields.Many2many('res.partner',
                                    string="Peserta",
                                    domain=[('instructor', '=', False)])

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats