/*--------------------------------- Crypto ICO---------------------------------------------------------------------*/

/*
    About this program:
    
    This is about generating WumboCoins and keeping a tab of its rate and how many of them
    have been bought by investors.
*/

pragma solidity ^0.4.11; //Version Compiler


//create a contract
contract wumbocoin_ico{
    
  uint public no_of_wc_issued = 1000000;  // No. of WumboCoins available for sale
  
  // WC to USD rate
  uint public usd_to_wc_rate = 100; //$1 = 100 wbc
  
  //WumboCoins bought by investors
  
  uint public wc_purchased =0; //Starts with 0
  
  /*Mapping to investor's address to its equity in wc and USD*/
  
  //Creating mapping address variables that display equity in WumboCoin as well as USD
  mapping(address => uint)equity_wumbo_coin; 
  mapping(address => uint)equity_usd;  
  
  /*Modifier - CHecks if an investor can add or sell cryptos*/
  
  modifier can_buy_wc(uint usd_spent){
      require(usd_spent * usd_to_wc_rate + wc_purchased <=no_of_wc_issued);
      _; //If the condition is true
  }
  
  /*Equity in wbc of investors*/
  
  // Function accepting address of the investor as the parameter
  function equity_wbc(address investor) external constant returns (uint){
      return equity_wumbo_coin[investor];
  }
  
  /*Equity in USD of investors*/
  function equity_ret_usd(address investor) external constant returns (uint){
      return equity_usd[investor];
  }
    
  /* Purchasing WC */
  
  //Address of the investor, amount of dollars spent to buy WumboCoins (reason why uint is taken cause it has a limit)
  //A modifier is added in the end to check if the investor can buy coins using the money.
  function buy_wc(address investor, uint usd_spent) external
  can_buy_wc(usd_spent){
      uint wc_bought = usd_spent * usd_to_wc_rate; //no. of wc purchased ($1=100 wc)
      equity_wumbo_coin[investor] +=wc_bought; //add no of wc_bought to total wc of an investor
      equity_usd[investor] = equity_wumbo_coin[investor]/usd_to_wc_rate; //convert it into usd
      
      //Number of wc bought from a total pool of 1 mil wc
      wc_purchased +=wc_bought; 
  }
  
  /*Selling WC*/
  
  function sell_wc(address investor, uint wc_sold) external {
      equity_wumbo_coin[investor] -= wc_sold; //Decreases wc possessed by an investor
      equity_usd[investor] = equity_wumbo_coin[investor]/100; // Converting wc to dollars
      wc_purchased -=wc_sold; // Decrease Number of wc purchased
  }
  
}

