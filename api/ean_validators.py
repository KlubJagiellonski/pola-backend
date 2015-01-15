__author__ = 'paweljaneczek'

class EAN13Validator:
    @classmethod
    def validate(cls, barcode):
        checksum = int(barcode[-1:])
        data = barcode[:12]

        sum = 0

        for position in range(len(data) - 1, 0, -1):
            number = data[position]
            if number % 2 == 0:
                sum += number
            else:
                sum += 3 * number

        valid_checksum = (10 - (sum % 10)) % 10
        return valid_checksum == checksum