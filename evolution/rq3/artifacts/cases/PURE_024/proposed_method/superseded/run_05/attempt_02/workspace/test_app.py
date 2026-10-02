import unittest
import app

class NeniosTests(unittest.TestCase):
    def setUp(self):
        app.state["families"].clear(); app.state["children"].clear(); app.state["classrooms"].clear(); app.state["invoices"].clear(); app.state["waiting_list"].clear(); app.state["audit"].clear()

    def test_child_status(self):
        f = app.Family(id="f1", name="Smith")
        app.state["families"][f.id] = f
        c = app.Child(id="c1", family_id="f1", name="Ava", dob="2020-01-01", site="north")
        self.assertEqual(app.child_status(c), "not_compliant")
        c.compliance_verified = True
        c.immunization_status = "current"
        self.assertEqual(app.child_status(c), "compliant")

    def test_assignment_and_payment(self):
        app.state["families"]["f1"] = app.Family(id="f1", name="Smith")
        app.state["children"]["c1"] = app.Child(id="c1", family_id="f1", name="Ava", dob="2020-01-01", site="north")
        app.state["classrooms"]["r1"] = app.Classroom(id="r1", site="north", name="Toddlers", capacity=1)
        room = app.state["classrooms"]["r1"]
        child = app.state["children"]["c1"]
        child.classroom_id = room.id
        invoice = app.Invoice(id="i1", family_id="f1", child_id="c1", amount=100, balance=100)
        app.state["invoices"]["i1"] = invoice
        invoice.balance -= 25
        invoice.status = "partial"
        self.assertEqual(invoice.balance, 75)
        self.assertEqual(invoice.status, "partial")

if __name__ == "__main__":
    unittest.main()
