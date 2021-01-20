from .decorator import update_route
from models.income import Income
from .route import Route
from models.payment import Payment


@update_route('IncomeSta_线路营收及人次报表')
class IncomeSheet1(Route):
    def __init__(self):
        self.data = {
            'vars': {
                'duration': '2012'
            },
            'data': []
        }
        self.DB = Income
        self.aggregation_key = 'route'
        self.is_aggregate = True

    @staticmethod
    def _sum_by_payment_type(q, payment_type_name):
        """
        统计某一个记录集合中某一个payment_type的人次, 金额
        :param q: model的list
        :param payment_type_name: payment_type的name
        :return: (num, value)
        """
        num = 0
        value = 0.0
        payments = Payment.find_by(payment_type=payment_type_name)
        for payment in payments:
            if payment.name == payment.payment_type+'合计':
                continue
            for i in q:
                temp = getattr(i, payment.name)
                if temp[0]:
                    num += temp[0]
                if temp[1]:
                    value += temp[1]
        res = (num, value)
        return res

    def _aggregation_func(self, q):
        """
        :param q:
        :type q: models.Income
        :return:
        """
        # res: 线路, 线路车辆数, 营收现金人次, 营收现金金额, 实体卡人次,
        # 实体卡金额, 银联人次, 银联金额, 总人次, 总营收

        # 好算的基本数据
        res = [
            q[0].route, # lm
            len(q),
            self.sum_by_key(q, 'people_num_by_cash', int),
            self.sum_by_key(q, 'revenue', float),
        ]

        # payment_type合计
        card1 = self._sum_by_payment_type(q, '实体卡（IC卡）')
        card2 = self._sum_by_payment_type(q, '银联+天交通二维码')
        res.append(card1[0])
        res.append(card1[1])
        res.append(card2[0])
        res.append(card2[1])

        # 总合计
        all_num = res[2] + res[4] + res[6]
        all_value = res[3] + res[5] + res[7]
        res.append(all_num)
        res.append(all_value)

        return res


@update_route("IncomeSta_营收及人次汇总报表")
class IncomeStaSheet2(Route):
    def __init__(self):
        self.data = {
            'vars': {
                'duration': '2012'
            },
            'data': [
            ]
        }
        self.DB = Income
        self.aggregation_key = 'route'
        self.is_aggregate = False

    def _get_tri_data(self, q):
        from models.income import Income
        data = [
            (0, 2, 'haha'),
        ]
        return data