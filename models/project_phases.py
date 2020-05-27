from odoo import api, fields, models, _


class ProjectPhases(models.Model):
    _name = "project.phases"

    @api.model
    def _default_company_id(self):
        if self._context.get('default_project_id'):
            return self.env['project.project'].browse(self._context['default_project_id']).company_id
        return self.env.company

    project_id = fields.Many2one('project.project', string='Project',
                                 default=lambda self: self.env.context.get('default_project_id'),
                                 index=True, tracking=True, check_company=True, change_default=True)
    user_id = fields.Many2one('res.users', string='Assigned to', default=lambda self: self.env.uid, index=True,
                              tracking=True)
    start_date = fields.Date("Start Date of Phase")
    end_date = fields.Date("End Date of Phase")
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=_default_company_id)
    sequence = fields.Integer("Sequence")
    phase_name = fields.One2many("Phase Name")
    deadline = fields.Date("Deadline of The phase")
