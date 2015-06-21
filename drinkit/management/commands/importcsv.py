from django.core.management.base import BaseCommand, CommandError
from drinkit.models import Drinker, Transaction
import csv
from decimal import Decimal
import datetime
import re

class Command(BaseCommand):
    help = 'Imports the data from the CSV file'

    re_new = re.compile(r'neu', re.IGNORECASE)
    re_new_with_date = re.compile(r'neu \((\d+\.\d+\.\d+)\)', re.IGNORECASE)
    re_paid = re.compile(r'bezahlt', re.IGNORECASE)

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=open)

    @staticmethod
    def _parse_amount(amount):
        amount = amount.strip('€').strip()
        if amount:
            return Decimal(amount.strip('€').strip())
        else:
            return Decimal(0)

    @staticmethod
    def _parse_date(datestring):
        try:
            date = datetime.datetime.strptime(datestring, '%d.%m.%y').date()
            return date
        except ValueError:
            return None

    def handle(self, *args, **options):
        reader = csv.reader(options['csvfile'])
        headers = next(iter(reader))

        for line in reader:
            # Skip people with zero balance
            if not self._parse_amount(line[-1]):
                continue

            drinker = Drinker(
                firstname = line[0].strip(),
                lastname = line[1].strip(),
                email = line[2].strip(),
            )
            drinker.save()
            print(drinker)

            # Initial amount
            initial = self._parse_amount(line[5])
            if initial:
                date = self._parse_date(headers[5])
                transaction = Transaction(
                    drinker=drinker,
                    date=date,
                    amount=-initial,
                    comment='Import: Initial balance',
                )
                transaction.save()
                print(transaction)

            new = None
            paid = None
            for header, item in zip(headers[6:], line[6:]):
                date = self._parse_date(header)
                if date:
                    if paid:
                        transaction = Transaction(
                            drinker=drinker,
                            date=date,
                            amount=paid,
                            comment='Import: Paid',
                        )
                        transaction.save()
                        print(transaction)
                        paid = None
                    if new:
                        transaction = Transaction(
                            drinker=drinker,
                            date=date,
                            amount=-new,
                            comment='Import: New',
                        )
                        transaction.save()
                        print(transaction)
                        new = None
                    continue

                if self.re_new.fullmatch(header):
                    new = self._parse_amount(item)
                    continue

                if self.re_paid.fullmatch(header):
                    paid = self._parse_amount(item)
                    continue

                amount = self._parse_amount(item)
                if not amount:
                    continue

                match = self.re_new_with_date.fullmatch(header)
                if match:
                    transaction = Transaction(
                        drinker=drinker,
                        date=self._parse_date(match.group(1)),
                        amount=-amount,
                        comment='Import: {}'.format(header),
                    )
                    transaction.save()
                    print(transaction)
                    continue

                # Was not able to match column type
                raise ValueError('Unknown column label: {}'.format(header))

            assert drinker.balance == -self._parse_amount(line[-1])
