from odoo import models, fields


class ParishChapel(models.Model):
    _name = "parish.chapel"
    _description = "Capilla / Templo"

    name = fields.Char("Nombre", required=True)
    code = fields.Char("Código interno", required=True)  # parroquiasamara / capillasanpedro
    firebase_key = fields.Char("Clave Firebase")  # opcional, por si quieres guardar churchName tal cual

    active = fields.Boolean(default=True)

    mass_time_ids = fields.One2many(
        "parish.chapel.mass_time",
        "chapel_id",
        string="Horarios de misa",
    )


class ParishChapelMassTime(models.Model):
    _name = "parish.chapel.mass_time"
    _description = "Horario de misa por capilla"

    chapel_id = fields.Many2one(
        "parish.chapel",
        string="Capilla",
        required=True,
        ondelete="cascade",
    )

    title = fields.Char("Título de misa")          # "Misa de intenciones matutina", etc.
    father_name = fields.Char("Nombre del padre")  # fatherName
    schedule_type = fields.Char("Tipo de horario") # scheduleType (available, etc.)
    recur_type = fields.Char("Tipo de recurrencia")# recurType (custom, workDays, allDays, none)
    description = fields.Char("Descripción")       # description del JSON

    # 0 = Lunes ... 6 = Domingo, para ir alineado con Odoo (ojo al map vs tu JSON, ahora lo vemos)
    weekday = fields.Selection([
        ("0", "Domingo"),
        ("1", "Lunes"),
        ("2", "Martes"),
        ("3", "Miércoles"),
        ("4", "Jueves"),
        ("5", "Viernes"),
        ("6", "Sábado"),
    ], string="Día de la semana", required=True)

    start_time = fields.Char("Hora inicio")  # "08:30"
    end_time = fields.Char("Hora fin")      # "09:30"

    active = fields.Boolean(default=True)
