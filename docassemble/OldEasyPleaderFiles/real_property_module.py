__all__ = ['RealProperty']

from docassemble.base.util import DAObject, Individual, Address, DAList
from datetime import datetime, timedelta
import requests

class Occupancy(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.occupant_type = None
        self.monthly_rent = None
        self.occupant_name = None

class Lease(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.lease_name = None
        self.execution_date = None
        self.rental_deposit = None

class Unit(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.unit_number = None
        self.occupancy = Occupancy()
        self.lease = Lease()

class Structure(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.bedrooms = None
        self.bathrooms = None
        self.square_footage = None
        self.build_year = None
        self.stories_above_ground = None
        self.stories_below_ground = None
        self.basement_finish = None
        self.property_type = None
        self.residence_type = None
        self.number_of_units = None
        self.units = DAList()

class Parking(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.garage = None
        self.carport = None
        self.driveway = None
        self.on_street = None

class Title(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.instrument_name = None
        self.book_page_number = None
        self.date_recorded = None
        self.grantor = Individual()
        self.sale_price = None

class Owner(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.individual = Individual()
        self.ownership_interest = None
        self.title = Title()

class RecurringExpenses(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.electricity = None
        self.gas = None
        self.water = None
        self.sewer = None
        self.security = None
        self.garbage_recycling = None
        self.landscaping = None
        self.other = None
        self.hoa_fees = None

class Financial(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.petitioner_attorney_fees_claim = None
        self.city_code_enforcement_fees = None

class RealProperty(DAObject):
    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.fair_market_value = None
        self.assessors_parcel_number = None
        self.lot_size = None
        self.structures = DAList()
        self.owners = DAList()
        self.parking = Parking()
        self.zoning = None
        self.street_address = Address()
        self.legal_description = None
        self.site_county = None
        self.recurring_expenses = RecurringExpenses()
        self.financial = Financial()

    def fetch_interest_rate(self, index, date):
        if index == 'FRED':
            date_str = date.strftime('%Y-%m-%d')
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=MORTGAGE30US&api_key=your_api_key&file_type=json&observation_start={date_str}&observation_end={date_str}"
            response = requests.get(url)
            data = response.json()
            rate = float(data['observations'][0]['value'])
            return rate
        elif index == 'Other_Index':
            pass

    def calculate_accrued_interest(self, principal, rate, start_date):
        today = datetime.today().date()
        time_elapsed = (today - start_date).days / 365.25
        accrued_interest = principal * rate * time_elapsed
        return accrued_interest

    def calculate_equity(self, custom_rate=None):
        total_lien_amount = 0
        for encumbrance in self.encumbrances:
            if isinstance(encumbrance, MonetaryLien):
                rate_date = encumbrance.date_recorded - timedelta(days=7)
                rate = custom_rate if custom_rate else self.fetch_interest_rate(encumbrance.interest_rate_index, rate_date)
                lien_amount = encumbrance.principal_amount + self.calculate_accrued_interest(encumbrance.principal_amount, rate, encumbrance.date_recorded)
                total_lien_amount += lien_amount
        total_payments_made = sum(encumbrance.regular_payments for encumbrance in self.encumbrances if isinstance(encumbrance, MonetaryLien))
        estimated_equity = self.fair_market_value - total_lien_amount - total_payments_made
        return estimated_equity