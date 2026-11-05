import unittest

from response_policy import build_safe_answer


class TestResponsePolicy(unittest.TestCase):

    def test_product_price(self):
        answer = build_safe_answer(["product"])

        self.assertIn("2490", answer)
        self.assertIn("X1", answer)

    def test_unknown_order(self):
        answer = build_safe_answer(["order"])

        self.assertIn("не могу проверить", answer)

    def test_order_and_payment(self):
        answer = build_safe_answer(["order", "order_payment"])

        self.assertIn("статус и оплату", answer)
        self.assertEqual(answer.count("К сожалению"), 1)

    def test_return_within_period(self):
        answer = build_safe_answer(
            ["return"],
            return_day=7,
            product_condition="not_defective"
        )

        self.assertIn("можно вернуть", answer)

    def test_return_after_period(self):
        answer = build_safe_answer(
            ["return"],
            return_day=16,
            product_condition="unknown"
        )

        self.assertIn("истёк", answer)
        self.assertIn("экспертизу", answer)

    def test_defective_product(self):
        answer = build_safe_answer(
            ["defect", "return"],
            return_day=16,
            product_condition="defective"
        )

        self.assertIn("экспертизу", answer)
        self.assertEqual(answer.count("экспертизу"), 1)

    def test_discount(self):
        answer = build_safe_answer(["discount"])

        self.assertIn("не предоставляются", answer)

    def test_unknown_category(self):
        answer = build_safe_answer(["unknown_topic"])

        self.assertIn("нет информации", answer)

    def test_duplicate_categories(self):
        answer = build_safe_answer(["product", "product"])

        self.assertEqual(answer.count("2490"), 1)


if __name__ == "__main__":
    unittest.main()
