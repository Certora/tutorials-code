/**
 * # English auction spec - proving strict inequality
 */
methods
{
    // Declaring getters as `envfree`
    function highestBidder() external returns (address) envfree;
    function highestBid() external returns (uint) envfree;
    function bids(address) external returns (uint) envfree;
}


/** @title A ghost and hook identifying if any bid was placed
 *  There is no other way to detect if a bid was placed *unless we assume that
 *  `address(0)` cannot place a bid).
 */
ghost bool _hasAnyoneBid {
    init_state axiom !_hasAnyoneBid;
}

hook Sstore bids[KEY address bidder] uint newAmount (uint oldAmount) {
    _hasAnyoneBid = _hasAnyoneBid || (newAmount > 0);
}


/// @title `highestBid` is the maximal bid
invariant integrityOfHighestBid(address bidder)
    bids(bidder) <= highestBid();


/// @title No bids implies all bids are zero and highest bidder is address zero
invariant noBidsIntegrity(address bidder)
    !_hasAnyoneBid => (bids(bidder) == 0 && highestBidder() == 0);


/// @title There can be no tie in highest bid (if there is at least one bid)
invariant highestBidStrictlyHighest(address bidder)
    (_hasAnyoneBid && bidder != highestBidder()) => (highestBid() > bids(bidder)) {
        preserved {
            requireInvariant integrityOfHighestBid(bidder);
        }
        preserved withdrawFor(address bidder2, uint amount) with (env e1) {
            requireInvariant noBidsIntegrity(bidder2);
        }
        preserved withdrawAmount(address recipient, uint amount) with (env e2) {
            requireInvariant noBidsIntegrity(e2.msg.sender);
        }
    }


// -----------------------------------------------------------------------------
// Here is the invariant "highest bidder has the highest bid" without assuming that
// `address(0)` cannot place a bid.

/// @title Highest bidder has the highest bid
invariant highestBidderHasHighestBid()
    _hasAnyoneBid => (bids(highestBidder()) == highestBid()) {
        preserved withdrawFor(address bidder, uint amount) with (env e1) {
            requireInvariant noBidsIntegrity(bidder);
        }
        preserved withdrawAmount(address recipient, uint amount) with (env e2) {
            requireInvariant noBidsIntegrity(e2.msg.sender);
        }
    }
