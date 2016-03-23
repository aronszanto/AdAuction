#!/usr/bin/env python

import random

import logging

from gsp import GSP

class VCG:
    """
    Implements the Vickrey-Clarke-Groves mechanism for ad auctions.
    """
    @staticmethod
    def compute(slot_clicks, reserve, bids):
        """
        Given info about the setting (clicks for each slot, and reserve price),
        and bids (list of (id, bid) tuples), compute the following:
          allocation:  list of the occupant in each slot
              len(allocation) = min(len(bids), len(slot_clicks))
          per_click_payments: list of payments for each slot
              len(per_click_payments) = len(allocation)

        If any bids are below the reserve price, they are ignored.

        Returns a pair of lists (allocation, per_click_payments):
         - allocation is a list of the ids of the bidders in each slot
            (in order)
         - per_click_payments is the corresponding payments.
        """

        # The allocation is the same as GSP, so we filled that in for you...
        
        valid = lambda (a, bid): bid >= reserve
        valid_bids = filter(valid, bids)

        rev_cmp_bids = lambda (a1, b1), (a2, b2): cmp(b2, b1)
        # shuffle first to make sure we don't have any bias for lower or
        # higher ids
        random.shuffle(valid_bids)
        valid_bids.sort(rev_cmp_bids)

        num_slots = len(slot_clicks)
        allocated_bids = valid_bids[:num_slots]
        if len(allocated_bids) == 0:
            return ([], [])
        
        (allocation, just_bids) = zip(*allocated_bids)


        # TODO: You just have to implement this function
        def total_payment(k):
            """
            Total payment for a bidder in slot k.
            """
            c = slot_clicks # because slot_clicks looks like [[3, 2, 1]]
            n = len(allocation)

            # TODO: Compute the payment and return it.

            # if n < len(c):

            # slot k >= n not in the allocation, so pay nothing
            # This case should not happen though because per_click_payments call
            # total_payment(k) for k in range(len(allocation))
            if k >= n:
                return 0 
            # last slot in the allocation
            # t(bidder 3) = p3*max(r,b_4) = p3*r because r>b_4 per the example
            # pay p_k*max(reserve,next_highest_bid)
            elif k == n-1:
                maximum = valid_bids[n][1] if len(valid_bids) >= n else reserve
                return c[n-1]*maximum
            # k < n-1
            else:
                return (c[k]-c[k+1])*just_bids[k+1] + total_payment(k+1)


        def norm(totals):
            """Normalize total payments by the clicks in each slot"""
            return map(lambda (x,y): x/y, zip(totals, slot_clicks))

        per_click_payments = norm(
            [total_payment(k) for k in range(len(allocation))])
        
        return (list(allocation), per_click_payments)

    @staticmethod
    def bid_range_for_slot(slot, slot_clicks, reserve, bids):
        """
        Compute the range of bids that would result in the bidder ending up
        in slot, given that the other bidders submit bidders.
        Returns a tuple (min_bid, max_bid).
        If slot == 0, returns None for max_bid, since it's not well defined.
        """
        # Conveniently enough, bid ranges are the same for GSP and VCG:
        return GSP.bid_range_for_slot(slot, slot_clicks, reserve, bids)
