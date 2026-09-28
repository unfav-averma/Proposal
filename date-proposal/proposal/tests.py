import json

from django.test import TestCase
from django.urls import reverse

from .models import ProposalResponse


class ProposalFlowTests(TestCase):

    def start_proposal(self):
        return self.client.post(reverse("start_proposal"))

    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="yesBtn"')
        self.assertNotContains(response, "onclick=")

    def test_proposal_pages_require_previous_steps(self):
        response = self.client.get(reverse("date_page"))

        self.assertRedirects(
            response,
            reverse("home")
        )

        response = self.client.get(reverse("select_date"))

        self.assertRedirects(
            response,
            reverse("date_page"),
            fetch_redirect_response=False
        )

    def test_complete_proposal_flow(self):
        start_response = self.start_proposal()

        self.assertEqual(start_response.status_code, 200)

        self.assertJSONEqual(
            start_response.content,
            {"success": True}
        )

        date_type_response = self.client.post(
            reverse("save_date_type"),
            data=json.dumps({
                "date_type": "Movie Date"
            }),
            content_type="application/json"
        )

        self.assertEqual(
            date_type_response.status_code,
            200
        )
        select_date_response = self.client.get(
            reverse("select_date")
        )

        self.assertEqual(
            select_date_response.status_code,
            200
        )

        selection_response = self.client.post(
            reverse("save_selection"),
            data=json.dumps({
                "selected_date": "2026-10-10",
                "selected_time": "6:00 PM"
            }),
            content_type="application/json"
        )

        self.assertEqual(
            selection_response.status_code,
            200
        )

        self.assertEqual(
            ProposalResponse.objects.count(),
            1
        )

        thank_you_response = self.client.get(
            reverse("thank_you")
        )

        self.assertEqual(
            thank_you_response.status_code,
            200
        )

    def test_invalid_selection_does_not_create_response(self):
        self.start_proposal()

        self.client.post(
            reverse("save_date_type"),
            data=json.dumps({
                "date_type": "Coffee Date"
            }),
            content_type="application/json"
        )

        response = self.client.post(
            reverse("save_selection"),
            data=json.dumps({
                "selected_date": "not-a-date"
            }),
            content_type="application/json"
        )

        self.assertEqual(
            response.status_code,
            400
        )

        self.assertEqual(
            ProposalResponse.objects.count(),
            0
        )
