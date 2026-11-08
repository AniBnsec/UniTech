const hre = require("hardhat");

async function main() {
  console.log("Deploying ThreatReportRegistry contract...");
  const ThreatReportRegistry = await hre.ethers.getContractFactory("ThreatReportRegistry");
  const registry = await ThreatReportRegistry.deploy();
  await registry.waitForDeployment();

  const address = await registry.getAddress();
  console.log(`ThreatReportRegistry successfully deployed to: ${address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
