from typing import Dict, List

SEVERITY_ORDER = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
    "Info": 4
}

def aggregate_findings(file_report: Dict) -> List[Dict]:
    findings = []
    for finding in file_report.get("bug_results", []):
        item = dict(finding)
        item["category"] = "Bug"
        findings.append(item)

    for finding in file_report.get("quality_results", []):
        item = dict(finding)
        item["category"] = "Quality"
        findings.append(item)

    for finding in file_report.get("security_results", []):
        item = dict(finding)
        item["category"] = "Security"
        findings.append(item)

    for finding in file_report.get("improvement_results", []):
        item = dict(finding)

        if "severity" not in item:
            item["severity"] = "Info"

        item["category"] = "Improvement"
        findings.append(item)

    # ==========================================
    # DEDUPLICATE SECURITY FINDINGS
    # ==========================================

    security_issues = {
        finding.get("issue", "").lower().strip()
        for finding in findings
        if finding.get("category") == "Security"
    }

    filtered_findings = []

    for finding in findings:
        issue = finding.get("issue", "").lower().strip()
        category = finding.get("category")

        if (
            category in ["Bug", "Quality"]
            and issue in security_issues
        ):
            continue

        filtered_findings.append(finding)

    findings = filtered_findings

    findings.sort(
        key=lambda x: SEVERITY_ORDER.get(
            x.get("severity", "Info"),
            4
        )
    )

    return findings

def build_summary(findings: List[Dict]) -> Dict:
    return {
        "total_issues": len(findings),
        "critical_count": len(
            [f for f in findings if f.get("severity") == "Critical"]
        ),
        "high_count": len(
            [f for f in findings if f.get("severity") == "High"]
        ),
        "medium_count": len(
            [f for f in findings if f.get("severity") == "Medium"]
        ),
        "low_count": len(
            [f for f in findings if f.get("severity") == "Low"]
        ),
        "info_count": len(
            [f for f in findings if f.get("severity") == "Info"]
        )
    }

def generate_json_report(
    filename: str,
    file_report: Dict
) -> Dict:
    findings = aggregate_findings(file_report)
    return {
        "file_meta": {
            "filename": filename
        },
        "summary": build_summary(findings),
        "findings": findings
    }

def generate_markdown_report(
    filename: str,
    file_report: Dict
) -> str:
    findings = aggregate_findings(file_report)
    summary = build_summary(findings)
    markdown = f"# Code Review Report\n\n"
    markdown += f"## File: {filename}\n\n"

    markdown += "## Summary\n\n"
    markdown += f"- Total Issues: {summary['total_issues']}\n"
    markdown += f"- Critical: {summary['critical_count']}\n"
    markdown += f"- High: {summary['high_count']}\n"
    markdown += f"- Medium: {summary['medium_count']}\n"
    markdown += f"- Low: {summary['low_count']}\n"
    markdown += f"- Info: {summary['info_count']}\n\n"

    markdown += "## Findings\n\n"

    for finding in findings:
        markdown += (
            f"### [{finding.get('severity', 'Info')}] "
            f"{finding.get('category', 'Unknown')}\n\n"
        )

        if "issue" in finding:
            markdown += f"**Issue:** {finding['issue']}\n\n"

        if "suggestion" in finding:
            markdown += f"**Suggestion:** {finding['suggestion']}\n\n"

        if "line_hint" in finding:
            markdown += f"**Location:** {finding['line_hint']}\n\n"

        if "confidence" in finding:
            markdown += f"**Confidence:** {finding['confidence']}\n\n"

        if "cwe_id" in finding:
            markdown += f"**CWE:** {finding['cwe_id']}\n\n"

        if "owasp_category" in finding:
            markdown += (
                f"**OWASP Top 10:** "
                f"{finding['owasp_category']}\n\n"
            )

        if "explanation" in finding:
            markdown += (
                f"**Explanation:** "
                f"{finding['explanation']}\n\n"
            )

        if "evidence" in finding:
            markdown += "**Evidence:**\n\n"
            markdown += "```text\n"
            markdown += f"{finding['evidence']}\n"
            markdown += "```\n\n"

        if "remediation" in finding:
            markdown += (
                f"**Remediation:** "
                f"{finding['remediation']}\n\n"
            )

        if "reason" in finding:
            markdown += f"**Reason:** {finding['reason']}\n\n"

        if "impact" in finding:
            markdown += f"**Impact:** {finding['impact']}\n\n"

        markdown += "---\n\n"

    return markdown