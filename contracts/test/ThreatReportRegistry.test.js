const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ThreatReportRegistry Smart Contract", function () {
  let ThreatReportRegistry;
  let registry;
  let owner, validator1, validator2, validator3, disputer, attacker;

  const mockReportHash = ethers.keccak256(ethers.toUtf8Bytes(JSON.stringify({ domain: "paypaI-security.com", risk: 92 })));
  const mockIndicatorHash = ethers.keccak256(ethers.toUtf8Bytes("paypai-security.com"));
  const riskClass = 3; // ConfirmedMalicious
  const riskScore = 92;

  beforeEach(async function () {
    [owner, validator1, validator2, validator3, disputer, attacker] = await ethers.getSigners();
    ThreatReportRegistry = await ethers.getContractFactory("ThreatReportRegistry");
    registry = await ThreatReportRegistry.deploy();
    await registry.waitForDeployment();
  });

  it("Should successfully register a new threat report commitment", async function () {
    const tx = await registry.registerReport(
      mockReportHash,
      mockIndicatorHash,
      riskClass,
      riskScore,
      "ipfs://QmThreatProofSample123"
    );
    await tx.wait();

    const report = await registry.getReport(mockReportHash);
    expect(report.reportHash).to.equal(mockReportHash);
    expect(report.indicatorHash).to.equal(mockIndicatorHash);
    expect(report.riskClass).to.equal(riskClass);
    expect(report.riskScore).to.equal(riskScore);
    expect(report.reporter).to.equal(owner.address);
    expect(report.status).to.equal(0); // Active
    expect(report.verificationCount).to.equal(1);
    expect(await registry.getTotalReports()).to.equal(1);
  });

  it("Should prevent duplicate registrations of identical report hash", async function () {
    await registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "");

    await expect(
      registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "")
    ).to.be.revertedWithCustomError(registry, "ReportAlreadyExists");
  });

  it("Should reject invalid risk scores exceeding 100", async function () {
    await expect(
      registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, 105, "")
    ).to.be.revertedWithCustomError(registry, "InvalidScore");
  });

  it("Should allow independent peer attestations and transition to Verified status", async function () {
    await registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "");

    // Validator 1 attests
    await registry.connect(validator1).attestReport(mockReportHash);
    let report = await registry.getReport(mockReportHash);
    expect(report.verificationCount).to.equal(2);
    expect(report.status).to.equal(0); // Still Active

    // Validator 2 attests -> hits threshold of 3 -> status becomes Verified (1)
    await registry.connect(validator2).attestReport(mockReportHash);
    report = await registry.getReport(mockReportHash);
    expect(report.verificationCount).to.equal(3);
    expect(report.status).to.equal(1); // Verified
  });

  it("Should allow community disputes", async function () {
    await registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "");
    await registry.connect(disputer).disputeReport(mockReportHash, "Suspected false positive");

    const report = await registry.getReport(mockReportHash);
    expect(report.disputeCount).to.equal(1);
  });

  it("Should enforce revocation rights exclusively to the original reporter", async function () {
    await registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "");

    // Attacker tries to revoke
    await expect(
      registry.connect(attacker).revokeReport(mockReportHash, "Malicious attempt")
    ).to.be.revertedWithCustomError(registry, "Unauthorized");

    // Original owner revokes
    await registry.revokeReport(mockReportHash, "Resolved and patched by domain owner");
    const report = await registry.getReport(mockReportHash);
    expect(report.status).to.equal(3); // Revoked
  });

  it("Should perform independent integrity verification against on-chain state", async function () {
    await registry.registerReport(mockReportHash, mockIndicatorHash, riskClass, riskScore, "");

    // Correct verification
    const [exists, matches, timestamp, reporter, status] = await registry.verifyIntegrity(
      mockReportHash,
      mockIndicatorHash,
      riskScore
    );

    expect(exists).to.be.true;
    expect(matches).to.be.true;
    expect(reporter).to.equal(owner.address);

    // Mismatched score verification (detects tampering of off-chain report)
    const [exists2, matches2] = await registry.verifyIntegrity(
      mockReportHash,
      mockIndicatorHash,
      50 // Tampered score
    );
    expect(exists2).to.be.true;
    expect(matches2).to.be.false; // Tamper detected!
  });
});
