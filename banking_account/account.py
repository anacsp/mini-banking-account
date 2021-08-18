import transaction

class Account():

    db_dict = {}

    """ event functions """

    def set_account_balance(self, transaction):
        retval = None
        json_response = None
        if "deposit" == transaction.type:
            retval = self.verify_deposit(transaction)
        elif "withdraw" == transaction.type:
            retval = self.verify_withdraw(transaction)
        elif "transfer" == transaction.type:
            retval = self.verify_transfer(transaction)

        return retval
    
    def verify_deposit(self, deposit):
        status = False
        if deposit.destination is not None:
            id = deposit.destination
            status = True
            if id in self.db_dict:
                self.db_dict[id] = self.db_dict.get(id) + deposit.amount
            else:
                self.db_dict[id] = deposit.amount
            response = transaction.Transaction_response(
                    destination={'id': id, 'balance': self.db_dict.get(id)})
        return response.dict(exclude_none=True) if status is True else None

    def verify_withdraw(self, withdraw):
        status = False
        if withdraw.origin is not None:
            id = withdraw.origin
            if id in self.db_dict:
                status = True
                self.db_dict[id] = self.db_dict.get(id) - withdraw.amount
                response = transaction.Transaction_response(
                        origin={'id': id, 'balance': self.db_dict.get(id)})
        return response.dict(exclude_none=True) if status is True else None

    def verify_transfer(self, transfer):
        status  = False
        withdraw_status = self.verify_withdraw(transfer)
        if withdraw_status is not None:
            status = True
            self.verify_deposit(transfer)
            response = transaction.Transaction_response(
                    origin={'id': transfer.origin, 
                    'balance': self.db_dict.get(transfer.origin)},
                    destination={'id': transfer.destination, 
                    'balance': self.db_dict.get(transfer.destination)})
        return response if status is True else None

    """ balance functions """

    def get_balance(self, id):
        balance = None
        if id in self.db_dict:
            balance = self.db_dict.get(id)
        return balance

    """ reset functions """
    
    def clear_database(self):
        self.db_dict.clear()

account_controller = Account()
