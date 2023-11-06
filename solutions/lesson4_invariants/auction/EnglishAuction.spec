/**
 * # English auction spec - invariants example
 */
methods
{
    // Declaring getters as `envfree`
    function highestBidder() external returns (address) envfree;
    function highestBid() external returns (uint) envfree;
    function bids(address) external returns (uint) envfree;
}


/// @title `highestBid` is the maximal bid
invariant integrityOfHighestBid(address bidder)
    bids(bidder) <= highestBid();


/// @title Highest bidder has the highest bid
invariant highestBidderHasHighestBid()
    (highestBidder() != 0) => (bids(highestBidder()) == highestBid());
