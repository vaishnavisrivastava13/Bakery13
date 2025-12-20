from django import forms

PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('upi', 'UPI'),
    ('cod', 'Cash on Delivery'),
]

class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        label="Select Payment Method"
    )
