from odoo.tests import common


class TestResPartnerTicketMassiveCreationWizard(common.SavepointCase):
    def test_massive_helpdesk_ticket_create(self):
        partner_1 = self.env.ref("base.res_partner_1")
        partner_2 = self.env.ref("base.res_partner_2")
        partner_ids = [partner_1.id, partner_2.id]
        ticket_domain = [
            ("partner_id", "in", partner_ids),
            ("name", "=", "Massive incident"),
        ]
        partners_tickets = self.env["helpdesk.ticket"].search(ticket_domain)

        self.assertFalse(partners_tickets)

        wizard = (
            self.env["helpdesk.ticket.massive.creation.wizard"]
            .with_context(active_ids=partner_ids)
            .create(
                {
                    "name": "Massive incident",
                    "category_id": self.env.ref("helpdesk_mgmt.helpdesk_category_3").id,
                    "team_id": self.env.ref("helpdesk_mgmt.helpdesk_team_1").id,
                    "user_id": self.env.ref("base.user_demo").id,
                    "tag_ids": [(4, self.env.ref("helpdesk_mgmt.helpdesk_tag_1").id)],
                    "priority": "2",
                    "description": "Massive issue going on",
                }
            )
        )
        wizard.button_create()

        partners_tickets = self.env["helpdesk.ticket"].search(ticket_domain)

        self.assertTrue(partners_tickets)
        self.assertEquals(len(partners_tickets), 2)

        ticket = partners_tickets[0]
        self.assertEqual(ticket.name, wizard.name)
        self.assertEqual(ticket.category_id, wizard.category_id)
        self.assertEqual(ticket.team_id, wizard.team_id)
        self.assertEqual(ticket.tag_ids, wizard.tag_ids)
        self.assertEqual(ticket.priority, wizard.priority)
        self.assertEqual(ticket.description, wizard.description)
