from data_models import AttackChain

class ReportGenerator:
    def generate_attack_chain_report(self, attack_chain: AttackChain):
        report = f"# Attack Chain Report: {attack_chain.objective.value}\n\n"
        report += f"**Entry Point:** {attack_chain.entry_point.type.value} - `{attack_chain.entry_point.value}`\n"
        report += f"**Difficulty:** {attack_chain.difficulty.value}\n"
        report += f"**Detection Risk:** {attack_chain.detection_risk.value}\n\n"
        report += "## Steps to Reproduce\n\n"

        for i, step in enumerate(attack_chain.steps):
            report += f"### Step {i+1}: {step.type.value}\n\n"
            report += f"**Description:** A {step.type.value} was found with the value `{step.value}`.\n"
            report += f"**Source:** {step.source_module}\n"
            report += f"**Target:** {step.target}\n"
            report += f"**Confidence:** {step.confidence}\n"
            
            # Add exploitation guidance based on finding type
            if step.type.value == "api_key":
                report += "**Exploitation:** This API key could potentially be used to access sensitive data or functionality. Try using this key with common API endpoints associated with the target.\n"
            elif step.type.value == "endpoint":
                report += "**Exploitation:** This endpoint may be vulnerable to common web attacks such as SQL injection, XSS, or parameter tampering. Fuzzing the endpoint for vulnerabilities is recommended.\n"
            elif step.type.value == "sensitive_data":
                report += "**Exploitation:** This indicates a direct leak of sensitive information. The data should be reviewed for personally identifiable information (PII), credentials, or other confidential data.\n"
            report += "\n"

        return report
