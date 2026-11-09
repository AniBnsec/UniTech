import { ethers } from "hardhat";

async function main() {
  console.log("Deploying ThreatIntelRegistry contract...");

  // Get the contract factory
  const ThreatIntelRegistry = await ethers.getContractFactory("ThreatIntelRegistry");

  // Deploy the contract
  const registry = await ThreatIntelRegistry.deploy();

  await registry.waitForDeployment();

  const address = await registry.getAddress();

  console.log(`✅ ThreatIntelRegistry deployed to: ${address}`);
  console.log(`\nAdd this address to your .env file:`);
  console.log(`CONTRACT_ADDRESS=${address}`);

  // Wait for a few block confirmations
  console.log("\nWaiting for block confirmations...");
  await registry.deploymentTransaction()?.wait(5);

  console.log("\n✅ Deployment complete!");
  console.log(`\nVerify on Etherscan:`);
  console.log(`npx hardhat verify --network sepolia ${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
