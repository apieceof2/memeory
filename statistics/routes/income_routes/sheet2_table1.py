from models.income import Income
from statistics.routes.router import Router


class IncomeSheet2Table1(Router):
    def __init__(self, table_name):
        super().__init__(table_name)
        self.DB = Income
        self.aggregation_key = 'cashier'

    def _aggregation_func(self, q):
        res = [getattr(q[0], 'cashier')]
        routes_msg = {}
        for item in q:
            route = getattr(item, 'route')
            if route in routes_msg:
                routes_msg[route][0] += 1
                routes_msg[route][1] += item.income_sum()
            else:
                routes_msg[route] = [1, item.income_sum()]
        routes_list = ['1路', '2路', '3路', '4路', '5路', '6路', '7路', '8路', '9路',
                       'K3路', 'K9路', 'K10路', '布尔陶亥', '苗家滩']
        for route in routes_list:
            if route in routes_msg:
                res.append(routes_msg[route][0])
                res.append(routes_msg[route][1])
            else:
                res.append(0)
                res.append(0)
        return res

    def test(self):
        a = Income.aggregate(self._aggregation_func, 'cashier')



if __name__ == '__main__':
    a =IncomeSheet2Table1('sheet2_table1')
    a.test()
