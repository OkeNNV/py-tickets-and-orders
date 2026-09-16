from django.db import transaction

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order,
        )

    return order


def get_orders(username: str = None) -> list[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
