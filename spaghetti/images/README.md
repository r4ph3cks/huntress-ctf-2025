# Images Directory

This directory should contain images used in the writeup. Images help illustrate technical concepts, analysis, and exploitation steps.

## Image Types by Category

### For Binary Exploitation Challenges (PWN)
- **offset_calculation.png** - Show offset calculations for buffer overflow
- **stack_layout.png** - Show how bytes are overwritten in memory
- **assembly_analysis.png** - Illustrate stack frame structure and assembly
- **rop_chain.png** - Demonstrate ROP chains and gadgets
- **memory_layout.png** - Show memory layout (stack, heap, BSS)

### For Reverse Engineering Challenges (REV)
- **function_flow.png** - Function flowchart and program logic
- **decompiled_code.png** - Decompiled code with annotations
- **algorithm_analysis.png** - Analysis of important algorithms
- **debugger_view.png** - Debugger screenshots with values

### For Web Challenges (WEB)
- **request_response.png** - HTTP request/response captures
- **payload_construction.png** - Show payload construction
- **source_analysis.png** - Source code analysis
- **vulnerability_location.png** - Vulnerability location in code

### For Cryptography Challenges (CRYPTO)
- **algorithm_flow.png** - Cryptographic algorithm flow
- **key_analysis.png** - Key/pattern analysis
- **attack_implementation.png** - Attack implementation
- **mathematical_proof.png** - Mathematical proofs or calculations

### For Forensics Challenges (FORENSICS)
- **file_analysis.png** - Hexadecimal file analysis
- **timeline.png** - Timeline of events
- **artifact_extraction.png** - Artifact extraction
- **metadata_analysis.png** - Metadata information

### For Miscellaneous Challenges (MISC)
- **data_pattern.png** - Patterns found in data
- **automation_script.png** - Automation scripts
- **problem_breakdown.png** - Problem breakdown into parts
- **solution_verification.png** - Solution verification

### For OSINT Challenges
- **search_results.png** - Search results
- **data_correlation.png** - Information correlation
- **social_media.png** - Social media captures
- **geolocation.png** - Geolocation information

### For Steganography Challenges (STEGO)
- **file_comparison.png** - File comparison
- **hidden_data.png** - Revealed hidden data
- **analysis_tools.png** - Analysis tools
- **extraction_process.png** - Extraction process

## Naming Conventions

Use descriptive names for images:
- `offset_calculation.png` instead of `img1.png`
- `stack_layout.png` instead of `screenshot.png`
- `payload_structure.png` instead of `exploit.png`

## How to Reference in Writeup

Use the following syntax in markdown:

```markdown
![Image description](images/image_name.png)
```

Example:
```markdown
![Buffer overflow offset calculation](images/offset_calculation.png)
```

## Recommended Tools for Screenshots

- **GDB/Pwndbg** - For debugging and memory analysis
- **Ghidra/IDA** - For reverse engineering
- **Wireshark** - For network analysis
- **Burp Suite** - For web testing
- **HxD/010 Editor** - For hexadecimal analysis

## Tips for Good Images

1. **Use high resolution** - So text is readable
2. **Highlight important information** - Use arrows, boxes or colors
3. **Maintain consistency** - Use the same theme/style in all images
4. **Include context** - Show enough information for understanding
5. **Avoid sensitive information** - Don't include flags from other teams or private info

## Example Image Structure

For a typical PWN writeup:
```
images/
├── file_info.png           # Output of 'file' command
├── checksec_output.png     # Checksec output
├── ghidra_main.png         # Main function in Ghidra
├── vulnerable_function.png # Vulnerable function
├── offset_calculation.png  # Offset calculation
├── stack_layout.png        # Stack layout
├── rop_chain.png          # ROP chain structure
├── exploit_success.png     # Successful execution
└── flag_capture.png        # Flag capture
```