from unittest.mock import Mock, patch

from django.test import TestCase


class AlumniDirectoryViewTests(TestCase):
    def test_year_only_search_uses_passout_year_filter(self):
        response_data = Mock()
        response_data.data = [{"ktu_id": "123", "name": "Alice", "passout_year": "2024"}]

        fake_table = Mock()
        fake_table.select.return_value = fake_table
        fake_table.eq.return_value = fake_table
        fake_table.ilike.return_value = fake_table
        fake_table.execute.return_value = response_data

        with patch("core.views.supabase.table", return_value=fake_table):
            session = self.client.session
            session["admin_name"] = "admin"
            session.save()
            response = self.client.post(
                "/alumni-directory/",
                {"passout_year": "2024", "name": "", "ktu_id": ""},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["alumni"], response_data.data)
        self.assertTrue(
            any(
                call.args[0] == "passout_year" and call.args[1] == "2024"
                for call in fake_table.eq.call_args_list
            )
        )

    def test_name_only_search_uses_name_filter(self):
        response_data = Mock()
        response_data.data = [{"ktu_id": "123", "name": "Alice", "passout_year": "2024"}]

        fake_table = Mock()
        fake_table.select.return_value = fake_table
        fake_table.eq.return_value = fake_table
        fake_table.ilike.return_value = fake_table
        fake_table.execute.return_value = response_data

        with patch("core.views.supabase.table", return_value=fake_table):
            session = self.client.session
            session["admin_name"] = "admin"
            session.save()
            response = self.client.post(
                "/alumni-directory/",
                {"passout_year": "", "name": "Ali", "ktu_id": ""},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["alumni"], response_data.data)
        self.assertTrue(
            any(
                call.args[0] == "name" and call.args[1] == "%Ali%"
                for call in fake_table.ilike.call_args_list
            )
        )

    def test_ktu_id_only_search_uses_ktu_id_filter(self):
        response_data = Mock()
        response_data.data = [{"ktu_id": "123", "name": "Alice", "passout_year": "2024"}]

        fake_table = Mock()
        fake_table.select.return_value = fake_table
        fake_table.eq.return_value = fake_table
        fake_table.ilike.return_value = fake_table
        fake_table.execute.return_value = response_data

        with patch("core.views.supabase.table", return_value=fake_table):
            session = self.client.session
            session["admin_name"] = "admin"
            session.save()
            response = self.client.post(
                "/alumni-directory/",
                {"passout_year": "", "name": "", "ktu_id": "123"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["alumni"], response_data.data)
        self.assertTrue(
            any(
                call.args[0] == "ktu_id" and call.args[1] == "123"
                for call in fake_table.eq.call_args_list
            )
        )
