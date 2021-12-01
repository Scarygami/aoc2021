const { expect } = require("chai");

describe("AOC01 contract", function () {

  const initialSupply = 1;

  let AOC01;
  let contract;
  let owner;
  let user;

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

  // `beforeEach` will run before each test, re-deploying the contract every
  // time. It receives a callback, which can be async.
  beforeEach(async function () {
    // Get the ContractFactory and Signers here.
    AOC01 = await ethers.getContractFactory("AOC01");
    [owner, user] = await ethers.getSigners();

    // To deploy our contract, we just have to call Token.deploy() and await
    // for it to be deployed(), which happens once its transaction has been
    // mined.
    contract = await AOC01.deploy(initialSupply);
  });

  it("Owner should have the initial supply", async function () {
    expect(await contract.balanceOf(owner.address)).to.be.equal(initialSupply);
  });

  it("Part 1 should mint the correct solution", async function () {
    await contract.connect(user).part1(testInput);
    const addrBalance = await contract.balanceOf(user.address);
    expect(addrBalance).to.be.equal(7);
  });

  it("Part 2 should mint the correct solution", async function () {
    await contract.connect(user).part2(testInput);
    const addrBalance = await contract.balanceOf(user.address);
    expect(addrBalance).to.be.equal(5);
  });
});
