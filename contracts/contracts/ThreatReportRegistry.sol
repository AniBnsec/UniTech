// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ThreatReportRegistry
 * @dev Decentralized, tamper-evident registry for cryptographic commitments of digital threat reports.
 *      Preserves strict privacy: Raw URLs, personal data, and message bodies remain strictly OFF-CHAIN.
 *      Anchors Keccak-256 hashes of canonical threat reports and indicator digests on-chain.
 */
contract ThreatReportRegistry {

    enum RiskClassification {
        LowRisk,        // 0: Clean / No significant threat found
        Suspicious,     // 1: Multiple anomalies requiring caution
        HighRisk,       // 2: Strong threat indicators (typosquatting, invalid trust)
        ConfirmedMalicious, // 3: Verified malicious (known phishing/compromised CA)
        Inconclusive    // 4: Insufficient data or unreachable host
    }

    enum ReportStatus {
        Active,         // 0: Normal active report
        Verified,       // 1: Verified by multiple independent nodes/analysts
        Disputed,       // 2: Under community review or disputed
        Revoked         // 3: Revoked due to correction or remediation
    }

    struct ThreatReport {
        bytes32 reportHash;           // Keccak-256 commitment of canonical JSON report
        bytes32 indicatorHash;        // Keccak-256 hash of normalized domain or indicator
        RiskClassification riskClass; // Standardized risk classification
        uint8 riskScore;              // Computed risk score (0 to 100)
        uint64 timestamp;             // Block timestamp when registered
        address reporter;             // Submitter wallet address
        ReportStatus status;          // Lifecycle status
        uint32 verificationCount;     // Independent peer attestations
        uint32 disputeCount;          // Dispute submissions
        string ipfsCid;               // Optional IPFS/Arweave content identifier for encrypted archive
    }

    // Mapping: reportHash => ThreatReport
    mapping(bytes32 => ThreatReport) public reports;

    // Mapping: indicatorHash => array of associated reportHashes
    mapping(bytes32 => bytes32[]) private indicatorToReports;

    // List of all registered report hashes for enumeration
    bytes32[] public reportHashes;

    // Events
    event ReportRegistered(
        bytes32 indexed reportHash,
        bytes32 indexed indicatorHash,
        address indexed reporter,
        RiskClassification riskClass,
        uint8 riskScore,
        uint64 timestamp
    );

    event ReportAttested(
        bytes32 indexed reportHash,
        address indexed validator,
        uint32 newVerificationCount
    );

    event ReportDisputed(
        bytes32 indexed reportHash,
        address indexed disputer,
        string reason
    );

    event ReportRevoked(
        bytes32 indexed reportHash,
        address indexed revoker,
        string reason
    );

    error ReportAlreadyExists(bytes32 reportHash);
    error ReportNotFound(bytes32 reportHash);
    error Unauthorized(address caller);
    error InvalidScore(uint8 score);

    /**
     * @notice Registers a new threat report commitment.
     * @param reportHash Keccak-256 of canonical report JSON
     * @param indicatorHash Keccak-256 of normalized target indicator (domain, URL hash)
     * @param riskClass Classification enum (0 to 4)
     * @param riskScore Numerical risk score between 0 and 100
     * @param ipfsCid Optional CID reference (empty string if none)
     */
    function registerReport(
        bytes32 reportHash,
        bytes32 indicatorHash,
        RiskClassification riskClass,
        uint8 riskScore,
        string calldata ipfsCid
    ) external returns (bool) {
        if (reports[reportHash].timestamp != 0) {
            revert ReportAlreadyExists(reportHash);
        }
        if (riskScore > 100) {
            revert InvalidScore(riskScore);
        }

        uint64 currentTimestamp = uint64(block.timestamp);

        reports[reportHash] = ThreatReport({
            reportHash: reportHash,
            indicatorHash: indicatorHash,
            riskClass: riskClass,
            riskScore: riskScore,
            timestamp: currentTimestamp,
            reporter: msg.sender,
            status: ReportStatus.Active,
            verificationCount: 1,
            disputeCount: 0,
            ipfsCid: ipfsCid
        });

        indicatorToReports[indicatorHash].push(reportHash);
        reportHashes.push(reportHash);

        emit ReportRegistered(
            reportHash,
            indicatorHash,
            msg.sender,
            riskClass,
            riskScore,
            currentTimestamp
        );

        return true;
    }

    /**
     * @notice Attest/verify an existing registered threat report.
     * @param reportHash The report commitment to attest.
     */
    function attestReport(bytes32 reportHash) external returns (uint32) {
        ThreatReport storage report = reports[reportHash];
        if (report.timestamp == 0) {
            revert ReportNotFound(reportHash);
        }

        report.verificationCount += 1;
        if (report.verificationCount >= 3 && report.status == ReportStatus.Active) {
            report.status = ReportStatus.Verified;
        }

        emit ReportAttested(reportHash, msg.sender, report.verificationCount);
        return report.verificationCount;
    }

    /**
     * @notice Dispute a report if believed to be a false positive.
     * @param reportHash The report commitment to dispute.
     * @param reason Brief description or reference.
     */
    function disputeReport(bytes32 reportHash, string calldata reason) external {
        ThreatReport storage report = reports[reportHash];
        if (report.timestamp == 0) {
            revert ReportNotFound(reportHash);
        }

        report.disputeCount += 1;
        if (report.disputeCount >= 3) {
            report.status = ReportStatus.Disputed;
        }

        emit ReportDisputed(reportHash, msg.sender, reason);
    }

    /**
     * @notice Revoke a report (restricted to original reporter).
     * @param reportHash The report commitment to revoke.
     * @param reason The rationale for revocation.
     */
    function revokeReport(bytes32 reportHash, string calldata reason) external {
        ThreatReport storage report = reports[reportHash];
        if (report.timestamp == 0) {
            revert ReportNotFound(reportHash);
        }
        if (report.reporter != msg.sender) {
            revert Unauthorized(msg.sender);
        }

        report.status = ReportStatus.Revoked;
        emit ReportRevoked(reportHash, msg.sender, reason);
    }

    /**
     * @notice Verifies the integrity of a locally held report against on-chain cryptographic commitment.
     * @param reportHash The Keccak-256 hash computed from local report
     * @return exists Whether the report exists on-chain
     * @return matches Whether on-chain parameters match
     * @param expectedIndicatorHash Hash of indicator in local report
     * @param expectedRiskScore Risk score in local report
     * @return onChainTimestamp Timestamp when anchored
     * @return reporter Address of submitter
     * @return status Current status enum
     */
    function verifyIntegrity(
        bytes32 reportHash,
        bytes32 expectedIndicatorHash,
        uint8 expectedRiskScore
    ) external view returns (
        bool exists,
        bool matches,
        uint64 onChainTimestamp,
        address reporter,
        ReportStatus status
    ) {
        ThreatReport memory report = reports[reportHash];
        if (report.timestamp == 0) {
            return (false, false, 0, address(0), ReportStatus.Active);
        }

        bool paramMatch = (report.indicatorHash == expectedIndicatorHash && report.riskScore == expectedRiskScore);
        return (true, paramMatch, report.timestamp, report.reporter, report.status);
    }

    /**
     * @notice Retrieve full report record by hash.
     */
    function getReport(bytes32 reportHash) external view returns (ThreatReport memory) {
        ThreatReport memory report = reports[reportHash];
        if (report.timestamp == 0) {
            revert ReportNotFound(reportHash);
        }
        return report;
    }

    /**
     * @notice Get all report hashes associated with a given indicator.
     */
    function getReportsForIndicator(bytes32 indicatorHash) external view returns (bytes32[] memory) {
        return indicatorToReports[indicatorHash];
    }

    /**
     * @notice Returns total number of registered reports.
     */
    function getTotalReports() external view returns (uint256) {
        return reportHashes.length;
    }
}
