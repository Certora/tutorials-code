pragma solidity ^0.8.0;

/** Borda Election Overview
 * @dev This contract simulates a Borda election
 * (see https://en.wikipedia.org/wiki/Borda_count).
 * 
 * The election system follows the following rules:
 *
 * - Every user with an Etheruem address is allowed to vote in the election.
 * - A voter may vote to 3 distinct contenders at once. 
 * - The voter's 1st choice gets 3 points, their 2nd choice gets 2 points, and their 3rd
 *   choice gets 1 point.
 * - At any point in time there is a winner which can change due to new votes that bypass the current winner 

 */

interface IBorda {

    // current winner
    function winner() external view returns(address);

    // msg.sender votes first choice to f, second to s and third to t
    function vote(address f, address s, address t) external;

    // number of points the candidate has received
    function points(address c) external view returns(uint256);

    // has user x voted?
    function voted(address x) external view returns(bool);
}