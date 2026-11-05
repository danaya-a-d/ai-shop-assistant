from knowledge import SHOP_FACTS, RETURN_PERIOD_DAYS


# разрешенные ответы основанные на регламенте магазина
SAFE_RESPONSES = {
    "product": SHOP_FACTS["product"],

    "delivery": SHOP_FACTS["delivery"],

    "order": (
        "К сожалению, я не могу проверить "
        "текущий статус конкретного заказа."
    ),

    "return": (
        SHOP_FACTS["opened_return"] + " "
        + SHOP_FACTS["return"]
    ),

    "defect": SHOP_FACTS["defect"],

    "discount": (
        "К сожалению, " + SHOP_FACTS["discount"].lower()
    ),

    "delivery_price": (
        "К сожалению, у меня нет информации "
        "о стоимости доставки."
    ),

    "payment_methods": (
        "К сожалению, у меня нет информации "
        "о доступных способах оплаты."
    ),

    "order_payment": (
        "К сожалению, я не могу проверить, "
        "оплачен ли конкретный заказ."
    ),

    "other_models": (
        "У меня нет информации о других моделях. "
        "Могу рассказать об известном товаре: "
        + SHOP_FACTS["product"]
    ),

    "product_change": (
        "Я не могу изменять сведения о товарах. "
        + SHOP_FACTS["product"]
    ),
}

FALLBACK_RESPONSE = (
    "К сожалению, у меня нет информации по этому вопросу. "
    "Я могу помочь с вопросами о наушниках X1, "
    "доставке и возврате."
)

ORDER_FIELDS = {
    "order": "статус",
    "order_payment": "оплату",
}


# функция для естественного перечисления:
def join_items(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]

    return ", ".join(items[:-1]) + " и " + items[-1]


# функция для обработки возвратов
def build_return_answer(
    day: int | None,
    condition: str
) -> str:

    # если товар неисправен действует порядок экспертизы
    if condition == "defective":
        return SHOP_FACTS["defect"]

    # если день неизвестен сообщаем общие условия
    if day is None or day < 1:
        return SAFE_RESPONSES["return"]

    # в пределах срока обычного возврата
    if day <= RETURN_PERIOD_DAYS:
        return (
            f"Если товар без брака, на {day}-й день "
            "его можно вернуть, даже если упаковка вскрыта. "
            + SHOP_FACTS["return"]
        )

    # срок обычного возврата истек
    return (
        f"На {day}-й день срок возврата товара "
        f"без брака ({RETURN_PERIOD_DAYS} дней) "
        "уже истёк. Если товар неисправен, "
        "он принимается на экспертизу. "
        "Возврат денег до её результатов "
        "не гарантируется."
    )


def build_safe_answer(
    topics: list[str],
    return_day: int | None = None,
    product_condition: str = "unknown"
) -> str:
    # оставляем только допустимые категории без повторений
    valid_topics = list(dict.fromkeys(
        topic for topic in topics
        if topic in SAFE_RESPONSES
    ))

    answers = []

    # объединяем сведения о конкретном заказе
    order_fields = [
        field
        for topic, field in ORDER_FIELDS.items()
        if topic in valid_topics
    ]

    if order_fields:
        fields = join_items(order_fields)

        answers.append(
            f"К сожалению, я не могу проверить "
            f"{fields} конкретного заказа."
        )

    # остальные категории обрабатываем отдельно
    other_topics = [
        topic for topic in valid_topics
        if topic not in ORDER_FIELDS
    ]

    for topic in other_topics:
        if topic == "return":
            answer = build_return_answer(
                return_day,
                product_condition
            )
        else:
            answer = SAFE_RESPONSES[topic]

        if answer not in answers:
            answers.append(answer)

    return "\n\n".join(answers) if answers else FALLBACK_RESPONSE


if __name__ == "__main__":
    print(build_safe_answer(["order"]))
    print("---")
    print(build_safe_answer(["defect"]))
    print("---")
    print(build_safe_answer(["discount"]))
