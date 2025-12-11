import sys
sys.path.insert(0, 'src')

from agent import TPRMAgent

def investigate_vendor():
    """Run a complete vendor investigation."""
    agent = TPRMAgent()
    
    # Run investigation
    result = agent.investigate(
        vendor_name="Acme Corp",
        categories=["litigation", "financial", "fraud"],
        generate_monitors=True,
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Investigation Complete: {result.vendor_name}")
    print(f"{'='*60}")
    print(f"Sources Found: {result.total_sources_found}")
    print(f"Sources Accessed: {result.total_sources_accessed}")
    print(f"Risk Assessments: {len(result.risk_assessments)}")
    print(f"Monitoring Scripts: {len(result.monitoring_scripts)}")
    
    # Print risk assessments
    for assessment in result.risk_assessments:
        print(f"\n{'─'*60}")
        print(f"[{assessment.category.upper()}] Severity: {assessment.severity.upper()}")
        print(f"{'─'*60}")
        print(f"Summary: {assessment.summary}")
        print("\nKey Findings:")
        for finding in assessment.key_findings:
            print(f"  • {finding}")
        print("\nRecommended Actions:")
        for action in assessment.recommended_actions:
            print(f"  → {action}")
    
    # Print monitoring script info
    for script in result.monitoring_scripts:
        print(f"\n{'='*60}")
        print(f"Generated Monitoring Script")
        print(f"{'='*60}")
        print(f"Path: {script.script_path}")
        print(f"Monitoring {len(script.urls_monitored)} URLs")
        print(f"Frequency: {script.check_frequency}")
    
    # Print errors if any
    if result.errors:
        print(f"\n{'='*60}")
        print("Errors:")
        for error in result.errors:
            print(f"  ⚠️  {error}")

if __name__ == "__main__":
    investigate_vendor()