async function main() {
  const AOC01 = await ethers.getContractFactory("AOC01");

  // Start deployment, returning a promise that resolves to a contract object
  const contract = await AOC01.deploy(1);
  console.log("Contract deployed to address:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
