from odoo.tests import common
from odoo.exceptions import ValidationError


class TestHelpdeskTicket(common.SavepointCase):
    def setUp(self):
        self.partner = self.env.ref("base.res_partner_1")
        self.user = self.env.ref("base.user_admin")
        self.contract = self.env["contract.contract"].create(
            {
                "name": "Test Contract",
                "partner_id": self.partner.id,
            }
        )
        common.SavepointCase.setUp(self)

    def test_create_with_contract_without_partner(self):
        ticket_data = {
            "name": "New Ticket",
            "description": "Description",
            "user_id": self.user.id,
            "contract_id": self.contract.id,
        }
        new_ticket = self.env["helpdesk.ticket"].create(ticket_data)

        self.assertTrue(new_ticket.partner_id, self.contract.partner_id.id)

    def test_create_with_contract_with_different_partner(self):
        ticket_data = {
            "name": "New Ticket",
            "description": "Description",
            "user_id": self.user.id,
            "contract_id": self.contract.id,
            "partner_id": self.env.ref("base.res_partner_2").id,
        }

        self.assertRaisesRegex(
            ValidationError,
            "Cannot create ticket with contract {}".format(self.contract.id),
            self.env["helpdesk.ticket"].create,
            ticket_data,
        )
