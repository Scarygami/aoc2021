const API_KEY = process.env.API_KEY;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS;

const contract = require("../artifacts/contracts/aoc01.sol/AOC01.json");

const alchemyProvider = new ethers.providers.AlchemyProvider(network="ropsten", API_KEY);
const signer = new ethers.Wallet(PRIVATE_KEY, alchemyProvider);
const token = new ethers.Contract(CONTRACT_ADDRESS, contract.abi, signer);

const testInput = [
  199,
  200,
  208,
  210,
  200,
  207,
  240,
  269,
  260,
  263
];

async function main() {
  const supply = await token.totalSupply();
  console.log("Total supply is: " + supply);

  let balance = await token.balanceOf(signer.address);
  console.log("Balance is: " + balance);

  const part1Tx = await token.part1(testInput);
  await part1Tx.wait();

  balance = await token.balanceOf(signer.address);
  console.log("Part 1 solution: " + balance);

  const part2Tx = await token.part2(testInput);
  await part2Tx.wait();

  balance = await token.balanceOf(signer.address);
  console.log("Part 2 solution: " + balance);
}

main();
