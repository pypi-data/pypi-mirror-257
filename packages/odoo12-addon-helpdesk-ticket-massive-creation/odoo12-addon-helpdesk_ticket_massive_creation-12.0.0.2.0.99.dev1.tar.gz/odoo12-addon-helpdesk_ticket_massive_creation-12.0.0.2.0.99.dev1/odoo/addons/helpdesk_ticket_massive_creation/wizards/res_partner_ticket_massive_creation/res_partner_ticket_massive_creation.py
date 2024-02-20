from odoo import api, fields, models


class HelpdeskTicketMassiveCreation(models.TransientModel):
    _name = "helpdesk.ticket.massive.creation.wizard"
    res_partner_ids = fields.Many2many("res.partner")

    name = fields.Char(string="Subject", required=True)
    category_id = fields.Many2one(
        comodel_name="helpdesk.ticket.category",
        string="Category",
    )
    team_id = fields.Many2one(
        comodel_name="helpdesk.ticket.team",
        string="Team",
        index=True,
    )
    user_ids = fields.Many2many(
        comodel_name="res.users", related="team_id.user_ids", string="Users"
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned user",
        tracking=True,
        index=True,
        domain="[('id', 'in', user_ids)]",
    )
    tag_ids = fields.Many2many(comodel_name="helpdesk.ticket.tag", string="Tags")
    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Medium"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        default="1",
    )
    description = fields.Html(required=True, sanitize_style=True)

    @api.multi
    def button_create(self):
        for partner in self.res_partner_ids:
            ticket_params = {
                "name": self.name,
                "partner_id": partner.id,
                "partner_name": partner.name,
                "parnter_email": partner.email,
                "category_id": self.category_id.id,
                "team_id": self.team_id.id,
                "user_id": self.user_id.id,
                "tag_ids": [(6, 0, self.tag_ids.ids)],
                "priority": self.priority,
                "description": self.description,
            }
            self.env["helpdesk.ticket"].create(ticket_params)
        return True

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["res_partner_ids"] = self.env.context["active_ids"]
        return defaults
