pragma solidity ^0.8.0;
import "./IBorda.sol";

contract BordaNewBug is IBorda {
    // The current winner
    address public _winner;

    // A map storing whether an address has already voted. Initialized to false.
    mapping(address => bool) _voted;

    // Points each candidate has recieved, initialized to zero.
    mapping(address => uint256) _points;

    // current maximum points of all candidates.
    uint256 public pointsOfWinner;

    address public previousWinner;

    function vote(
        address f,
        address s,
        address t
    ) public override {
        require(!_voted[msg.sender], "this voter has already cast its vote");
        require(f != s && f != t && s != t, "candidates are not different");
        _voted[msg.sender] = true;
        voteTo(f, 3);
        voteTo(s, 2);
        voteTo(t, 1);
    }

    function voteTo(address c, uint256 p) private {
        //update points
        _points[c] = _points[c] + p;
        // update winner if needed
        if (_points[c] > _points[_winner]) {
            _winner = c;
            //updating the points of winner
            pointsOfWinner = _points[_winner];
        }
    }

    //adding backdoor to change pointsofwinner
    function changePointsOfWinner(uint256 amt) external {
        pointsOfWinner = amt;
    }

    function winner() external view override returns (address) {
        return _winner;
    }

    function points(address c) public view override returns (uint256) {
        return _points[c];
    }

    function voted(address x) public view override returns (bool) {
        return _voted[x];
    }

    function getWinnerPoints() public view returns (uint256) {
        return pointsOfWinner;
    }
}
