from abc import ABC
from .toForm import ToForm
from models.payment import Payment
from models.paymentType import PaymentType
from models.income import Income


class Income2Form(ToForm, ABC):
    def __init__(self, filename):
        super(Income2Form, self).__init__(filename)
        if not getattr(self, 'payment_end_col', 0):
            setattr(self, 'payment_end_col', self.get_payment_end_col())

    def get_payment_end_col(self):
        return self.sheet.ncols - 1

    def read_line(self, row):
        # 基本行数据载入
        basic_form = {
            'date': self.get_cell_value(getattr(self, 'date_row'), 0, t=str),
            'car': self.get_cell_value(row, getattr(self, 'car_col'), t=str),
            'route': self.get_cell_value(row, getattr(self, 'route_col'), t=str),
            'revenue': self.get_cell_value(row, getattr(self, 'revenue_col'), t=float),
            'cashier': self.get_cell_value(row, getattr(self, 'cashier_col'), t=str),
            'remnant_num': self.get_cell_value(row, getattr(self, 'remnant_col'), t=int),
            'remnant_value': self.get_cell_value(row, getattr(self, 'remnant_col') + 1, t=float),
            'fake_num': self.get_cell_value(row, getattr(self, 'fake_col'), t=int),
            'fake_value': self.get_cell_value(row, getattr(self, 'fake_col') + 1, t=float),
            'people_num_by_cash': self.get_cell_value(row, getattr(self, 'people_num_by_cash_col'), t=int),
            'people_num_by_cal': self.get_cell_value(row, getattr(self, 'people_num_by_cal_col'), t=int),
            'people_num_by_car': self.get_cell_value(row, getattr(self, 'people_num_by_car_col'), t=int),
        }
        # 把PaymentType和Payment关系建立起来并将这一行加入Income
        payment_type_row = getattr(self, 'payment_type_row')
        payment_start_col = getattr(self, 'payment_start_col')
        payment_end_col = getattr(self, 'payment_end_col')
        payment_type_name = self.get_cell_value(payment_type_row, payment_start_col, t=str)
        title_row = getattr(self, 'title_row')
        p_f = {}
        for col in range(payment_start_col, payment_end_col, 2):
            # 建立数据库关系
            name = self.get_cell_value(payment_type_row, col, t=str)
            if name:
                payment_type_name = self.strip_space(name)
            f = {'name': payment_type_name}
            PaymentType.update_or_new(f, name=payment_type_name)
            payment_name = self.strip_space(self.get_cell_value(title_row, col, t=str))
            if not payment_name:
                payment_name = payment_type_name + '@'
            if payment_name == '合计':
                payment_name = payment_type_name + payment_name
            f = {'name': payment_name, 'payment_type': payment_type_name}
            Payment.update_or_new(f, name=payment_name, payment_type=payment_type_name)

            # 载入这一行数据
            p_f[payment_name] = (self.get_cell_value(row, col, int), self.get_cell_value(row, col + 1, t=float))

        income_form = {**basic_form, **p_f}
        Income.update_or_new(income_form,
                             car=income_form.get('car'),
                             route=income_form.get('route'),
                             date=income_form.get('date'))


if __name__ == '__main__':
    a = Income2Form('../files/income_xls/test_income.xls')
    a.read_page()
