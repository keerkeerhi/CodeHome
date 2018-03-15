// 获取合约主体
export const getBC = function (abi, address) {
  return web3.eth.contract(abi).at(address);
}
/*
* 购买菠萝章
* bc       主合同对象:BOLOZERO_sale或者BOLOX_sale
* boloID        菠萝章ID
* value         创建时传入金额，value需要调用web3.toWei转换成wei的单位
* */
export const bidBolo = function (bc, boloID, value, my_wallet, sucBack ,failBack, completeBack) {
  var tx = bc.bid(
    boloID,
    {value: value, from: my_wallet, gas: 120000},
    function (err, myContract) {
      if(!err) {
        // NOTE: The callback will fire twice!
        // Once the contract has the transactionHash property set and once its deployed on an address.
        sucBack(myContract.transactionHash)
        // e.g. check tx hash on the first call (transaction send)
        // if(!myContract.address) {
        //   console.log(myContract.transactionHash) // The hash of the transaction, which deploys the contract
        //   // check address on the second call (contract deployed)
        // } else {
        //   console.log(myContract.address) // the contract address
        //   completeBack(myContract.address)
        // }

        // Note that the returned "myContractReturned" === "myContract",
        // so the returned "myContractReturned" object will also get the address set.
      } else {
        failBack()
      }
    }
  )

  // tx.on('confirmation', function(confirmationNumber, receipt){
  //   sucBack(confirmationNumber)
  // });
  //定义监听事件
  // var me = bc.Transfer();
  // me.on('confirmation', function(confirmationNumber, receipt){
  //   sucBack(confirmationNumber)
  // })
  //返回交易Tx
  return tx;
}

