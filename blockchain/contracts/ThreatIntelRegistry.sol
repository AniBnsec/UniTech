// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ThreatIntelRegistry
 * @dev Tamper-evident registry for cybersecurity threat intelligence reports
 * @notice This contract stores hashes of threat reports on-chain for verification
 */
contract ThreatIntelRegistry {
    
    struct ThreatReport {
        bytes32 reportHash;      // SHA-256 hash of the report
        address submitter;       // Address that submitted the report
        uint256 timestamp;       // Block timestamp
        uint256 blockNumber;     // Block number
        bool exists;             // Flag to check if report exists
    }
    
    // Mapping from report hash to ThreatReport struct
    mapping(bytes32 => ThreatReport) public reports;
    
    // Array to store all report hashes for enumeration
    bytes32[] public reportHashes;
    
    // Mapping to track submitter's reports
    mapping(address => bytes32[]) public submitterReports;
    
    // Events
    event ReportRegistered(
        bytes32 indexed reportHash,
        address indexed submitter,
        uint256 timestamp,
        uint256 blockNumber
    );
    
    event ReportVerified(
        bytes32 indexed reportHash,
        address indexed verifier,
        bool exists
    );
    
    /**
     * @dev Register a new threat report hash
     * @param _reportHash SHA-256 hash of the threat report
     */
    function registerReport(bytes32 _reportHash) external {
        require(_reportHash != bytes32(0), "Invalid report hash");
        require(!reports[_reportHash].exists, "Report already registered");
        
        // Create new report record
        reports[_reportHash] = ThreatReport({
            reportHash: _reportHash,
            submitter: msg.sender,
            timestamp: block.timestamp,
            blockNumber: block.number,
            exists: true
        });
        
        // Add to arrays
        reportHashes.push(_reportHash);
        submitterReports[msg.sender].push(_reportHash);
        
        // Emit event
        emit ReportRegistered(
            _reportHash,
            msg.sender,
            block.timestamp,
            block.number
        );
    }
    
    /**
     * @dev Verify if a report hash exists in the registry
     * @param _reportHash SHA-256 hash to verify
     * @return exists Whether the report exists
     * @return submitter Address that submitted the report
     * @return timestamp When the report was registered
     * @return blockNumber Block number of registration
     */
    function verifyReport(bytes32 _reportHash) 
        external 
        returns (
            bool exists,
            address submitter,
            uint256 timestamp,
            uint256 blockNumber
        ) 
    {
        ThreatReport memory report = reports[_reportHash];
        
        emit ReportVerified(_reportHash, msg.sender, report.exists);
        
        return (
            report.exists,
            report.submitter,
            report.timestamp,
            report.blockNumber
        );
    }
    
    /**
     * @dev Get report details (view function, no gas cost)
     * @param _reportHash SHA-256 hash to query
     * @return exists Whether the report exists
     * @return submitter Address that submitted the report
     * @return timestamp When the report was registered
     * @return blockNumber Block number of registration
     */
    function getReport(bytes32 _reportHash)
        external
        view
        returns (
            bool exists,
            address submitter,
            uint256 timestamp,
            uint256 blockNumber
        )
    {
        ThreatReport memory report = reports[_reportHash];
        return (
            report.exists,
            report.submitter,
            report.timestamp,
            report.blockNumber
        );
    }
    
    /**
     * @dev Get total number of registered reports
     * @return count Total number of reports
     */
    function getReportCount() external view returns (uint256 count) {
        return reportHashes.length;
    }
    
    /**
     * @dev Get reports by submitter
     * @param _submitter Address to query
     * @return hashes Array of report hashes submitted by address
     */
    function getReportsBySubmitter(address _submitter)
        external
        view
        returns (bytes32[] memory hashes)
    {
        return submitterReports[_submitter];
    }
    
    /**
     * @dev Get report hash by index
     * @param _index Index in the reportHashes array
     * @return reportHash The report hash at given index
     */
    function getReportHashByIndex(uint256 _index)
        external
        view
        returns (bytes32 reportHash)
    {
        require(_index < reportHashes.length, "Index out of bounds");
        return reportHashes[_index];
    }
}
