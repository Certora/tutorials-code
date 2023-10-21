
interface IERC20 {
    function transfer(address recipient, uint256 amount)
        external
        returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool);
}


interface IOracle {

    // returns the price of one tokenTo in WAD precision 
    function getPrice(
        IERC20 tokenFrom,
        IERC20 tokenTo
    ) external returns (uint256);
}


contract Swapper {

    uint constant WAD = 10 ** 18;
    IOracle oracle;

    
    function swap(IERC20 tokenFrom, IERC20 tokenTo, uint256 amountFrom) external returns (uint256 amountTo) {
        uint256 price = oracle.getPrice(tokenFrom, tokenTo);
        require (price != 0);
        amountTo = amountFrom * price / WAD;
        tokenFrom.transferFrom(msg.sender, address(this), amountFrom);
        tokenTo.transfer(msg.sender, amountTo);        
    }
}