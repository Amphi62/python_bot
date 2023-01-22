from entity.platform.Platform import Platform


class InstantGamingPlatform(Platform):
    def __init__(self, link, default_price, reduction_price=None, in_stock=True):
        super().__init__(link, default_price, reduction_price, in_stock)

    def __str__(self):
        return "InstantGaming : {}\nPrix : {}\nRéduction : {}\nStock : {}".format(
            self.link,
            self.default_price,
            self.reduction_price,
            self.stock
        )
