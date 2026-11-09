import { expect } from "chai";
import { ethers } from "hardhat";
import { ThreatIntelRegistry } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";

describe("ThreatIntelRegistry", function () {
  let registry: ThreatIntelRegistry;
  let owner: SignerWithAddress;
  let user1: SignerWithAddress;
  let user2: SignerWithAddress;

  const sampleHash = ethers.keccak256(ethers.toUtf8Bytes("test-report-1"));

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();

    const ThreatIntelRegistry = await ethers.getContractFactory("ThreatIntelRegistry");
    registry = await ThreatIntelRegistry.deploy();
    await registry.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should deploy successfully", async function () {
      expect(await registry.getAddress()).to.be.properAddress;
    });

    it("Should start with zero reports", async function () {
      expect(await registry.getReportCount()).to.equal(0);
    });
  });

  describe("Report Registration", function () {
    it("Should register a new report", async function () {
      await expect(registry.connect(user1).registerReport(sampleHash))
        .to.emit(registry, "ReportRegistered")
        .withArgs(sampleHash, user1.address, await getBlockTimestamp(), await getBlockNumber());

      const report = await registry.getReport(sampleHash);
      expect(report.exists).to.be.true;
      expect(report.submitter).to.equal(user1.address);
    });

    it("Should not allow duplicate registrations", async function () {
      await registry.connect(user1).registerReport(sampleHash);
      await expect(registry.connect(user2).registerReport(sampleHash))
        .to.be.revertedWith("Report already registered");
    });

    it("Should reject zero hash", async function () {
      await expect(registry.registerReport(ethers.ZeroHash))
        .to.be.revertedWith("Invalid report hash");
    });

    it("Should increment report count", async function () {
      await registry.registerReport(sampleHash);
      expect(await registry.getReportCount()).to.equal(1);

      const hash2 = ethers.keccak256(ethers.toUtf8Bytes("test-report-2"));
      await registry.registerReport(hash2);
      expect(await registry.getReportCount()).to.equal(2);
    });
  });

  describe("Report Verification", function () {
    beforeEach(async function () {
      await registry.connect(user1).registerReport(sampleHash);
    });

    it("Should verify existing report", async function () {
      const report = await registry.getReport(sampleHash);
      expect(report.exists).to.be.true;
      expect(report.submitter).to.equal(user1.address);
    });

    it("Should return false for non-existent report", async function () {
      const fakeHash = ethers.keccak256(ethers.toUtf8Bytes("fake-report"));
      const report = await registry.getReport(fakeHash);
      expect(report.exists).to.be.false;
    });

    it("Should emit verification event", async function () {
      await expect(registry.connect(user2).verifyReport(sampleHash))
        .to.emit(registry, "ReportVerified")
        .withArgs(sampleHash, user2.address, true);
    });
  });

  describe("Query Functions", function () {
    it("Should get reports by submitter", async function () {
      const hash1 = ethers.keccak256(ethers.toUtf8Bytes("report-1"));
      const hash2 = ethers.keccak256(ethers.toUtf8Bytes("report-2"));

      await registry.connect(user1).registerReport(hash1);
      await registry.connect(user1).registerReport(hash2);

      const reports = await registry.getReportsBySubmitter(user1.address);
      expect(reports.length).to.equal(2);
      expect(reports[0]).to.equal(hash1);
      expect(reports[1]).to.equal(hash2);
    });

    it("Should get report by index", async function () {
      await registry.registerReport(sampleHash);
      const hash = await registry.getReportHashByIndex(0);
      expect(hash).to.equal(sampleHash);
    });

    it("Should revert for invalid index", async function () {
      await expect(registry.getReportHashByIndex(0))
        .to.be.revertedWith("Index out of bounds");
    });
  });

  async function getBlockTimestamp(): Promise<number> {
    const blockNum = await ethers.provider.getBlockNumber();
    const block = await ethers.provider.getBlock(blockNum);
    return block!.timestamp + 1;
  }

  async function getBlockNumber(): Promise<number> {
    return (await ethers.provider.getBlockNumber()) + 1;
  }
});
