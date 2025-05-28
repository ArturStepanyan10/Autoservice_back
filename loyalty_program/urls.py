from django.urls import path

from loyalty_program.views import LoyaltyProfileDetail, BonusTransactionList, AddBonusPoints

urlpatterns = [
    path('loyalty/profile/', LoyaltyProfileDetail.as_view(), name='loyalty-profile'),
    path('loyalty/history/', BonusTransactionList.as_view(), name='bonus-history'),
    path('loyalty/add/', AddBonusPoints.as_view(), name='add-bonus'),
    path('loyalty/deduction/', AddBonusPoints.as_view(), name='add-bonus'),
]
