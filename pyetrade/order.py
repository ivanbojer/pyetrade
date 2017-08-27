#!/usr/bin/python3

'''Order - ETrade Order API
   TODO:
       * List Order
       * Preview Equity Order
       * Place equity order - test arg types
       * Preview equity order change
       * Place equity order change
       * Preview option order
       * Place option order
       * Preview option order change
       * Place option order change
       * Cancel Order'''

import logging
from requests_oauthlib import OAuth1Session
from pyetrade.etrade_exception import OrderException
# Set up logging
logger = logging.getLogger(__name__)

class ETradeOrder(object):
    '''ETradeOrder'''
    def __init__(self, client_key, client_secret,
                 resource_owner_key, resource_owner_secret):
        '''__init__(client_key, client_secret)
           param: client_key
           type: str
           description: etrade client key
           param: client_secret
           type: str
           description: etrade client secret
           param: resource_owner_key
           type: str
           description: OAuth authentication token key
           param: resource_owner_secret
           type: str
           description: OAuth authentication token secret'''
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.base_url_prod = r'https://etws.etrade.com'
        self.base_url_dev = r'https://etwssandbox.etrade.com'
        self.session = OAuth1Session(self.client_key,
                                     self.client_secret,
                                     self.resource_owner_key,
                                     self.resource_owner_secret,
                                     signature_type='AUTH_HEADER')

    def list_orders(self, account_id, dev=True,
                    resp_format='json', **kwargs):
        '''list_orders(dev, resp_format) -> resp
           param: account_id
           type: int
           required: true
           description: Numeric account ID
           param: marker
           type: str
           description: Specify the desired starting point of the set
                of items to return. Used for paging.
           param: count
           type: int
           description: The number of orders to return in a response.
                The default is 25. Used for paging.
           rdescription: see ETrade API docs'''
        # Set Env
        if dev:
            uri = r'order/sandbox/rest/orderlist'
            api_url = '%s/%s/%s.%s' % (
                    self.base_url_dev,
                    uri,
                    account_id,
                    resp_format
                )
        else:
            uri = r'order/rest/orderlist'
            api_url = '%s/%s/%s.%s' % (
                    self.base_url_prod,
                    uri,
                    account_id,
                    resp_format
                )

        # Build Payload
        payload = kwargs
        logger.debug('payload: %s', payload)

        logger.debug(api_url)
        req = self.session.get(api_url, params=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text

    def place_equity_order(self, dev=True, resp_format='json', **kwargs):
        '''place_equity_order(dev, resp_format, **kwargs) -> resp
           param: dev
           type: bool
           description: API enviornment
           param: resp_format
           type: str
           description: Response format JSON or None = XML
           kwargs:
           param: accountId
           type: int
           required: true
           description: Numeric account ID
           param: symbol
           type: str
           required: true
           description: The market symbol for the security
                        being bought or sold
           param: orderAction
           type: str
           required: true
           description: The action that the broker is requested
                        to perform Possible values are:
                            * BUY
                            * SELL
                            * BUY_TO_COVER
                            * SELL_SHORT
           param: previewid
           type: long
           required: conditional
           description: If the order was not previewed, this
                        parameter should not be specified. If
                        the order was previewed, this parameter
                        must specify the numeric preview ID from
                        the preview, and other parameters of
                        this request must match the parameters
                        of the preview
           param: clientOrderId
           type: str
           required: true
           description: A reference number generated by the
                        developer. Used to ensure that a
                        duplicate order is not being submitted.
                        It can be any value of 20 alphanmeric
                        characters or less, but must be unique
                        within this account. It does not appear
                        in any API responses.
           param: priceType
           type: str
           required: true
           description: The type of pricing specified in the
                        equity order. Possible values are:
                            * MARKET
                            * LIMIT
                            * STOP
                            * STOP_LIMIT
                            * MARKET_ON_CLOSE
                        If STOP, requires a stopPrice. If LIMIT,
                        requires a limitPrice. if STOP_LIMIT,
                        requires both. For more information
                        on these values, refer to the E-Trade
                        online help on conditional orders
           param: limitPrice
           type: double
           required: conditional
           description: The highest price at which to buy or
                        lowest price at which to sell. Required
                        if priceType is STOP or STOP_LIMIT.
           param: stopPrice
           type: double
           required: conditional
           description: The price at which to buy or sell if
                        specified in a stop order. Required if
                        priceType is STOP or STOP_LIMIT.
           param: allOrNone
           type: bool
           required: optional
           description: If TRUE, the transactions specified in
                        the order must be executed all at once
                        or not at all. Default is FALSE.
           param: quantity
           type: int
           required: true
           description: The number of shares to buy or sell
           param: reserveOrder
           type: bool
           required: optional
           description: If set to TRUE, publicly displays only
                        a limited number of shares (the
                        reserve quantity), instead of the
                        entire order, to avoid influencing
                        other traders. Default is FALSE. If
                        TRUE, must also specify the
                        reserveQuantity.
           param: reserveQuantity
           type: int
           required: conditional
           description: The number of shares to be publicly
                        displayed if this is a reserve order.
                        Required if serveOrder is True.
           param: marketSession
           type: str
           required: true
           description: Session in which the equity order will
                        be placed. Possible values are:
                            * REGULAR
                            * EXTENDED
           param: orderTerm
           type: str
           required: true
           description: Specifies the term for which the order
                        is in effect. Possible values are:
                            * GOOD_UNTIL_CANCEL
                            * GOOD_FOR_DAY
                            * IMMEDIATE_OR_CANCEL (only for
                              limit orders)
                            * FILL_OR_KILL (only for limit
                              orders)
           param: routingDestination
           type: str
           required: optional
           description: The exchange where the order should be
                        executed. Users may want to specify
                        this if they believe they can get a
                        better order fill at a specific exchange
                        rather than relying on automatic order
                        routing system. Posssible values are:
                            * AUTO (default)
                            * ARCA
                            * NSDQ
                            * NYSE
           rparam: accountId
           rtype: int
           rdescription: Numeric account ID
           rparam: allOrNone
           rtype: bool
           rdescription: if True, the transaction specified in
                         the order are to be executed all at
                         once, or not at all
           rparam: estimatedCommission
           rtype: double
           rdescription: The cost billed to the user to preform
                         the requested action
           rparam: estimatedTotalAmount
           rtype: double
           rdescription: The cost or proceeds, including broker
                         commission, resulting from the requested
                         action
           rparam: messageList
           rtype: dict
           rdescription: Container for messages describing the
                         result of the action
            - rparam: msgDesc
              rtype: str
              rdescription: Text of the result message,
                            indicating order status, success or
                            failure, additional requirements
                            that must be met before placing the
                            order, etc. Applications typically
                            display this message to the user,
                            which may result in further user
                            action
            - rparam: msgCode
              rtype: int
              rdescription: Standard numeric code of the result
                            message. Refer to the Error Messages
                            documentation for examples. May
                            optionally be displayed to the user,
                            but is primarily intended for
                            internal use.
           rparam: orderNum
           rtype: int
           rdescription: Numeric ID for this order in the E*TRADE
                         system
           rparam: orderTime
           rtype: long
           rdescription: The time the order was submitted, in
                         epoch time.
           rparam: symbolDesc
           rtype: str
           rdescription: Text description of the security
           rparam: symbol
           rtype: str
           rdescription: The market symbol for the underlier
           rparam: quantity
           rtype: int
           rdescription: The number of shares to buy or sell
           rparam: reserveOrder
           rtype: bool
           rdescription: If TRUE, this is a reserve order -
                         meaning that only a limited number
                         of shares will be publicly displayed,
                         instead of the entire order, to
                         avoid influencing other traders.
           rparam: orderTerm
           rtype: str
           rdescription: Specifies the term for which the
                         order is in effect. Possible values
                         are:
                             * GOOD_UNTIL_CANCEL
                             * GOOD_FOR_DAY
                             * IMMEDIATE_OR_CANCEL (only for
                                limit orders)
                             * FILL_OR_KILL (only for limit
                                orders)
           rparam: orderAction
           rtype: str
           rdescription: The action that the broker is requested
                         to perform. Possible values are:
                             * BUY
                             * SELL
                             * BUY_TO_COVER
                             * SELL_SHORT
           rparam: priceType
           rtype: str
           rdescription: The type of pricing. Possible values are:
                            * MARKET
                            * LIMIT
                            * STOP
                            * STOP_LIMIT
                            * MARKET_ON_CLOSE
           rparam: limitPrice
           rtype: double
           rdescription: The highest price at which to buy or the
                         lowest price at which to sell if specified
                         in a limit order. Returned if priceType is
                         LIMIT
           rparam: stopPrice
           rtype: double
           rdescription: The price at which a stock is to be bought
                         or sold if specified in a stop order.
                         Returned if priceType is STOP.
           rparam: routingDestination
           rtype: str
           rdescription: The exchange where the order should be
                         executed. Possible values are:
                             * AUTO
                             * ARCA
                             * NSDQ
                             * NYSE'''
        # Build Payload
        logger.debug(kwargs)
        # Test required values
        if 'accountId' not in kwargs and\
           'symbol' not in kwargs and\
           'orderAction' not in kwargs and\
           'clientOrderId' not in kwargs and\
           'priceType' not in kwargs and\
           'quantity' not in kwargs and\
           'orderTerm' not in kwargs and\
           'marketSession' not in kwargs:
            raise OrderException

        if kwargs['priceType'] == 'STOP' and \
           'stopPrice' not in kwargs:
            raise OrderException
        if kwargs['priceType'] == 'LIMIT' and \
           'limitPrice' not in kwargs:
            raise OrderException
        if kwargs['priceType'] == 'STOP_LIMIT' and \
           'limitPrice' not in kwargs and \
           'stopPrice' not in kwargs:
            raise OrderException

        # Init payload
        payload = {'PlaceEquityOrder': ''}

        # Set Env
        if dev:
            uri = r'order/sandbox/rest/placeequityorder'
            api_url = '%s/%s.%s' % (self.base_url_dev, uri, resp_format)
            payload['PlaceEquityOrder'] = {'-xmlns': self.base_url_dev}
            # Not sure if it matters
            #payload['PlaceEquityOrder'] = {'-xmlns': r'http://order.etws.etrade.com'}
        else:
            uri = r'order/rest/placeequityorder'
            api_url = '%s/%s.%s' % (self.base_url_prod, uri, resp_format)
            payload['PlaceEquityOrder'] = {'-xmlns': self.base_url_prod}

        # Build Payload
        payload['PlaceEquityOrder']['EquityOrderRequest'] = kwargs
        logger.debug('payload: %s', payload)

        logger.debug(api_url)
        req = self.session.post(api_url, json=payload)
        req.raise_for_status()
        logger.debug(req.text)

        if resp_format is 'json':
            return req.json()
        else:
            return req.text
